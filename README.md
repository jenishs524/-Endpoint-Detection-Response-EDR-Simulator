📁 Endpoint Detection & Response (EDR) Simulator

Description
Simulates an EDR by monitoring running processes, detecting suspicious command-line patterns (e.g., powershell -e, nmap, mimikatz), and displaying alerts on a live dashboard.

Key Features

    Uses psutil to enumerate processes.

    Regex‑based detection rules.

    Alerts appear in the terminal and on a Flask dashboard.

    Rules are extensible.

Technologies

    psutil, Flask, Jinja2.

Prerequisites

    Python 3, psutil, flask.

Installation
bash

pip install psutil flask jinja2

Usage

    Run the dashboard (which starts the monitor):
    bash

python dashboard_edr.py

Open http://127.0.0.1:5000 to see alerts.

Trigger a test alert:
bash

nmap localhost

Sample Output
Dashboard shows:
text

2026-07-09T20:27:41.186193  Network Scanner (nmap) (PID 12345)
/usr/bin/nmap localhost

Notes

    The detection rules are defined in SUSPICIOUS_PATTERNS in edr_sim.py.
