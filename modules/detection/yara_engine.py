import os

YARA_RULES_FILE = 'yara_rules.yar'

def _load_yara():
    try:
        import yara
        return yara
    except ImportError:
        return None

def scan_payload(payload, rules_file=YARA_RULES_FILE):
    yara = _load_yara()
    if not yara:
        return {'error': 'yara-python not installed. Run: pip3 install yara-python --break-system-packages'}

    if not os.path.exists(rules_file):
        return {'error': f'Rules file not found: {rules_file}'}

    try:
        rules   = yara.compile(filepath=rules_file)
        matches = rules.match(data=payload.encode() if isinstance(payload, str) else payload)

        results = []
        for match in matches:
            results.append({
                'rule':        match.rule,
                'tags':        match.tags,
                'meta':        match.meta,
                'strings':     [(s.identifier, s.instances[0].plaintext().decode('utf-8', errors='ignore'))
                                for s in match.strings if s.instances],
            })

        return {
            'detected': len(results) > 0,
            'matches':  results,
            'count':    len(results),
        }
    except Exception as e:
        return {'error': str(e)}

def yara_compare(original, variants, rules_file=YARA_RULES_FILE):
    all_payloads = [('Original', original)] + variants
    results = []
    for label, payload in all_payloads:
        r = scan_payload(payload, rules_file)
        if 'error' in r:
            results.append({'label': label, 'error': r['error']})
        else:
            results.append({
                'label':    label,
                'detected': r['detected'],
                'count':    r['count'],
                'rules':    [m['rule'] for m in r['matches']],
            })
    return results

def display_yara_results(results):
    print(f"\n  [YARA Scan Results]")
    print(f"  {'─'*50}")
    print(f"  {'Variant':<20} {'Status':<16} {'Rules Matched'}")
    print(f"  {'─'*50}")
    for r in results:
        if 'error' in r:
            print(f"  {r['label']:<20} ERROR: {r['error']}")
        else:
            status = "DETECTED" if r['detected'] else "NOT DETECTED"
            rules  = ', '.join(r['rules']) if r['rules'] else 'none'
            print(f"  {r['label']:<20} {status:<16} {rules}")
    print()
