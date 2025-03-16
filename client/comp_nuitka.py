import os
import subprocess
import shutil
import sys

SCRIPT_NAME = "polymorphic_main.py"
OUTPUT_DIR = "compiled_payloads"
EXE_NAME = "payload.exe"

def compile_to_exe(script_name, exe_name):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("[+] Compiling to C using Nuitka...")

    compile_command = [
        "nuitka",
        "--mingw64",
        "--onefile",
        "--windows-disable-console",
        "--output-dir=dist",
        f"--output-filename={exe_name}",
        script_name
    ]

    result = subprocess.run(compile_command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[-] Compilation failed: {result.stderr}")
        return

    build_path = f"dist/{exe_name}"
    final_path = os.path.join(OUTPUT_DIR, exe_name)

    if os.path.exists(build_path):
        shutil.move(build_path, final_path)
        print(f"[+] Compiled EXE saved to: {final_path}")
    else:
        print("[-] Compilation failed.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python comp_nuitka.py <script_name> <exe_name>")
        sys.exit(1)
    compile_to_exe(sys.argv[1], sys.argv[2])
