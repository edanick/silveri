import subprocess, sys, os, time, glob

SILVERI = r"C:\Users\haya_\OneDrive\Desktop\Code\rust\silver\silveri\silveri.exe"
TESTS_DIR = r"C:\Users\haya_\OneDrive\Desktop\Code\rust\silver\tests"
TIMEOUT = 15

def run_test(path):
    try:
        proc = subprocess.run(
            [SILVERI, path],
            capture_output=True, text=True, timeout=TIMEOUT,
            cwd=r"C:\Users\haya_\OneDrive\Desktop\Code\rust\silver"
        )
        ok = proc.returncode == 0
        return ok, proc.returncode, proc.stdout[-200:] if proc.stdout else "", proc.stderr[-200:] if proc.stderr else ""
    except subprocess.TimeoutExpired:
        return False, -1, "", "TIMEOUT"
    except Exception as e:
        return False, -2, "", str(e)

files = sorted(glob.glob(os.path.join(TESTS_DIR, "*.sr")))
print(f"Total test files: {len(files)}")

passes = 0
fails = 0
timeouts = 0
fail_list = []

for i, f in enumerate(files):
    name = os.path.basename(f)
    ok, rc, out, err = run_test(f)
    if ok:
        passes += 1
    elif rc == -1:
        timeouts += 1
        fails += 1
        fail_list.append((name, "TIMEOUT"))
    else:
        fails += 1
        fail_list.append((name, f"rc={rc} {err[:80]}"))
    
    if (i+1) % 50 == 0:
        print(f"  Progress: {i+1}/{len(files)}")

print(f"\nResults: {passes} pass, {fails} fail ({timeouts} timeouts)")
if fail_list:
    print(f"\nFirst 20 failures:")
    for name, reason in fail_list[:20]:
        print(f"  {name}: {reason}")