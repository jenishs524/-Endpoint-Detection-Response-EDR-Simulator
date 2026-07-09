#!/usr/bin/env python3
import psutil, time, re, threading
from datetime import datetime

SUSPICIOUS_PATTERNS = [
    (r'(?i)powershell.*-e', "PowerShell with Encoded Command"),
    (r'(?i)nmap', "Network Scanner (nmap)"),
    (r'(?i)netcat|nc', "Netcat (nc)"),
    (r'(?i)mimikatz', "Mimikatz"),
    (r'(?i)wget.*\|.*sh|curl.*\|.*sh', "Wget/Curl Pipe to Shell"),
    (r'(?i)sqlmap', "SQL Injection Scanner (sqlmap)"),
]

alerts = []
alert_lock = threading.Lock()

def check_process(proc):
    try:
        name = proc.name()
        cmdline = ' '.join(proc.cmdline())
        for pattern, desc in SUSPICIOUS_PATTERNS:
            if re.search(pattern, cmdline, re.IGNORECASE):
                alert = {
                    "timestamp": datetime.now().isoformat(),
                    "process": name,
                    "pid": proc.pid,
                    "cmdline": cmdline[:200],
                    "reason": desc
                }
                with alert_lock:
                    alerts.append(alert)
                    if len(alerts) > 100:
                        alerts.pop(0)
                print(f"[!] ALERT: {desc} (PID {proc.pid}) - {name}")
                break
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

def monitor():
    seen = set()
    print("[*] EDR monitor started. Press Ctrl+C to stop.")
    while True:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            pid = proc.info['pid']
            if pid not in seen:
                seen.add(pid)
                check_process(proc)
        time.sleep(2)

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        print("\n[*] EDR monitor stopped.")#!/usr/bin/env python3
"""
Project 28 – EDR Simulator (Engine)
Monitors running processes and alerts on suspicious patterns.
"""

import psutil
import time
import re
import threading
from datetime import datetime

# ---------- RULES: (regex pattern, description) ----------
SUSPICIOUS_PATTERNS = [
    (r'(?i)powershell.*-e', "PowerShell with Encoded Command"),
    (r'(?i)nmap', "Network Scanner (nmap)"),
    (r'(?i)netcat|nc', "Netcat (nc)"),
    (r'(?i)mimikatz', "Mimikatz"),
    (r'(?i)wget.*\|.*sh|curl.*\|.*sh', "Wget/Curl Pipe to Shell"),
    (r'(?i)sqlmap', "SQL Injection Scanner (sqlmap)"),
]

alerts = []
alert_lock = threading.Lock()

def check_process(proc):
    """Check a single process against all suspicious patterns."""
    try:
        name = proc.name()
        cmdline = ' '.join(proc.cmdline())
        for pattern, desc in SUSPICIOUS_PATTERNS:
            if re.search(pattern, cmdline, re.IGNORECASE):
                alert = {
                    "timestamp": datetime.now().isoformat(),
                    "process": name,
                    "pid": proc.pid,
                    "cmdline": cmdline[:200],
                    "reason": desc
                }
                with alert_lock:
                    alerts.append(alert)
                    if len(alerts) > 100:
                        alerts.pop(0)
                print(f"[!] ALERT: {desc} (PID {proc.pid}) - {name}")
                break  # avoid duplicate alerts for same process
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

def monitor():
    """Main monitoring loop – runs in a separate thread."""
    seen = set()
    print("[*] EDR monitor started. Press Ctrl+C to stop.")
    while True:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            pid = proc.info['pid']
            if pid not in seen:
                seen.add(pid)
                check_process(proc)
        time.sleep(2)

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        print("\n[*] EDR monitor stopped.")
