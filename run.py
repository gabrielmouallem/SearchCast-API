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
activate_script = "Scripts/activate.bat" if os.name == "nt" else "bin/activate"
activate_path = os.path.normpath(os.path.join(venv_path, activate_script))
activate_command = f"source {activate_path}" if os.name != "nt" else f"{activate_path}"
run_command([activate_command])

# Install dependencies
run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Run the main Python script (normalize the path)
main_script_path = os.path.normpath(os.path.join("shorts-sniper", "main.py"))
print(f"Running {main_script_path}...")

# Capture and color the output of the main script
main_script_output = subprocess.check_output(
    [sys.executable, main_script_path], text=True
)
print(main_script_output)

# Deactivate the virtual environment (not needed on Windows)
if os.name != "nt":
    run_command(["deactivate"])
