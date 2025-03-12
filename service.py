import win32serviceutil
import win32service
import win32event
import servicemanager
import logging
import time
import winreg
import sys
import os

# Registry key path
REGISTRY_PATH = r"SOFTWARE\PythonService"

LOG_FILE = "C:\\Windows\\Temp\\PythonService.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def read_registry_value(name, default):
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REGISTRY_PATH) as key:
            value, _ = winreg.QueryValueEx(key, name)
            return value
    except FileNotFoundError:
        logging.warning(f"Registry key {name} not found. Using default: {default}")
        return default
    except Exception as e:
        logging.error(f"Error reading registry key {name}: {e}")
        return default

class PythonService(win32serviceutil.ServiceFramework):
    """Python Windows Service"""
    
    _svc_name_ = "PythonService"
    _svc_display_name_ = "Python Service Example"
    _svc_description_ = "A sample Windows service that logs messages periodically."

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        logging.info("Service is stopping...")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        logging.info("Service is starting...")
        servicemanager.LogInfoMsg("Python Service Started")
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)

        # Read registry values
        log_interval = int(read_registry_value("LogInterval", 10))

        while True:
            result = win32event.WaitForSingleObject(self.stop_event, log_interval * 1000)
            if result == win32event.WAIT_OBJECT_0:
                break  # Stop signal received
            logging.info("Hello World!")

        logging.info("Service stopped.")

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(PythonService)