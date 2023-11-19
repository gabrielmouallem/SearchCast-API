import subprocess
import sys
import os

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)

# Check if venv exists, if not, create it
venv_path = "venv"
if not os.path.exists(venv_path):
    run_command([sys.executable, "-m", "venv", venv_path])

# Activate the virtual environment
activate_script = "Scripts/activate" if os.name == "nt" else "bin/activate"
activate_path = os.path.normpath(os.path.join(venv_path, activate_script))

# Source the activation script directly in the shell
activate_command = f"source {activate_path}" if os.name != "nt" else f"{activate_path}"
print(activate_command)

# Run the activation command in the shell
subprocess.run(activate_command, shell=True)

# Install dependencies
run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Run the main Python script (normalize the path)
main_script_path = os.path.normpath(os.path.join("shorts-sniper", "main.py"))
print(f"Running {main_script_path}...")

# Use subprocess.Popen to capture and print output in real-time
with subprocess.Popen([sys.executable, main_script_path], stdout=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True) as process:
    for line in process.stdout:
        print(line, end='')

# Wait for the process to finish
process.wait()
