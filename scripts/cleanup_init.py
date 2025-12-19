import os
from pathlib import Path

def cleanup():
    for p in Path('backend').rglob('__init__.py'):
        try:
            os.remove(p)
            print(f"Removed {p}")
        except FileNotFoundError:
            pass
        
        with open(p, 'w', encoding='utf-8') as f:
            f.write("# init\n")
            print(f"Recreated {p}")

if __name__ == "__main__":
    cleanup()
