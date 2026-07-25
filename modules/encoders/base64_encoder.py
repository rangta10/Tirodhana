import base64

def encode(payload):
    if isinstance(payload, str):
        payload = payload.encode('utf-8')
    return base64.b64encode(payload).decode('utf-8')

def decode(payload):
    try:
        decoded = base64.b64decode(payload)
        return decoded.decode('utf-8')
    except Exception as e:
        return f"[!] Decode error: {e}"
