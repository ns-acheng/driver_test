import subprocess
import sys

def run_batch_file(batch_file: str = "20tab.bat"):

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
        
