# Advance Key Generator v2.0

A professional desktop application for generating hardware-fingerprinted license keys with a modern dark-themed GUI.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![GUI](https://img.shields.io/badge/GUI-customtkinter-green) ![Build](https://img.shields.io/badge/Build-PyInstaller-orange)

## Overview

Advance Key Generator reads unique hardware identifiers from the user's PC (motherboard serial, RAM serial, GPU ID, HDD serial, Windows product key, CPU ID, MAC address), hashes them with the current date using SHA-256 + HMAC, and produces a secure, formatted license key. It is designed for software developers and vendors who need a hardware-bound licensing system.

## Features

- **Hardware Fingerprinting** — Reads WMI-based hardware IDs for strong device binding
- **Three Key Types** — Standard (16-char), Enterprise (25-char), Trial (8-char) license keys
- **Copy & Save** — Copy keys to clipboard or save as `.txt` files
- **SMS Delivery** — Send keys via TextBelt (free) or Fast2SMS (paid) APIs
- **HTML Reports** — Generate styled reports showing keys and hardware fingerprint
- **Modern GUI** — Dark-themed interface with 5 navigation views (Dashboard, Key Gen, SMS, Settings, About)
- **Standalone Executable** — Build a portable `.exe` with PyInstaller

## Tech Stack

| Component          | Technology                    |
|--------------------|-------------------------------|
| Language           | Python 3.12                   |
| GUI Framework      | customtkinter (Tkinter)       |
| Hardware Detection | WMI (pywin32/wmi) + winreg    |
| Key Generation     | SHA-256, HMAC, base64         |
| SMS APIs           | TextBelt, Fast2SMS            |
| Build Tool         | PyInstaller                   |

## Getting Started

### Prerequisites

- Python 3.12+
- Windows OS (hardware detection uses WMI)

### Installation

```bash
# Clone the repository
git clone https://github.com/WAPCC/Advance-Key-Gen.git
cd Advance-Key-Gen

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Run the GUI application
python main.py

# Generate HTML reports (standalone)
python generate_report.py
```

### Build Executable

```bash
.\build_exe.bat
```

The standalone `.exe` will be created in the `dist/` directory.

## Project Structure

```
Advance-Key-Gen/
├── main.py                 # Entry point
├── ui.py                   # GUI application (customtkinter)
├── keygen.py               # Key generation logic
├── hardware.py             # Hardware fingerprinting
├── sms.py                  # SMS sending module
├── generate_report.py      # HTML report generator
├── requirements.txt        # Python dependencies
├── AdvanceKeyGen.spec      # PyInstaller spec file
├── run.bat                 # Run script
└── build_exe.bat           # Build script
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Developer

**W.A.P.C.CHATHURANGA**

---

*Advance Key Generator v2.0 — Secure hardware-bound license key generation*
