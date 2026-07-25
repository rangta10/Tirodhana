import json, os
from datetime import datetime

SESSIONS_DIR = 'sessions'

class Session:
    def __init__(self):
        self.reset()

    def reset(self):
        self.payload             = None
        self.payload_file        = None
        self.encoder_name        = None
        self.obfuscator_name     = None
        self.key                 = None
        self.encoded_payload     = None
        self.obfuscated_payload  = None
        self.detection_results   = []
        self.reports             = []

    def to_dict(self):
        return {
            'payload':            self.payload,
            'payload_file':       self.payload_file,
            'encoder':            self.encoder_name,
            'obfuscator':         self.obfuscator_name,
            'key':                self.key,
            'encoded_payload':    self.encoded_payload,
            'obfuscated_payload': self.obfuscated_payload,
            'detection_results':  self.detection_results,
            'reports':            self.reports,
        }

    def save(self, name):
        os.makedirs(SESSIONS_DIR, exist_ok=True)
        path = os.path.join(SESSIONS_DIR, f'{name}.json')
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"[+] Session saved: {path}")

    def load(self, name):
        path = os.path.join(SESSIONS_DIR, f'{name}.json')
        if not os.path.exists(path):
            print(f"[-] Session not found: {path}")
            return False
        with open(path, 'r') as f:
            data = json.load(f)
        self.payload             = data.get('payload')
        self.payload_file        = data.get('payload_file')
        self.encoder_name        = data.get('encoder')
        self.obfuscator_name     = data.get('obfuscator')
        self.key                 = data.get('key')
        self.encoded_payload     = data.get('encoded_payload')
        self.obfuscated_payload  = data.get('obfuscated_payload')
        self.detection_results   = data.get('detection_results', [])
        self.reports             = data.get('reports', [])
        print(f"[+] Session loaded: {path}")
        return True

    def show(self):
        print("\n  [Current Session]")
        print(f"  Payload file : {self.payload_file or 'None'}")
        print(f"  Payload      : {(self.payload or 'None')[:60]}")
        print(f"  Encoder      : {self.encoder_name or 'None'}")
        print(f"  Obfuscator   : {self.obfuscator_name or 'None'}")
        print(f"  Key          : {self.key or 'None'}")
        print(f"  Encoded      : {(self.encoded_payload or 'None')[:60]}")
        print(f"  Obfuscated   : {(self.obfuscated_payload or 'None')[:60]}")
        print(f"  Tests run    : {len(self.detection_results)}")
        print()
