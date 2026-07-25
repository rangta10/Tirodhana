import os

DEFAULT_SIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'signatures.txt')

def load_signatures(path=DEFAULT_SIG_FILE):
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return [line.strip().lower() for line in f if line.strip()]

def detect(payload, signatures=None):
    if signatures is None:
        signatures = load_signatures()
    payload_lower = payload.lower()
    matched = [sig for sig in signatures if sig in payload_lower]
    total = len(signatures)
    score = round((len(matched) / total) * 100, 1) if total > 0 else 0.0
    return {
        'detected': len(matched) > 0,
        'matched': matched,
        'score': score
    }

def compare(payload, variants):
    signatures = load_signatures()
    results = []
    original = detect(payload, signatures)
    results.append({
        'label': 'Original',
        'detected': original['detected'],
        'matched': original['matched'],
        'score': original['score']
    })
    for label, variant in variants:
        r = detect(variant, signatures)
        results.append({
            'label': label,
            'detected': r['detected'],
            'matched': r['matched'],
            'score': r['score']
        })
    return results
