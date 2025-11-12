import time
import sys
from service import start_service, stop_service, get_service_status
from log import setup_logging

SERVICE_NAME = "stagentsvc"
INTERVAL_SECONDS = 60

try:
    logger, log_file = setup_logging()
except Exception as e:
    print(f"Critical error during logging setup: {e}", file=sys.stderr)
    sys.exit(1)

def main_loop():
    logger.info("--- Service Control Loop ---")
    logger.info(f"Target Service: {SERVICE_NAME}")
    logger.info(f"Interval: {INTERVAL_SECONDS} seconds")
    logger.info("Press Ctrl+C to stop the loop.")
    logger.info("-" * 30)

    while True:
        try:
            logger.info(f"Attempting to START '{SERVICE_NAME}'...")
            start_service(SERVICE_NAME)
            current_status = get_service_status(SERVICE_NAME)
            logger.info(f"Current status: {current_status}")
            
            logger.info(f"Waiting for {INTERVAL_SECONDS} seconds...")
            time.sleep(INTERVAL_SECONDS)

            logger.info(f"Attempting to STOP '{SERVICE_NAME}'...")
            stop_service(SERVICE_NAME)
            current_status = get_service_status(SERVICE_NAME)
            logger.info(f"Current status: {current_status}")

            logger.info(f"Waiting for {INTERVAL_SECONDS} seconds...")
            time.sleep(INTERVAL_SECONDS)

        except Exception as e:
            logger.exception("An error occurred:")
            logger.info(f"Retrying in {INTERVAL_SECONDS} seconds...")
            time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        logger.info(f"Logging initialized. Log file: {log_file}")
        main_loop()
    except KeyboardInterrupt:
        logger.info("Loop stopped by user. Exiting.")
        sys.exit(0)