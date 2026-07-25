import os
import json
from datetime import datetime

REPORTS_DIR = 'reports'

def _next_report_name():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    existing = [f for f in os.listdir(REPORTS_DIR) if f.startswith('report_')]
    return os.path.join(REPORTS_DIR, f'report_{len(existing)+1:03d}.txt')

def generate(session):
    path     = _next_report_name()
    now      = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    payload  = session.get('payload', 'N/A')
    encoder  = session.get('encoder', 'None')
    obf      = session.get('obfuscator', 'None')
    key      = session.get('key', 'N/A')
    encoded  = session.get('encoded_payload', 'N/A')
    obfed    = session.get('obfuscated_payload', 'N/A')
    results  = session.get('detection_results', [])

    detected_count   = sum(1 for r in results if r['detected'])
    undetected_count = len(results) - detected_count
    bypass_rate      = round((undetected_count / len(results)) * 100, 2) if results else 0

    lines = [
        "=" * 54,
        "  Payload Obfuscation & Encoding Framework",
        "  Detection Report",
        "=" * 54,
        f"  Generated : {now}",
        "",
        "  [PAYLOAD]",
        f"  Original  : {payload}",
        f"  Encoder   : {encoder}",
        f"  Key       : {key}",
        f"  Obfuscator: {obf}",
        "",
        "  [TRANSFORMED PAYLOADS]",
        f"  Encoded   : {encoded}",
        f"  Obfuscated: {obfed}",
        "",
        "  [DETECTION RESULTS]",
    ]

    for r in results:
        status = "DETECTED" if r['detected'] else "NOT DETECTED"
        lines.append(f"  {r['label']:<18} {status:<15} (score: {r['score']}%)")
        if r['matched']:
            lines.append(f"    Matched sigs: {', '.join(r['matched'])}")

    lines += [
        "",
        "  [STATISTICS]",
        f"  Total Variants  : {len(results)}",
        f"  Detected        : {detected_count}",
        f"  Undetected      : {undetected_count}",
        f"  Bypass Rate     : {bypass_rate}%",
        "",
        "  [OBSERVATIONS]",
    ]

    if bypass_rate == 100:
        lines.append("  All variants bypassed detection successfully.")
    elif bypass_rate > 50:
        lines.append("  Majority of variants bypassed static detection.")
    elif bypass_rate > 0:
        lines.append("  Some variants bypassed detection — refine further.")
    else:
        lines.append("  No variants bypassed detection — try different methods.")

    lines.append("=" * 54)

    content = '\n'.join(lines)
    with open(path, 'w') as f:
        f.write(content)

    print(content)
    print(f"\n[+] Report saved: {path}")
    return path
