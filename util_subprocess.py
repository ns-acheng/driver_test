import subprocess
import sys

def run_batch(batch_file: str = "20tab.bat"):

    try:
        subprocess.Popen(["cmd", "/c", batch_file])

    except subprocess.CalledProcessError as e:
        print(f"\n--- ERROR ---", file=sys.stderr)
        print(f"Command failed: {' '.join(e.cmd)}", file=sys.stderr)
        print(f"Return code: {e.returncode}", file=sys.stderr)
        
        error_message = e.stderr.strip() if e.stderr else "No error output."
        if not error_message and e.stdout:
             error_message = e.stdout.strip()

        print(f"Error details: {error_message}", file=sys.stderr)
        print("Exiting due to error.", file=sys.stderr)
        
    
    except FileNotFoundError as e:
        print(f"\n--- ERROR ---", file=sys.stderr)
        print(f"Command not found: {e.filename}", file=sys.stderr)
        print("Ensure the Windows System32 directory is in your PATH.", file=sys.stderr)


def run_powershell(script_path):
    command = [
        "powershell.exe",
        "-ExecutionPolicy", "Bypass",
        "-File", script_path
    ]
    
    try:
        print(f"Attempting to run PowerShell script: {script_path}...")
        
        subprocess.run(
            command, 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        print(f"Successfully executed '{script_path}'.")

    except subprocess.CalledProcessError as e:
        print(f"\n--- ERROR ---", file=sys.stderr)
        print(f"Script failed: {' '.join(e.cmd)}", file=sys.stderr)
        print(f"Return code: {e.returncode}", file=sys.stderr)
        
        error_message = e.stderr.strip() if e.stderr else "No error output."
        if not error_message and e.stdout:
             error_message = e.stdout.strip()

        print(f"Error details: {error_message}", file=sys.stderr)
    
    except FileNotFoundError:
        print(f"\n--- ERROR ---", file=sys.stderr)
        print("PowerShell.exe not found.", file=sys.stderr)
        print("Ensure PowerShell is installed and in your system's PATH.", file=sys.stderr)
