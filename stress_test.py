import sys
import json
from util_service import start_service, stop_service, get_service_status
from util_log import setup_logging
from util_time import sleep_ex
from util_subprocess import run_batch, run_powershell

SERVICE_NAME = "stagentsvc"
CONFIG_FILE = "config.json"
SHORT_SEC = 15
STD_SEC = 30
LONG_SEC = 60

try:
    logger, log_file = setup_logging()
except Exception as e:
    print(f"Critical error during logging setup: {e}", file=sys.stderr)
    sys.exit(1)

def load_config():  
    defaults = {
        "loop_times": 1000,
        "stop_svc_per_n_run": 1
    }

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        logger.info(f"Loaded configuration from {CONFIG_FILE}")
        
        loop_times = config.get('loop_times', defaults['loop_times'])
        stop_svc_per_n_run = config.get('stop_svc_per_n_run', defaults['stop_svc_per_n_run'])

    except FileNotFoundError:
        logger.warning(f"{CONFIG_FILE} not found. Using default values.")
        loop_times = defaults['loop_times']
        stop_svc_per_n_run = defaults['stop_svc_per_n_run']
    except json.JSONDecodeError:
        logger.error(f"Error decoding {CONFIG_FILE}. Please check for valid JSON. Exiting.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading config: {e}. Exiting.")
        sys.exit(1)

    if not isinstance(loop_times, int) or loop_times <= 0:
        logger.error(f"invalid 'loop_times'. Exiting.")
        sys.exit(1)
        
    if not isinstance(stop_svc_per_n_run, int) or stop_svc_per_n_run < 0:
        logger.error(f"invalid 'stop_svc_per_n_run'. Exiting.")
        sys.exit(1)

    logger.info(f"Configuration set: loop_times = {loop_times}, stop_svc_per_n_run = {stop_svc_per_n_run}")
    return loop_times, stop_svc_per_n_run

def main_loop(loop_times, stop_svc_per_n_run):
    logger.info(f"--- Start Testing. Total iterations: {loop_times} ---")
    logger.info(f"Stop service every {stop_svc_per_n_run} run(s) (0 = never)")
    logger.info("Press Ctrl+C to stop the loop.")
    logger.info("-" * 30)

    for loop_count in range(1, loop_times + 1):
        try:
            logger.info(f"==== Iteration {loop_count} / {loop_times} ====")

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

            if stop_svc_per_n_run > 0 and loop_count % stop_svc_per_n_run == 0:
                logger.info(f"Attempting to STOP '{SERVICE_NAME}'")
                stop_service(SERVICE_NAME)
                current_status = get_service_status(SERVICE_NAME)
                logger.info(f"Current status: {current_status}")
            else:
                logger.info(f"Skipping service stop for this iteration (run {loop_count}).")

            sleep_ex(STD_SEC)
            run_powershell("close_msedge.ps1")

        except KeyboardInterrupt:
            logger.info("Loop stopped by user. Exiting.")
            return
        except Exception:
            logger.exception("An error occurred:")
            logger.info(f"Retrying in {STD_SEC} seconds")
            sleep_ex(STD_SEC)

    logger.info(f"--- Testing finished after {loop_times} iterations. ---")

if __name__ == "__main__":
    try:
        logger.info(f"Logging initialized. Log file: {log_file}")
        loop_times, stop_svc_per_n_run = load_config()
        main_loop(loop_times, stop_svc_per_n_run)
    except KeyboardInterrupt:
        logger.info("Loop stopped by user. Exiting.")
        sys.exit(0)