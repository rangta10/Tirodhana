import random
import string
import itertools

def obfuscate(payload, char=None, freq=3):
    if char is None:
        char = random.choice(['^', '#', '$', '!', '@'])
    result = ''
    positions = []
    for i, c in enumerate(payload):
        result += c
        if (i + 1) % freq == 0 and i < len(payload) - 1:
            result += char
            positions.append(i + 1)
    return result, positions

def deobfuscate(payload, char, positions):
    result = list(payload)
    for p in sorted(positions, reverse=True):
        if result[p] == char:
            result.pop(p)
    return ''.join(result)

def generate_char_variants(payload, chars=None):
    if chars is None:
        chars = ['^', '#', '$', '!', '@']
    variants = []
    for char, freq in itertools.product(chars, [2, 3, 4]):
        result, positions = obfuscate(payload, char, freq)
        variants.append({
            'char': char,
            'freq': freq,
            'result': result,
            'positions': positions
        })
    return variants
