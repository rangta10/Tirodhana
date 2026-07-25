from modules.obfuscators import (
    random_insert, split_concat,
    escape_obfuscator, reverse_transform
)

OBFUSCATORS = {
    'random_insert':   random_insert,
    'split_concat':    split_concat,
    'escape':          escape_obfuscator,
    'reverse':         reverse_transform,
}

class ObfuscatorManager:
    def __init__(self):
        self.active = None
        self.name   = None

    def list_obfuscators(self):
        print("\n  Available Obfuscators")
        print("  " + "-"*22)
        for name in OBFUSCATORS:
            marker = " <-- active" if name == self.name else ""
            print(f"  [{name}]{marker}")
        print()

    def select(self, name):
        if name in OBFUSCATORS:
            self.active = OBFUSCATORS[name]
            self.name   = name
            print(f"[+] Obfuscator set to: {name}")
        else:
            print(f"[-] Unknown obfuscator: {name}")

    def run(self, payload):
        if not self.active:
            print("[-] No obfuscator selected. Use: use obfuscator <name>")
            return None
        if self.name == 'random_insert':
            result, _ = self.active.obfuscate(payload)
        else:
            result = self.active.obfuscate(payload)
        return result
