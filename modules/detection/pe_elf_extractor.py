import re
import os

MIN_STR_LEN = 4

def extract_strings(filepath):
    if not os.path.exists(filepath):
        return {'error': f'File not found: {filepath}', 'strings': []}

    with open(filepath, 'rb') as f:
        data = f.read()

    file_type = _detect_type(data)
    strings   = _extract_printable(data)

    return {
        'file':      filepath,
        'type':      file_type,
        'size':      len(data),
        'strings':   strings,
        'count':     len(strings),
    }

def _detect_type(data):
    if data[:2] == b'MZ':
        return 'PE (Windows Executable)'
    elif data[:4] == b'\x7fELF':
        return 'ELF (Linux Executable)'
    else:
        return 'Unknown / Text file'

def _extract_printable(data):
    pattern = rb'[ -~]{' + str(MIN_STR_LEN).encode() + rb',}'
    matches = re.findall(pattern, data)
    return [m.decode('ascii', errors='ignore') for m in matches]

def extract_and_display(filepath):
    result = extract_strings(filepath)
    if 'error' in result:
        print(f"[-] {result['error']}")
        return

    print(f"\n  [PE/ELF String Extractor]")
    print(f"  File : {result['file']}")
    print(f"  Type : {result['type']}")
    print(f"  Size : {result['size']} bytes")
    print(f"  Strings found: {result['count']}")
    print(f"  {'─'*40}")
    for s in result['strings'][:30]:
        print(f"  {s}")
    if result['count'] > 30:
        print(f"  ... and {result['count'] - 30} more strings")
    print()
    return result
