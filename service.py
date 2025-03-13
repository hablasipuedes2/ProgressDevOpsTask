import sys
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import logging
import winreg
import socket

class PythonService (win32serviceutil.ServiceFramework):
    _svc_name_ = "PythonService"
    _svc_display_name_ = "Python Service Example"
    REGISTRY_PATH = r"SOFTWARE\PythonService"
    LOG_FILE = "C:\\Windows\\Temp\\PythonService.log"
    logger = logging.getLogger()


    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

        logging.basicConfig(filename=self.LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger.setLevel(logging.INFO)
        log_file_path = self.read_registry_value("LogFilePath", "C:\\Windows\\Temp\\PythonService.log")
        self.setup_logging(log_file_path)


    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()
    
    def read_registry_value(self, name, default):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.REGISTRY_PATH) as key:
                value, _ = winreg.QueryValueEx(key, name)
                return value
        except FileNotFoundError:
            logging.warning(f"Registry key {name} not found. Using default: {default}")
            return default
        except Exception as e:
            logging.error(f"Error reading registry key {name}: {e}")
            return default

    def setup_logging(self, log_file_path):
        # Console handler (prints logs to the console)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
    
        # File handler (logs to a file)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO)
    
        # Log formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
    
        # Add both handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def main(self):
        log_interval = int(self.read_registry_value("LogInterval", 10))
 
        logging.info("Service Logger Started")
    
        while True:
            logging.info("Hello World")
            time.sleep(log_interval)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PythonService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PythonService)