"""
Quick start script - run this to launch NexCart AI
"""
import os
import subprocess
import sys

print("=" * 50)
print("  NexCart AI - Intelligent Shopping Platform")
print("=" * 50)

# Load .env if exists
if os.path.exists('.env'):
    with open('.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_ai.settings')

print("\nStarting server at http://127.0.0.1:8000/")
print("Admin panel: http://127.0.0.1:8000/admin/")
print("Credentials: admin / admin123")
print("\nPress Ctrl+C to stop\n")

subprocess.run([sys.executable, 'manage.py', 'runserver'])
