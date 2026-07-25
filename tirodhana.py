import os
import sys

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    OK    = Fore.GREEN  + "[+]" + Style.RESET_ALL
    INFO  = Fore.CYAN   + "[*]" + Style.RESET_ALL
    ERR   = Fore.RED    + "[-]" + Style.RESET_ALL
    WARN  = Fore.YELLOW + "[!]" + Style.RESET_ALL
except ImportError:
    OK = "[+]"; INFO = "[*]"; ERR = "[-]"; WARN = "[!]"

from modules.encoders.encoder_manager       import EncoderManager
from modules.obfuscators.obfuscator_manager import ObfuscatorManager
from modules.detection.signature_engine     import detect, compare
from modules.reports.report_generator       import generate
from modules.session                        import Session
from modules.detection.pe_elf_extractor     import extract_and_display
from modules.detection.yara_engine          import scan_payload, yara_compare, display_yara_results

session  = Session()
enc_mgr  = EncoderManager()
obf_mgr  = ObfuscatorManager()

BANNER = """
 ▄▄▄█████▓ ██▓ ██▀███   ▒█████  ▓█████▄  ██░ ██  ▄▄▄       ███▄    █  ▄▄▄
 ▓  ██▒ ▓▒▓██▒▓██ ▒ ██▒▒██▒  ██▒▒██▀ ██▌▓██░ ██▒▒████▄     ██ ▀█   █ ▒████▄
 ▒ ▓██░ ▒░▒██▒▓██ ░▄█ ▒▒██░  ██▒░██   █▌▒██▀▀██░▒██  ▀█▄  ▓██  ▀█ ██▒▒██  ▀█▄
 ░ ▓██▓ ░ ░██░▒██▀▀█▄  ▒██   ██░░▓█▄   ▌░▓█ ░██ ░██▄▄▄▄██ ▓██▒  ▐▌██▒░██▄▄▄▄██
   ▒██▒ ░ ░██░░██▓ ▒██▒░ ████▓▒░░▒████▓ ░▓█▒░██▓ ▓█   ▓██▒▒██░   ▓██░ ▓█   ▓██▒
   ▒ ░░   ░▓  ░ ▒▓ ░▒▓░░ ▒░▒░▒░  ▒▒▓  ▒  ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▒░   ▒ ▒  ▒▒   ▓▒█░
     ░     ▒ ░  ░▒ ░ ▒░  ░ ▒ ▒░  ░ ▒  ▒  ▒ ░▒░ ░  ▒   ▒▒ ░░ ░░   ░ ▒░  ▒   ▒▒ ░
   ░       ▒ ░  ░░   ░ ░ ░ ░ ▒   ░ ░  ░  ░  ░░ ░  ░   ▒      ░   ░ ░   ░   ▒
           ░     ░         ░ ░     ░     ░  ░  ░      ░  ░         ░       ░  ░


                    Veiling Form, Preserving Essence

================================================================================
                          Type 'help' for commands
================================================================================
"""

HELP = """
  Commands:
  -------------------------------------------------
  help                      show this menu
  show encoders             list available encoders
  show obfuscators          list available obfuscators
  show payload              display loaded payload
  show options              display session options
  show results              display detection results
  strings [file]            extract strings from payload or file

  load payload <file>       load a payload file
  use encoder <name>        select encoder
  use obfuscator <name>     select obfuscator
  set key <value>           set XOR key

  run                       run encoder + obfuscator
  test                      run detection on all variants
  report                    generate and save report
  yara                      scan payload with YARA rules

  save payload <file>       save final processed payload to file
  save session <name>       save current session
  load session <name>       load a saved session
  reset                     clear session

  back                      return to main prompt
  exit / quit               exit framework
  -------------------------------------------------
"""

def get_prompt():
    parts = ["Tirodhana"]
    if enc_mgr.name:
        parts.append(f"encoder({enc_mgr.name})")
    if obf_mgr.name:
        parts.append(f"obfuscator({obf_mgr.name})")
    return " > ".join(parts) + " > "

def cmd_load_payload(args):
    if not args:
        print(f"{ERR} Usage: load payload <filepath>")
        return
    path = args[0]
    if not os.path.exists(path):
        print(f"{ERR} File not found: {path}")
        return

    # ── FIX: try UTF-8 first, fall back to latin-1 for binary/non-UTF files ──
    content = None
    for encoding in ('utf-8', 'latin-1', 'cp1252'):
        try:
            with open(path, 'r', encoding=encoding) as f:
                content = f.read().strip()
            break
        except (UnicodeDecodeError, LookupError):
            continue

    if content is None:
        # Last resort: read as bytes and represent as escaped string
        with open(path, 'rb') as f:
            raw = f.read()
        content = raw.decode('latin-1')
        print(f"{WARN} Binary/non-UTF-8 file detected — loaded with latin-1 encoding")

    session.payload      = content
    session.payload_file = path
    print(f"{OK} Payload loaded")
    print(f"{INFO} File   : {path}")
    print(f"{INFO} Length : {len(content)} bytes")
    print(f"{INFO} Preview: {content[:80]}")

def cmd_save_payload(args):
    """Save the final processed payload (obfuscated > encoded > raw) to a file."""
    if not args:
        print(f"{ERR} Usage: save payload <filepath>")
        return

    # Priority: obfuscated → encoded → original
    if session.obfuscated_payload:
        data    = session.obfuscated_payload
        variant = "obfuscated"
    elif session.encoded_payload:
        data    = session.encoded_payload
        variant = "encoded"
    elif session.payload:
        data    = session.payload
        variant = "original (no encoding/obfuscation applied yet)"
    else:
        print(f"{ERR} No payload in session. Load one first with: load payload <file>")
        return

    out_path = args[0]
    try:
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else '.', exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(data)
        print(f"{OK} Payload saved ({variant})")
        print(f"{INFO} File   : {out_path}")
        print(f"{INFO} Length : {len(data)} bytes")
    except OSError as e:
        print(f"{ERR} Could not write file: {e}")

def cmd_run():
    if not session.payload:
        print(f"{ERR} No payload loaded. Use: load payload <file>")
        return

    working = session.payload

    if enc_mgr.active:
        print(f"{INFO} Running encoder: {enc_mgr.name}")
        result = enc_mgr.run(working, session.key)
        if result:
            session.encoded_payload = result
            working = result
            print(f"{OK} Encoded: {result[:80]}")
        else:
            return
    else:
        print(f"{WARN} No encoder selected — skipping encoding")

    if obf_mgr.active:
        print(f"{INFO} Running obfuscator: {obf_mgr.name}")
        result = obf_mgr.run(working)
        if result:
            session.obfuscated_payload = result
            print(f"{OK} Obfuscated: {result[:80]}")
        else:
            return
    else:
        print(f"{WARN} No obfuscator selected — skipping obfuscation")

def cmd_test():
    if not session.payload:
        print(f"{ERR} No payload loaded.")
        return

    variants = []
    if session.encoded_payload:
        variants.append((enc_mgr.name or 'Encoded', session.encoded_payload))
    if session.obfuscated_payload:
        variants.append((obf_mgr.name or 'Obfuscated', session.obfuscated_payload))

    results = compare(session.payload, variants)
    session.detection_results = results

    print(f"\n  {'Variant':<20} {'Status':<16} {'Score'}")
    print("  " + "-" * 48)
    for r in results:
        status = "DETECTED" if r['detected'] else "NOT DETECTED"
        print(f"  {r['label']:<20} {status:<16} {r['score']}%")
        if r['matched']:
            print(f"    Matched: {', '.join(r['matched'])}")
    print()

def cmd_report():
    if not session.detection_results:
        print(f"{WARN} Run 'test' first to generate detection results.")
        return
    data = {
        'payload':            session.payload,
        'encoder':            session.encoder_name or enc_mgr.name,
        'obfuscator':         session.obfuscator_name or obf_mgr.name,
        'key':                session.key,
        'encoded_payload':    session.encoded_payload,
        'obfuscated_payload': session.obfuscated_payload,
        'detection_results':  session.detection_results,
    }
    path = generate(data)
    session.reports.append(path)

def run():
    print(BANNER)
    while True:
        try:
            raw = input(get_prompt()).strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{INFO} Exiting.")
            sys.exit(0)

        if not raw:
            continue

        tokens  = raw.split()
        command = tokens[0].lower()
        args    = tokens[1:]

        if command in ('exit', 'quit'):
            print(f"{INFO} Goodbye.")
            break

        elif command == 'help':
            print(HELP)

        elif command == 'show':
            if not args:
                print(f"{ERR} Usage: show <encoders|obfuscators|payload|options|results>")
            elif args[0] == 'encoders':
                enc_mgr.list_encoders()
            elif args[0] == 'obfuscators':
                obf_mgr.list_obfuscators()
            elif args[0] == 'payload':
                if session.payload:
                    print(f"\n{INFO} {session.payload}\n")
                else:
                    print(f"{ERR} No payload loaded.")
            elif args[0] == 'options':
                session.show()
            elif args[0] == 'results':
                if session.detection_results:
                    for r in session.detection_results:
                        status = "DETECTED" if r['detected'] else "NOT DETECTED"
                        print(f"  {r['label']:<20} {status}")
                else:
                    print(f"{WARN} No results yet. Run 'test' first.")

        elif command == 'load':
            if len(args) >= 2 and args[0] == 'payload':
                cmd_load_payload([args[1]])
            elif len(args) >= 2 and args[0] == 'session':
                session.load(args[1])
            else:
                print(f"{ERR} Usage: load payload <file>  OR  load session <name>")

        elif command == 'use':
            if len(args) < 2:
                print(f"{ERR} Usage: use encoder <name>  OR  use obfuscator <name>")
            elif args[0] == 'encoder':
                enc_mgr.select(args[1])
                session.encoder_name = args[1]
            elif args[0] == 'obfuscator':
                obf_mgr.select(args[1])
                session.obfuscator_name = args[1]

        elif command == 'set':
            if len(args) >= 2 and args[0] == 'key':
                session.key = args[1]
                print(f"{OK} Key set to: {args[1]}")
            else:
                print(f"{ERR} Usage: set key <value>")

        elif command == 'run':
            cmd_run()

        elif command == 'test':
            cmd_test()

        elif command == 'report':
            cmd_report()

        elif command == 'save':
            if len(args) >= 2 and args[0] == 'payload':
                cmd_save_payload([args[1]])
            elif len(args) >= 2 and args[0] == 'session':
                session.save(args[1])
            else:
                print(f"{ERR} Usage: save payload <file>  OR  save session <name>")

        elif command == 'reset':
            session.reset()
            enc_mgr.active = None
            enc_mgr.name = None
            obf_mgr.active = None
            obf_mgr.name = None
            print(f"{OK} Session reset.")

        elif command == 'yara':
            if not session.payload_file:
                print(f"{ERR} Load a payload first.")
            else:
                with open(session.payload_file, 'r', encoding='latin-1') as _f:
                    _data = _f.read()
                results = yara_compare(_data, [])
                display_yara_results(results)

        elif command == 'strings':
            if not args:
                if session.payload_file:
                    extract_and_display(session.payload_file)
                else:
                    print(f"{ERR} Usage: strings <filepath> OR load a payload first")
            else:
                extract_and_display(args[0])

        elif command == 'back':
            print(f"{INFO} Already at main prompt.")

        else:
            print(f"{ERR} Unknown command: '{command}'. Type 'help'.")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Tirodhana - Veiling Form, Preserving Essence'
    )
    parser.add_argument('--payload',        type=str, help='Path to payload file')
    parser.add_argument('--encoder',        type=str, help='Encoder to use: base64, xor, rot13')
    parser.add_argument('--obfuscator',     type=str, help='Obfuscator: random_insert, split_concat, escape, reverse')
    parser.add_argument('--key',            type=str, help='XOR key')
    parser.add_argument('--test',           action='store_true', help='Run evasion test')
    parser.add_argument('--report',         action='store_true', help='Generate report')
    parser.add_argument('--save-payload',   type=str, metavar='FILE', help='Save final processed payload to file')

    args = parser.parse_args()

    if args.payload:
        print(BANNER)
        cmd_load_payload([args.payload])
        if args.encoder:
            enc_mgr.select(args.encoder)
            session.encoder_name = args.encoder
        if args.key:
            session.key = args.key
        if args.obfuscator:
            obf_mgr.select(args.obfuscator)
            session.obfuscator_name = args.obfuscator
        cmd_run()
        if args.test:
            cmd_test()
        if args.report:
            cmd_report()
        if args.save_payload:
            cmd_save_payload([args.save_payload])
    else:
        run()
