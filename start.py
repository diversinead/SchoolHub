import subprocess
import sys
import os
import time
import webbrowser

BASE = os.path.dirname(os.path.abspath(__file__))

print("Starting Assessments server  (port 8081)...")
assessments = subprocess.Popen([sys.executable, os.path.join(BASE, 'Assessments', 'assessments_server.py')])

print("Starting Assignments server  (port 8082)...")
assignments = subprocess.Popen([sys.executable, os.path.join(BASE, 'Assignments', 'assignments_server.py')])

time.sleep(1)

launcher = os.path.join(BASE, 'launcher.html')
print(f"Opening launcher: {launcher}")
webbrowser.open('file:///' + launcher.replace('\\', '/'))

print("\nAll servers running. Press Ctrl+C to stop.\n")
try:
    assessments.wait()
except KeyboardInterrupt:
    print("\nStopping servers...")
    assessments.terminate()
    assignments.terminate()
