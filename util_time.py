import time

def sleep_ex(duration_seconds: float):
    if duration_seconds <= 1.0:
        time.sleep(duration_seconds)
        return

    try:
        end_time = time.time() + duration_seconds

        while time.time() < end_time:
            remaining = end_time - time.time()
            sleep_interval = 0.0
        
            if remaining >= 1.0:
                sleep_interval = 1.0
            elif remaining > 0:
                sleep_interval = remaining
            else:
                break

            time.sleep(sleep_interval)
    except KeyboardInterrupt:
        return
