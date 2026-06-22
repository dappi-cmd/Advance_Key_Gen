#!/usr/bin/env python3
"""
Advance Key Generator - HTML Report Generator
Generates a beautiful HTML report with hardware info and license keys.
"""

import os
import sys
import datetime
import json

from hardware import HardwareDetector
from keygen import KeyGenerator


def _build_html(key_val, badge_type, license_type, hw_cards, timestamp, os_name):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advance Key Generator - Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #ffffff;
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: rgba(26, 26, 62, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(233, 69, 96, 0.3);
        }}
        .header {{
            text-align: center;
            padding-bottom: 30px;
            border-bottom: 2px solid rgba(233, 69, 96, 0.3);
            margin-bottom: 30px;
        }}
        .header .icon {{ font-size: 48px; }}
        .header h1 {{
            font-size: 28px;
            background: linear-gradient(135deg, #e94560, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 10px 0 5px;
        }}
        .header p {{ color: #8899aa; font-size: 14px; }}
        .key-section {{
            background: linear-gradient(135deg, #0a0a2e, #1a1a4e);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            margin-bottom: 30px;
            border: 2px solid rgba(0, 255, 136, 0.3);
        }}
        .key-section .label {{
            color: #8899aa; font-size: 12px;
            text-transform: uppercase; letter-spacing: 2px;
            margin-bottom: 10px;
        }}
        .key-section .key {{
            font-size: 36px; font-weight: bold;
            color: #00ff88; letter-spacing: 4px;
            font-family: 'Courier New', monospace;
            word-break: break-all;
        }}
        .key-section .badge {{
            display: inline-block; padding: 4px 12px;
            border-radius: 20px; font-size: 11px;
            font-weight: bold; margin-top: 10px;
        }}
        .badge-standard {{ background: #0f3460; color: #00ff88; }}
        .badge-enterprise {{ background: #e94560; color: #fff; }}
        .badge-trial {{ background: #ffcc00; color: #000; }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px; margin-bottom: 30px;
        }}
        .info-card {{
            background: rgba(15, 52, 96, 0.5);
            border-radius: 12px; padding: 20px;
            border: 1px solid rgba(42, 42, 94, 0.8);
            transition: transform 0.2s;
        }}
        .info-card:hover {{ transform: translateY(-3px); }}
        .info-card .card-icon {{ font-size: 24px; margin-bottom: 8px; }}
        .info-card .card-label {{
            color: #8899aa; font-size: 11px;
            text-transform: uppercase; letter-spacing: 1px;
            margin-bottom: 5px;
        }}
        .info-card .card-value {{ font-size: 14px; font-weight: bold; word-break: break-all; }}
        .info-card .card-value.ok {{ color: #00ff88; }}
        .info-card .card-value.na {{ color: #e94560; }}
        .footer {{
            text-align: center; padding-top: 20px;
            border-top: 1px solid rgba(42, 42, 94, 0.8);
            color: #556677; font-size: 12px;
        }}
        .timestamp {{
            text-align: right; color: #556677;
            font-size: 11px; margin-top: 10px;
        }}
        @media print {{
            body {{ background: #0f0c29; padding: 20px; }}
            .container {{ box-shadow: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="icon">&#x1F511;</div>
            <h1>Advance Key Generator</h1>
            <p>Hardware-based License Key Report</p>
        </div>

        <div class="key-section">
            <div class="label">Generated License Key</div>
            <div class="key">{key_val}</div>
            <span class="badge badge-{badge_type}">{license_type}</span>
        </div>

        <h2 style="color: #8899aa; font-size: 14px; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 2px;">
            &#x1F4CA; Hardware Fingerprint
        </h2>

        <div class="info-grid">
            {hw_cards}
        </div>

        <div class="footer">
            <p>&#x00A9; 2024 Advance Key Generator. All rights reserved.</p>
            <p>This key is uniquely tied to the hardware configuration above.</p>
        </div>
        <div class="timestamp">
            Generated: {timestamp} | System: {os_name}
        </div>
    </div>
</body>
</html>"""


def generate_report():
    print("=" * 50)
    print("  Advance Key Generator - HTML Report")
    print("=" * 50)

    print("\n[1/4] Detecting hardware...")
    hw = HardwareDetector()
    info = hw.get_all_info()

    print("[2/4] Generating keys...")
    kg = KeyGenerator()
    standard_key = kg.generate_license_key(info)
    enterprise_key = kg.generate_activation_code(info)
    trial_key = kg.generate_key(info, 8)

    print(f"  Standard  : {standard_key}")
    print(f"  Enterprise: {enterprise_key}")
    print(f"  Trial     : {trial_key}")

    print("[3/4] Generating HTML report...")

    import platform as pf
    os_name = pf.system()
    try:
        os_info = hw.get_os_info()
        os_name = f"{os_info[0]} v{os_info[1]}"
    except:
        pass

    icons = {
        "motherboard": "&#x1F4BB;",
        "ram": "&#x1F4BE;",
        "vga": "&#x1F5B5;",
        "hdd": "&#x1F4C0;",
        "windows_key": "&#x1F4CB;",
        "cpu": "&#x2699;",
        "mac": "&#x1F4F6;",
    }

    labels = {
        "motherboard": "Motherboard",
        "ram": "RAM Module",
        "vga": "Graphics Card",
        "hdd": "Hard Disk",
        "windows_key": "Windows Product Key",
        "cpu": "Processor ID",
        "mac": "MAC Address",
    }

    hw_cards = ""
    for key, label in labels.items():
        value = info.get(key, "N/A")
        is_ok = value and value != "N/A"
        status_class = "ok" if is_ok else "na"
        icon = icons.get(key, "&#x2753;")
        hw_cards += f"""
            <div class="info-card">
                <div class="card-icon">{icon}</div>
                <div class="card-label">{label}</div>
                <div class="card-value {status_class}">{value}</div>
            </div>"""

    print("[4/4] Writing report file...")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for key_name, key_val, badge_type, license_type in [
        ("standard_key", standard_key, "standard", "Standard (16 char)"),
        ("enterprise_key", enterprise_key, "enterprise", "Enterprise (25 char)"),
        ("trial_key", trial_key, "trial", "Trial (8 char)"),
    ]:
        html = _build_html(key_val, badge_type, license_type, hw_cards, timestamp, os_name)

        filename = f"report_{key_name}.html"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"  Created: {filename}")

    all_keys_html = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "report_all_keys.html"
    )
    all_keys = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All License Keys - Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #fff; min-height: 100vh; padding: 40px 20px;
        }}
        .container {{
            max-width: 700px; margin: 0 auto;
            background: rgba(26,26,62,0.95); border-radius: 20px;
            padding: 40px; box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            border: 1px solid rgba(233,69,96,0.3);
        }}
        h1 {{ text-align: center; font-size: 26px; margin-bottom: 30px;
            background: linear-gradient(135deg, #e94560, #ff6b6b);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .key-row {{
            background: rgba(15,52,96,0.5); border-radius: 12px;
            padding: 20px 25px; margin-bottom: 15px;
            border: 1px solid rgba(42,42,94,0.8);
        }}
        .key-row .type {{ color: #8899aa; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }}
        .key-row .value {{ font-family: 'Courier New', monospace; font-size: 22px; font-weight: bold; color: #00ff88; letter-spacing: 2px; margin-top: 5px; }}
        .footer {{ text-align: center; color: #556677; font-size: 12px; margin-top: 20px; }}
        .timestamp {{ text-align: right; color: #556677; font-size: 11px; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>&#x1F511; All Generated License Keys</h1>
        <div class="key-row">
            <div class="type">&#x1F538; Standard (16 char)</div>
            <div class="value">{standard_key}</div>
        </div>
        <div class="key-row">
            <div class="type">&#x1F537; Enterprise (25 char)</div>
            <div class="value">{enterprise_key}</div>
        </div>
        <div class="key-row">
            <div class="type">&#x1F539; Trial (8 char)</div>
            <div class="value">{trial_key}</div>
        </div>
        <div class="footer">&#x00A9; 2024 Advance Key Generator. All rights reserved.</div>
        <div class="timestamp">Generated: {timestamp} | {os_name}</div>
    </div>
</body>
</html>"""

    with open(all_keys_html, "w", encoding="utf-8") as f:
        f.write(all_keys)
    print(f"  Created: report_all_keys.html")

    print("\n" + "=" * 50)
    print("  DONE! Open the HTML files in your browser.")
    print("=" * 50)


if __name__ == "__main__":
    generate_report()
