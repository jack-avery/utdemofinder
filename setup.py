import subprocess
import sys

# Install dependencies

subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
)
