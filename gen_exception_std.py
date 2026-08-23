#!/usr/bin/env python3
"""Generate silveri/src/exception_std.sr from silverc-rs/std/exception.sr.

The interpreter has no source-loader, so (like llmai_std) it embeds the std
source as a string and parses it at startup. The canonical hierarchy lives in
silverc-rs/std/exception.sr (and is mirrored in silverc/std/exception.sr); this
script turns it into an `exception_std.source()` string module.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "silverc-rs" / "std" / "exception.sr"
OUT = Path(__file__).resolve().parent / "src" / "exception_std.sr"

body = SRC.read_text(encoding="utf-8")

# Strip the module declaration line; the prelude registers the classes at
# top level so they do not need (and should not re-declare) a module.
lines = body.splitlines()
if lines and lines[0].startswith("mod export"):
    lines = lines[1:]
body = "\n".join(lines)

# Escape for embedding inside a double-quoted Silver string literal. The
# exception source contains no double quotes or backslashes today, but keep the
# transform so the generator stays correct if comments/strings are added later.
escaped = body.replace("\\", "\\\\").replace('"', '\\"')

header = (
    "mod export exception_std;\n"
    "\n"
    "// The interpreter has no source-loader, so the exception hierarchy is\n"
    "// embedded here and parsed at startup (see main.sr), mirroring llmai_std.\n"
    "// Keep this in sync with silverc-rs/std/exception.sr and\n"
    "// silverc/std/exception.sr.\n"
    "//\n"
    "// NOTE: the accessor must NOT be named `source()`: the self-hosted\n"
    "// compiler flattens module-level functions to the global namespace by\n"
    "// bare name, so it would collide with llmai_std.source().\n"
    "public string exceptionSource() {\n"
    "    return \""
)

footer = "\";\n}\n"

OUT.write_text(header + escaped + footer, encoding="utf-8")
print(f"Wrote {OUT} ({len(escaped)} chars of embedded source)")
