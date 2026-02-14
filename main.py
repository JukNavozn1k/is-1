import json
import socket
import uuid
import hashlib
import sys
from pathlib import Path
import re


def get_computer_identifier():
    hostname = socket.gethostname()
    mac_int = uuid.getnode()
    mac_hex = format(mac_int, '012x')
    mac_addr = ':'.join(mac_hex[i:i+2] for i in range(0, 12, 2))
    return f"{hostname}-{mac_addr}"


def compute_license_for(device_id: str) -> str:
    h = hashlib.sha256()
    h.update(device_id.encode('utf-8'))
    return h.hexdigest()


def load_license(license_path: Path):
    with license_path.open('r', encoding='utf-8') as f:
        return json.load(f)


def license_valid(license_path: Path) -> bool:
    try:
        data = load_license(license_path)
        stored_key = data.get('license_key')
        if not stored_key:
            return False
        current_id = get_computer_identifier()
        current_key = compute_license_for(current_id)
        return stored_key == current_key
    except Exception:
        return False


def simple_calculator():
    print('Protected app started — simple calculator.')
    print('Enter arithmetic expressions (e.g. 2+2) or "exit" to quit.')
    allowed = re.compile(r'^[0-9+\-*/(). \t]+$')
    while True:
        s = input('> ').strip()
        if not s:
            continue
        if s.lower() in ('exit', 'quit'):
            print('Goodbye')
            break
        if not allowed.match(s):
            print('Invalid characters in expression.')
            continue
        try:
            # limited eval of arithmetic expressions
            result = eval(s, {'__builtins__': None}, {})
            print(result)
        except Exception as e:
            print('Error evaluating expression:', e)


def main():
    license_path = Path(__file__).parent / 'license.key'
    if not license_path.exists():
        print('License error: license.key not found.')
        sys.exit(1)

    if not license_valid(license_path):
        print('License error: license is invalid for this computer.')
        sys.exit(1)

    # License OK — run protected functionality
    simple_calculator()


if __name__ == '__main__':
    main()
