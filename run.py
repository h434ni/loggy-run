"""
Application Logger Wrapper
--------------------------
This script runs a specified command (or a default one), captures its
Standard Output (stdout) and Standard Error (stderr) in real-time,
prints them to the console, and saves them to a timestamped file in a ./logs directory.

Features:
- Auto-detects Python Virtual Environments (venv).
- Forces UTF-8 encoding to prevent Windows Unicode crashes (Charmap errors).
- Creates the log directory automatically.

Usage:
    1. Run default command:   python logger.py
    2. Run custom command:    python logger.py ping google.com
"""

import sys
import subprocess
import os
import datetime

# --- CONFIGURATION ---

# The directory where log files will be saved
LOG_DIR = "logs"

# The command to run if no arguments are passed to this script
DEFAULT_COMMAND = ["python", "main.py"]

# ---------------------

def get_log_filepath():
    """Generates a timestamped filename inside the LOG_DIR."""
    # Create the logs directory if it doesn't exist
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        print(f"[*] Created log directory: {LOG_DIR}")

    # Generate timestamp: YYYY-MM-DD_HH-MM-SS
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"log_{timestamp}.txt"
    
    return os.path.join(LOG_DIR, filename)

def run_and_log(command_args):
    """
    Executes a command, streams output to console, and saves to a log file.
    
    Args:
        command_args (list): A list of strings representing the command 
                             (e.g., ["python", "main.py"])
                             
    Returns:
        int: The exit code of the subprocess.
    """
    
    # 1. SMART FIX FOR VENV
    # If we are running a python script, ensure we use the current interpreter
    # (the one currently running logger.py), ensuring we stay in the venv.
    if command_args[0] == "python" or command_args[0] == "python3":
        command_args[0] = sys.executable

    # 2. FORCE UNBUFFERED OUTPUT
    # If running python, add '-u' so logs appear immediately, not in chunks.
    if "python" in command_args[0] and "-u" not in command_args:
        command_args.insert(1, "-u")

    # 3. FORCE UTF-8 ENCODING
    # This fixes the UnicodeEncodeError/Charmap crashes on Windows.
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    log_file = get_log_filepath()

    print(f"--- Running: {' '.join(command_args)} ---")
    print(f"--- Logging to: {log_file} ---")

    try:
        # Open the log file in write mode with UTF-8 encoding
        with open(log_file, "w", encoding="utf-8") as f:
            
            # Start the process
            process = subprocess.Popen(
                command_args,
                stdout=subprocess.PIPE,  # Capture stdout
                stderr=subprocess.STDOUT, # Merge stderr into stdout
                text=True,                # Treat output as text, not bytes
                bufsize=1,                # Line buffering
                env=env,                  # Pass the UTF-8 forced environment
                encoding='utf-8',         # Read pipe as UTF-8
                errors='replace'          # Replace bad chars instead of crashing
            )

            # Read output line by line
            for line in process.stdout:
                # A. Write to Terminal
                try:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                except UnicodeEncodeError:
                    # Fallback for legacy Windows consoles that can't print emojis
                    sys.stdout.write(line.encode('ascii', 'replace').decode())
                    sys.stdout.flush()
                
                # B. Write to File
                f.write(line)
                f.flush()

            # Wait for process to finish
            process.wait()
            return process.returncode

    except KeyboardInterrupt:
        print("\n[!] Process interrupted by user.")
        return 130 # Standard SIGINT exit code
    except Exception as e:
        print(f"\n[!] Critical Error: {e}")
        return 1

def main():
    # Determine which command to run
    if len(sys.argv) < 2:
        # No args provided -> Use Default
        command = list(DEFAULT_COMMAND)
    else:
        # Args provided -> Use User input
        command = sys.argv[1:]

    exit_code = run_and_log(command)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
