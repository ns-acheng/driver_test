import time
import sys
import logging
from datetime import datetime
from service import start_service, stop_service, get_service_status

SERVICE_NAME = "stagentsvc"
INTERVAL_SECONDS = 60

logger = logging.getLogger()

def setup_logging():
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f'service_control_{timestamp}.log'

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return log_filename

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
        log_file = setup_logging()
        logger.info(f"Logging initialized. Log file: {log_file}")
        main_loop()
    except KeyboardInterrupt:
        logger.info("Loop stopped by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"Critical error during setup: {e}", file=sys.stderr)
        sys.exit(1)