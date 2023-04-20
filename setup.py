import subprocess
import sys

# Install dependencies

subprocess.call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
