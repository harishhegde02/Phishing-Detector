import os
from pathlib import Path

def check_files(directory):
    for p in Path(directory).rglob('*.py'):
        print(f"Checking {p}...", end=" ")
        try:
            content = p.read_bytes()
            if b'\x00' in content:
                print("FAIL: Contains Null Bytes!")
            elif content.startswith(b'\xff\xfe') or content.startswith(b'\xfe\xff'):
                print("FAIL: Contains UTF-16 BOM!")
            else:
                p.read_text('utf-8')
                print("OK")
        except Exception as e:
            print(f"FAIL: {e}")

if __name__ == "__main__":
    check_files('backend')
    check_files('utils')
    check_files('scripts')
