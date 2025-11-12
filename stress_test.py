import time
import sys
from service import start_service, stop_service, get_service_status

SERVICE_NAME = "stagentsvc"
INTERVAL_SECONDS = 60

def main_loop():
    print(f"--- Service Control Loop ---")
    print(f"Target Service: {SERVICE_NAME}")
    print(f"Interval: {INTERVAL_SECONDS} seconds")
    print("Press Ctrl+C to stop the loop.")
    print("-" * 30)

    while True:
        try:
            # --- START SERVICE ---
            print(f"\nAttempting to START '{SERVICE_NAME}'...")
            start_service(SERVICE_NAME)
            current_status = get_service_status(SERVICE_NAME)
            print(f"Current status: {current_status}")
            
            print(f"Waiting for {INTERVAL_SECONDS} seconds...")
            time.sleep(INTERVAL_SECONDS)

            print(f"\nAttempting to STOP '{SERVICE_NAME}'...")
            stop_service(SERVICE_NAME)
            current_status = get_service_status(SERVICE_NAME)
            print(f"Current status: {current_status}")

            print(f"Waiting for {INTERVAL_SECONDS} seconds...")
            time.sleep(INTERVAL_SECONDS)

        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"Retrying in {INTERVAL_SECONDS} seconds...")
            time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        # Handle Ctrl+C press
        print("\nLoop stopped by user. Exiting.")
        sys.exit(0)
