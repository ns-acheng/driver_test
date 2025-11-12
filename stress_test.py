import sys
from util_service import start_service, stop_service, get_service_status
from util_log import setup_logging
from util_time import sleep_ex
from util_subprocess import run_batch, run_powershell

SERVICE_NAME = "stagentsvc"
TARGET_LOOP = 1000
SHORT_SEC = 15
STD_SEC = 30
LONG_SEC = 60

try:
    logger, log_file = setup_logging()
except Exception as e:
    print(f"Critical error during logging setup: {e}", file=sys.stderr)
    sys.exit(1)

def main_loop():
    logger.info("--- Start Testing ---")
    logger.info(f"Target Service: {SERVICE_NAME}")
    logger.info("Press Ctrl+C to stop the loop.")
    logger.info("-" * 30)

    loop_count = 1
    while True:
        try:
            logger.info(f"==== Iteration {loop_count} ====")
            logger.info(f"Attempting to START '{SERVICE_NAME}'")
            current_status = get_service_status(SERVICE_NAME)
            logger.info(f"Current status: {current_status}")
            if current_status != "RUNNING":
                start_service(SERVICE_NAME)
                logger.info(f"Waiting for {STD_SEC} seconds")
                sleep_ex(STD_SEC)
            else:
                sleep_ex(5)

            logger.info(f"Running batch file to open 20 tabs")
            run_batch("10tab.bat")
            sleep_ex(LONG_SEC)

            logger.info(f"Attempting to STOP '{SERVICE_NAME}'")
            stop_service(SERVICE_NAME)
            current_status = get_service_status(SERVICE_NAME)
            logger.info(f"Current status: {current_status}")

            if loop_count == TARGET_LOOP:
                break
            loop_count += 1
            sleep_ex(STD_SEC)
            run_powershell("close_msedge.ps1")

        except KeyboardInterrupt:
            logger.info("Loop stopped by user. Exiting.")
            return
        except Exception:
            logger.exception("An error occurred:")
            logger.info(f"Retrying in {STD_SEC} seconds")
            sleep_ex(STD_SEC)

if __name__ == "__main__":
    try:
        logger.info(f"Logging initialized. Log file: {log_file}")
        main_loop()
    except KeyboardInterrupt:
        logger.info("Loop stopped by user. Exiting.")
        sys.exit(0)
