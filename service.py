import win32serviceutil
import win32service
import pywintypes
import time
from enum import Enum

class _Action(Enum):
    START = "start"
    STOP = "stop"


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
        status_tuple = win32serviceutil.QueryServiceStatus(service_name, machine)
        status_code = status_tuple[1]
        return STATUS_MAP.get(status_code, f"UNKNOWN ({status_code})")
    
    except pywintypes.error as e:
        if e.winerror == 1060:
            return "NOT_FOUND"
        elif e.winerror == 5:
            print(f"Error: Access Denied. Try running this script as an Administrator.")
        raise e

def start_service(service_name: str, machine: str = None, timeout: int = 30) -> bool:
    return _control_service(service_name, _Action.START, machine, timeout)

def stop_service(service_name: str, machine: str = None, timeout: int = 30) -> bool:
    return _control_service(service_name, _Action.STOP, machine, timeout)


def _control_service(service_name: str, action: _Action, machine: str = None, timeout: int = 30) -> bool:
    
    if action == _Action.START:
        action_str = "Starting"
        service_func = win32serviceutil.StartService
        target_status = STATUS_MAP[win32service.SERVICE_RUNNING]
        pending_status = STATUS_MAP[win32service.SERVICE_START_PENDING]
        already_done_error_code = 1056
    elif action == _Action.STOP:
        action_str = "Stopping"
        service_func = win32serviceutil.StopService
        target_status = STATUS_MAP[win32service.SERVICE_STOPPED]
        pending_status = STATUS_MAP[win32service.SERVICE_STOP_PENDING]
        already_done_error_code = 1062
    else:
        print(f"Error: Invalid internal action '{action}' specified.")
        return False

    try:
        current_status = get_service_status(service_name, machine)
        
        if current_status == target_status:
            print(f"Service '{service_name}' is already {target_status.lower()}.")
            return True
        
        if current_status == "NOT_FOUND":
            print(f"Error: Service '{service_name}' does not exist.")
            return False

        print(f"{action_str} service '{service_name}'...")
        service_func(service_name, machine)

        start_time = time.time()
        while time.time() - start_time < timeout:
            current_status = get_service_status(service_name, machine)
            
            if current_status == target_status:
                print(f"Service '{service_name}' {action.value}ed successfully.")
                return True
            
            if current_status != pending_status:
                print(f"Error: Service '{service_name}' entered an unexpected state: {current_status}")
                return False
                
            time.sleep(0.5)

        print(f"Error: Timeout. Service '{service_name}' did not {action.value} within {timeout}s.")
        return False

    except pywintypes.error as e:
        if e.winerror == already_done_error_code:
            print(f"Service '{service_name}' is already {target_status.lower()}.")
            return True
        elif e.winerror == 5:
            print(f"Error {action_str.lower()} '{service_name}': Access Denied. Run as Administrator.")
        else:
            print(f"Error {action_str.lower()} '{service_name}': {e}")
        return False


if __name__ == "__main__":
    SERVICE_TO_TEST = "Spooler" # Print Spooler
    print(f"--- Testing {__file__} ---")
    
    try:
        print(f"\nAttempting to STOP '{SERVICE_TO_TEST}'...")
        if stop_service(SERVICE_TO_TEST):
            status = get_service_status(SERVICE_TO_TEST)
            print(f"Current status of '{SERVICE_TO_TEST}': {status}")

        time.sleep(2)
        
        print(f"\nAttempting to START '{SERVICE_TO_TEST}'...")
        if start_service(SERVICE_TO_TEST):
            status = get_service_status(SERVICE_TO_TEST)
            print(f"Current status of '{SERVICE_TO_TEST}': {status}")
            
    except Exception as e:
        print(f"Error testing: {e}")
        print("Please ensure you are running this script as an Administrator.")