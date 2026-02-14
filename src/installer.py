import argparse
import json
import socket
import uuid
import hashlib
from pathlib import Path


def get_computer_identifier():
    hostname = socket.gethostname()
    mac_int = uuid.getnode()
    mac_hex = format(mac_int, '012x')
    mac_addr = ':'.join(mac_hex[i:i+2] for i in range(0, 12, 2))
    return f"{hostname}-{mac_addr}"


def generate_license_for(device_id: str) -> str:
    h = hashlib.sha256()
    h.update(device_id.encode('utf-8'))
    return h.hexdigest()


def write_license_file(out_path: Path, device_id: str, license_key: str):
    payload = {"device_id": device_id, "license_key": license_key}
    with out_path.open('w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Installer: generate license.key for this machine')
    parser.add_argument('--out-dir', '-o', default='.', help='Directory to place license.key (default: current dir)')
    args = parser.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    device_id = get_computer_identifier()
    license_key = generate_license_for(device_id)

    license_path = out_dir / 'license.key'
    write_license_file(license_path, device_id, license_key)

    print(f'License generated and written to: {license_path}')
    print('Device identifier:')
    print(device_id)
    print('License key (SHA-256):')
    print(license_key)


if __name__ == '__main__':
    main()
