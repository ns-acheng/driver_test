import win32serviceutil
import win32service
import pywintypes
import time

# Map service status codes to human-readable strings
STATUS_MAP = {
    win32service.SERVICE_STOPPED: "STOPPED",
    win32service.SERVICE_START_PENDING: "START_PENDING",
    win32service.SERVICE_STOP_PENDING: "STOP_PENDING",
    win32service.SERVICE_RUNNING: "RUNNING",
    win32service.SERVICE_CONTINUE_PENDING: "CONTINUE_PENDING",
    win32service.SERVICE_PAUSE_PENDING: "PAUSE_PENDING",
    win32service.SERVICE_PAUSED: "PAUSED",
}

def get_service_status(service_name: str, machine: str = None) -> str:
    try:
        # QueryServiceStatus returns a tuple
        # The 2nd element (index 1) is a tuple of (serviceType, serviceState, ...)
        status_tuple = win32serviceutil.QueryServiceStatus(service_name, machine)
        status_code = status_tuple[1]  # Get the serviceState code
        return STATUS_MAP.get(status_code, f"UNKNOWN ({status_code})")
    
    except pywintypes.error as e:
        if e.winerror == 1060:  # ERROR_SERVICE_DOES_NOT_EXIST
            return "NOT_FOUND"
        elif e.winerror == 5:   # ERROR_ACCESS_DENIED
            print(f"Error: Access Denied. Try running this script as an Administrator.")
        raise e

def start_service(service_name: str, machine: str = None, timeout: int = 30) -> bool:
    try:
        current_status = get_service_status(service_name, machine)
        if current_status == "RUNNING":
            print(f"Service '{service_name}' is already running.")
            return True
        
        if current_status == "NOT_FOUND":
            print(f"Error: Service '{service_name}' does not exist.")
            return False

        print(f"Starting service '{service_name}'...")
        win32serviceutil.StartService(service_name, machine)

        start_time = time.time()
        while time.time() - start_time < timeout:
            current_status = get_service_status(service_name, machine)
            if current_status == "RUNNING":
                print(f"Service '{service_name}' started successfully.")
                return True
            elif current_status not in ("START_PENDING"):
                print(f"Error: Service '{service_name}' entered an unexpected state: {current_status}")
                return False
            time.sleep(0.5)

        print(f"Error: Timeout. Service '{service_name}' did not start within {timeout}s.")
        return False

    except pywintypes.error as e:
        if e.winerror == 1056: # ERROR_SERVICE_ALREADY_RUNNING
             print(f"Service '{service_name}' is already running.")
             return True
        elif e.winerror == 5: # ERROR_ACCESS_DENIED
            print(f"Error starting '{service_name}': Access Denied. Run as Administrator.")
        else:
            print(f"Error starting '{service_name}': {e}")
        return False

def stop_service(service_name: str, machine: str = None, timeout: int = 30) -> bool:
    try:
        current_status = get_service_status(service_name, machine)
        if current_status == "STOPPED":
            print(f"Service '{service_name}' is already stopped.")
            return True

        if current_status == "NOT_FOUND":
            print(f"Error: Service '{service_name}' does not exist.")
            return False

        print(f"Stopping service '{service_name}'...")
        win32serviceutil.StopService(service_name, machine)

        start_time = time.time()
        while time.time() - start_time < timeout:
            current_status = get_service_status(service_name, machine)
            if current_status == "STOPPED":
                print(f"Service '{service_name}' stopped successfully.")
                return True
            elif current_status not in ("STOP_PENDING"):
                print(f"Error: Service '{service_name}' entered an unexpected state: {current_status}")
                return False
            time.sleep(0.5)

        print(f"Error: Timeout. Service '{service_name}' did not stop within {timeout}s.")
        return False

    except pywintypes.error as e:
        if e.winerror == 1062: # ERROR_SERVICE_NOT_ACTIVE
             print(f"Service '{service_name}' is already stopped.")
             return True
        elif e.winerror == 5: # ERROR_ACCESS_DENIED
            print(f"Error stopping '{service_name}': Access Denied. Run as Administrator.")
        else:
            print(f"Error stopping '{service_name}': {e}")
        return False


if __name__ == "__main__":
    SERVICE_TO_TEST = "Spooler" # Print Spooler
    print(f"--- Testing {__file__} ---")
    
    try:
        status = get_service_status(SERVICE_TO_TEST)
        print(f"Status of '{SERVICE_TO_TEST}': {status}")
    except Exception as e:
        print(f"Error testing: {e}")
        print("Please ensure you are running this script as an Administrator.")
