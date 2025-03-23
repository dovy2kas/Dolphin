import os
import subprocess
import sys
import shutil

OUTPUT_DIR = "compiled_payloads"

def compile_to_exe_with_docker(script_name, exe_name):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    output_path = os.path.join(OUTPUT_DIR, exe_name)
    if os.path.exists(output_path):
        os.remove(output_path)

    print(f"[+] Compiling {script_name} to {exe_name} using Docker...")
    
    client_dir = os.path.abspath(os.path.dirname(__file__))
    print(f"[+] Using volume path: {client_dir}")

    docker_command = f'docker run --rm --volume {client_dir}:/src/:z batonogov/pyinstaller-windows:latest "pip install requests; pyinstaller --onefile --hidden-import=requests --collect-all requests --add-data "python-embed;python-embed" --name {exe_name} {script_name}"'

    try:
        result = subprocess.run(docker_command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
           print(f"[-] Compilation failed:\n{result.stderr}")
           sys.exit(1)

        build_path = f"{client_dir}/dist/{exe_name}"
        final_path = f"{client_dir}/../compiled_payloads/{exe_name}"

        if os.path.exists(build_path):
            shutil.move(build_path, final_path)
            print(f"[+] Compiled EXE saved to: {final_path}")
            sys.exit(0)
        else:
            print("[-] Compilation failed: EXE not found in dist/")
            sys.exit(1)

    except Exception as e:
        print(f"[-] Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compiler.py <script_name> <exe_name>")
        sys.exit(1)

    script_name = sys.argv[1]
    exe_name = sys.argv[2]
    
    compile_to_exe_with_docker(script_name, exe_name)
