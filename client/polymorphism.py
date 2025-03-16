import re
import random
import string

def random_string(length=8):
    first_char = random.choice(string.ascii_letters)
    rest = ''.join(random.choices(string.ascii_letters + string.digits, k=length - 1))
    return first_char + rest

def xor_encrypt(text, key):
    return ",".join(str(ord(char) ^ key) for char in text)

def add_decryption_function(code):
    decryptor = """
def decrypt_string(data, key):
    result = ''.join(chr(int(x) ^ key) for x in data.split(','))
    try:
        return eval(f"f'{result}'")  # Force evaluation as an f-string
    except:
        return result
"""
    return decryptor + code

def encrypt_strings(code):
    key = random.randint(1, 255)

    fstring_matches = re.findall(r'f\"(.*?)\"', code)
    normal_matches = re.findall(r'\"(.*?)\"', code)

    for string in fstring_matches:
        encrypted = xor_encrypt(string, key)
        decrypted = f'decrypt_string("{encrypted}", {key}).format(**locals())'
        code = code.replace(f'f"{string}"', decrypted)

    for string in normal_matches:
        if string not in fstring_matches:
            encrypted = xor_encrypt(string, key)
            decrypted = f'decrypt_string("{encrypted}", {key})'
            code = code.replace(f'"{string}"', decrypted)

    code = add_decryption_function(code)

    return code

def rename_functions(code):
    functions = re.findall(r'def (\w+)\(', code)
    mapping = {func: random_string() for func in functions}

    for old_func, new_func in mapping.items():
        code = re.sub(rf'def {old_func}\(', f'def {new_func}(', code)
        code = re.sub(rf'\b{old_func}\(', f'{new_func}(', code)

    return code

def generate_polymorphic_payload(input_path, output_path):
    with open(input_path, 'r') as f:
        code = f.read()

    code = rename_functions(code)

    code = encrypt_strings(code)

    with open(output_path, 'w') as f:
        f.write(code)

    print(f"[+] Polymorphic payload generated: {output_path}")

if __name__ == "__main__":
    input_path = 'main.py'
    output_path = 'polymorphic_payload.py'
    generate_polymorphic_payload(input_path, output_path)
