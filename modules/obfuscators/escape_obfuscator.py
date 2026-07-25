def obfuscate(payload):
    return ''.join(f'\\x{ord(c):02x}' for c in payload)

def deobfuscate(payload):
    try:
        return bytes.fromhex(payload.replace('\\x', '')).decode('utf-8')
    except Exception as e:
        return f"[!] Error: {e}"
