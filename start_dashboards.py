#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Disable Streamlit telemetry
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

# EP2 Dashboard
print("🚀 Starting EP2 Dashboard on port 8501...")
ep2_cmd = [
    sys.executable, '-m', 'streamlit', 'run',
    r'Entregables_EP2\dashboard\dashboard_ep2_streamview.py',
    '--server.port=8501',
    '--logger.level=warning'
]

# EP3 Dashboard
print("🚀 Starting EP3 Dashboard on port 8502...")
ep3_cmd = [
    sys.executable, '-m', 'streamlit', 'run',
    r'Entregables_EP3\dashboard\dashboard_ep3_streamview.py',
    '--server.port=8502',
    '--logger.level=warning'
]

# Start both processes
p1 = subprocess.Popen(ep2_cmd, cwd=r'C:\Users\fabia\Downloads\Caso_Semestral_STREAMVIEW-ANALYTICS-main (1)\Caso_Semestral_STREAMVIEW-ANALYTICS-main')
print(f"✅ EP2 started (PID: {p1.pid})")

time.sleep(2)

p2 = subprocess.Popen(ep3_cmd, cwd=r'C:\Users\fabia\Downloads\Caso_Semestral_STREAMVIEW-ANALYTICS-main (1)\Caso_Semestral_STREAMVIEW-ANALYTICS-main')
print(f"✅ EP3 started (PID: {p2.pid})")

print("\n📊 Dashboards:")
print("   EP2 (ANTES): http://localhost:8501")
print("   EP3 (DESPUÉS): http://localhost:8502")
print("\n⏳ Press Ctrl+C to stop...")

try:
    p1.wait()
    p2.wait()
except KeyboardInterrupt:
    print("\n🛑 Stopping dashboards...")
    p1.terminate()
    p2.terminate()
    p1.wait()
    p2.wait()
    print("✅ Dashboards stopped")
