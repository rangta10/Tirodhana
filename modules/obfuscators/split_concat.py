def obfuscate(payload, chunk_size=3):
    chunks = [payload[i:i+chunk_size] for i in range(0, len(payload), chunk_size)]
    result = '+'.join(f'"{c}"' for c in chunks)
    return result

def deobfuscate(payload):
    parts = payload.split('+')
    return ''.join(p.strip().strip('"') for p in parts)
