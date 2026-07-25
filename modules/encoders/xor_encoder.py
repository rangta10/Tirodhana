def encode(payload, key):
    if isinstance(payload, str):
        payload = payload.encode('utf-8')
    if isinstance(key, str):
        key = key.encode('utf-8')
    xored = bytes([payload[i] ^ key[i % len(key)] for i in range(len(payload))])
    return xored.hex()

def decode(payload_hex, key):
    try:
        payload = bytes.fromhex(payload_hex)
        if isinstance(key, str):
            key = key.encode('utf-8')
        decoded = bytes([payload[i] ^ key[i % len(key)] for i in range(len(payload))])
        return decoded.decode('utf-8')
    except Exception as e:
        return f"[!] Decode error: {e}"
