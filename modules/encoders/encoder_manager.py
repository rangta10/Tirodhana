from modules.encoders import base64_encoder, xor_encoder, rot13_encoder

ENCODERS = {
    'base64': base64_encoder,
    'xor':    xor_encoder,
    'rot13':  rot13_encoder,
}

class EncoderManager:
    def __init__(self):
        self.active = None
        self.name   = None

    def list_encoders(self):
        print("\n  Available Encoders")
        print("  " + "-"*20)
        for name in ENCODERS:
            marker = " <-- active" if name == self.name else ""
            print(f"  [{name}]{marker}")
        print()

    def select(self, name):
        if name in ENCODERS:
            self.active = ENCODERS[name]
            self.name   = name
            print(f"[+] Encoder set to: {name}")
        else:
            print(f"[-] Unknown encoder: {name}")

    def run(self, payload, key=None):
        if not self.active:
            print("[-] No encoder selected. Use: use encoder <name>")
            return None
        if self.name == 'xor':
            if not key:
                print("[-] XOR needs a key. Use: set key <yourkey>")
                return None
            result = self.active.encode(payload, key)
        else:
            result = self.active.encode(payload)
        return result

    def decode(self, payload, key=None):
        if not self.active:
            print("[-] No encoder selected.")
            return None
        if self.name == 'xor':
            if not key:
                print("[-] XOR needs a key.")
                return None
            return self.active.decode(payload, key)
        return self.active.decode(payload)
