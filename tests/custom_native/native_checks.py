#!/usr/bin/env python3
"""Regression coverage for interpreted `.srp` `nativeModules` (DOCS/261).

Runs the staged silveri binary over the FAKE-name fixtures in this directory
(positive runs must exit 0 with the documented stdout markers; negative runs
must exit 1 with the exact contract message) plus the `.qs` spinner consumer
proof. No real native libraries are ever touched.

Usage:
    python tests/custom_native/native_checks.py [interpreter]

    interpreter: path to the silveri binary (default: <repo>/silveri/silveri.exe
                 -- stage it to /tmp/opencode first: vfat checkouts cannot
                 execute binaries in place).

    Working directory must be the silveri project root (std probing and
    `build/diag` crumbs are cwd-relative, like the main test runner).
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SILVERI = HERE.parent.parent
INTERP = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else SILVERI / "silveri" / "silveri.exe"

STANZA = ('"nativeModules": [ {{ "module": "{m}", '
          '"windows": "<dll>", "linux": "<lib>" }} ]')

CASES = [
    # (args, cwd-relative-to-silvery, expected exit, expected stdout fragments)
    (["tests/custom_native/custom_native.srp"], ".", 0, [
        "gfx stub OK", "samefile stub OK", "sharea stub OK",
        "shareb stub OK", "starAlpha stub OK", "starBeta stub OK",
        "win32.fakebridge stub OK", "linux.fakebridge stub OK",
        "custom native grants OK",
    ]),
    (["--os", "windows", "tests/custom_native/custom_native.srp"], ".", 0, [
        "custom native grants OK",
    ]),
    (["--os", "windows", "tests/custom_native/wrongside.srp"], ".", 0, [
        "winonly stub OK",
    ]),
    (["tests/custom_native/shadow_std.srp"], ".", 0, ["shadow std OK"]),
    (["tests/custom_native/shadow_project.srp"], ".", 0, ["shadow project OK"]),
    (["tests/custom_native/casefold.srp"], ".", 0, ["casefold stub OK"]),
    (["tests/custom_native/fixed_collision.srp"], ".", 0, ["fixed collision OK"]),
    (["tests/custom_native/consumer_with.srp"], ".", 0, ["qs consumer: stub"]),
    (["tests/custom_native/undeclared.srp"], ".", 1, [
        'unknown native module "win32.nosuchmod"',
        STANZA.format(m="nosuchmod"),
    ]),
    (["tests/custom_native/undeclared_bare.srp"], ".", 1, [
        'unknown native module "nosuchbare"',
        STANZA.format(m="nosuchbare"),
    ]),
    (["tests/custom_native/wrongside.srp"], ".", 1, [
        'custom native module "winonly" has no library for LINUX targets',
        '(entry declares "windows": "fake-winonly.dll" only)',
        'add "linux": "<lib>" to its "nativeModules" entry',
    ]),
    (["tests/custom_native/star_nolist.srp"], ".", 1, [
        'whole-module import of custom native module "gfx" is not supported',
        'import { FuncName } from "gfx"',
    ]),
    (["tests/custom_native/prefixed_star.srp"], ".", 1, [
        'whole-module import of custom native module "win32.fakebridge" is not supported',
    ]),
    (["tests/custom_native/wholemod.srp"], ".", 1, [
        'whole-module import of custom native module "win32.fakebridge" is not supported',
    ]),
    (["tests/custom_native/consumer_without.srp"], ".", 1, [
        'unknown native module "fakebridge"',
        STANZA.format(m="fakebridge"),
    ]),
]

SPINNER_EXPECTED = [
    "loading |", "loading /", "loading -", "loading \\",
    "[    ]", "[=   ]", "[==  ]",
]


def run_one(args, cwd):
    try:
        return subprocess.run(
            [str(INTERP)] + args,
            capture_output=True, text=True, timeout=120, cwd=str(cwd),
        )
    except subprocess.TimeoutExpired:
        return None


def main() -> int:
    if not INTERP.exists():
        sys.exit(f"interpreter not found: {INTERP}")
    print(f"Interpreter: {INTERP}")
    passed = failed = 0
    for args, rel, code, frags in CASES:
        r = run_one(args, SILVERI / rel)
        label = " ".join(args)
        if r is None:
            print(f"  FAIL {label}: timeout");
            failed += 1
            continue
        missing = [f for f in frags if f not in (r.stdout or "")]
        if r.returncode != code or missing:
            print(f"  FAIL {label}: exit {r.returncode} (want {code})"
                  + (f", missing {missing}" if missing else ""))
            print("    stdout: " + (r.stdout or "").strip().splitlines()[:1].__str__())
            failed += 1
        else:
            print(f"  ok {label}")
            passed += 1
    # Interpreted-run proof: the spinners `.qs` consumer to documented output.
    demo_dir = SILVERI.parent / "demo qs" / "examples"
    r = run_one(["spinner_demo.srp"], demo_dir)
    lines = (r.stdout or "").strip().splitlines() if r is not None else []
    if r is not None and r.returncode == 0 and lines == SPINNER_EXPECTED:
        print("  ok spinner_demo.srp (.qs consumer proof)")
        passed += 1
    else:
        print(f"  FAIL spinner_demo.srp: exit {None if r is None else r.returncode}, "
              f"output {lines}")
        failed += 1
    print(f"{passed}/{passed + failed} native checks passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
