# Tirodhana

> **Veiling Form, Preserving Essence**

Tirodhana is a modular payload transformation framework designed to demonstrate how different encoding and string obfuscation techniques affect static signature-based detection. It provides an interactive CLI for applying transformations, testing detection, generating reports, and analyzing payloads.

> **Disclaimer**
> This project is intended **strictly for educational, research, malware analysis, and defensive security purposes**. It is designed to help understand payload transformations and evaluate simple detection techniques. Do **not** use this tool for unauthorized or malicious activities.

---

## Features

- Interactive command-line interface
- Modular encoder architecture
- Modular obfuscation engine
- Payload loading and saving
- Static signature detection comparison
- YARA rule scanning
- String extraction from binaries
- Report generation
- Session save/load support
- Command-line automation support

---

## Supported Encoders

- Base64
- XOR (custom key)
- ROT13

Additional encoders can be added through the encoder module.

---

## Supported Obfuscators

- Random Insert
- Split & Concat
- Escape Characters
- Reverse String

The framework is designed so new obfuscators can easily be integrated.

---

## Detection Engine

Tirodhana compares the original payload with transformed variants using:

- Signature-based detection
- Detection score comparison
- Matched signatures display
- Detection statistics

---

## YARA Integration

The framework supports scanning payloads using YARA rules.

Features include:

- Rule matching
- Comparison of transformed payloads
- Human-readable output

---

## PE / ELF Analysis

Includes utilities for:

- Extracting printable strings
- Viewing embedded strings
- Basic binary inspection

---

## Report Generation

Automatically generates reports containing:

- Selected encoder
- Selected obfuscator
- Payload information
- Detection results
- Transformation summary

---

# Installation

Clone the repository

```bash
git clone https://github.com/rangta10/Tirodhana.git

cd Tirodhana
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python tirodhana.py
```

---

# Interactive Commands

## General

```
help
exit
quit
back
```

## Payload

```
load payload <file>

show payload

save payload <file>
```

## Encoders

```
show encoders

use encoder base64

use encoder xor

use encoder rot13
```

## Obfuscators

```
show obfuscators

use obfuscator random_insert

use obfuscator split_concat

use obfuscator escape

use obfuscator reverse
```

## XOR

```
set key mysecret
```

## Processing

```
run
```

## Detection

```
test

show results
```

## YARA

```
yara
```

## Reports

```
report
```

## Sessions

```
save session mysession

load session mysession

reset
```

## String Extraction

```
strings

strings sample.exe
```

---

# Command Line Mode

Instead of interactive mode, Tirodhana can execute directly from the command line.

Example:

```bash
python tirodhana.py \
    --payload payload.txt \
    --encoder xor \
    --key secret \
    --obfuscator reverse \
    --test \
    --report \
    --save-payload output.txt
```

Available options

| Argument | Description |
|----------|-------------|
| `--payload` | Payload file |
| `--encoder` | Encoder to use |
| `--obfuscator` | Obfuscator to use |
| `--key` | XOR key |
| `--test` | Run detection |
| `--report` | Generate report |
| `--save-payload` | Save processed payload |

---

# Project Structure

```
Tirodhana/

├── modules/
│   ├── encoders/
│   ├── obfuscators/
│   ├── detection/
│   ├── reports/
│   └── session.py
│
├── reports/
├── payloads/
├── tirodhana.py
├── requirements.txt
└── README.md
```

---

# Example Workflow

```
load payload payload.txt

use encoder xor

set key secret123

use obfuscator reverse

run

test

report

save payload encoded_payload.txt
```

---

# Design Goals

- Modular architecture
- Easily extensible
- Educational
- Research-oriented
- Simple CLI
- Lightweight
- Easy to integrate with new encoders and obfuscators

---

# Future Improvements

- AES encoder
- Multi-layer encoding
- Custom YARA rule management
- Entropy analysis
- Binary payload support
- Plugin system
- Additional reporting formats
- More obfuscation techniques

---

# Technologies Used

- Python 3
- Colorama
- YARA
- Object-Oriented Design

---

# Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Submit a Pull Request

---

# License

This project is intended for educational and research purposes.

Users are responsible for ensuring that their use complies with all applicable laws and regulations.

---

## Author

**Annanay Rangta**

**Project:** Tirodhana – *Veiling Form, Preserving Essence*
