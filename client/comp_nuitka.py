import os
import subprocess
import shutil

SCRIPT_NAME = "polymorphic_main.py"
OUTPUT_DIR = "compiled_payloads"
EXE_NAME = "payload.exe"

def compile_to_exe():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("[+] Compiling to C using Nuitka...")

    compile_command = [
        "nuitka",
        "--mingw64",
        "--onefile",
        "--windows-disable-console",
        "--output-dir=dist",
        f"--output-filename={EXE_NAME}",
        SCRIPT_NAME
    ]

    result = subprocess.run(compile_command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[-] Compilation failed: {result.stderr}")
        return

    build_path = f"dist/{EXE_NAME}"
    final_path = os.path.join(OUTPUT_DIR, EXE_NAME)

    if os.path.exists(build_path):
        shutil.move(build_path, final_path)
        print(f"[+] Compiled EXE saved to: {final_path}")
    else:
        print("[-] Compilation failed.")

if __name__ == "__main__":
    compile_to_exe()
