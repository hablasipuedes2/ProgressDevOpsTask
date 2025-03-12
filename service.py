import asyncio
import logging
import time
import winreg
import signal
import sys
import os

# Registry key path
REGISTRY_PATH = r"SOFTWARE\PythonService"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Remove any existing handlers (if any, e.g., StreamHandler for stdout)
if logger.hasHandlers():
    logger.handlers.clear()

def setup_logging(log_file_path):
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
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

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

async def service_loop():

    # Read registry values
    log_interval = int(read_registry_value("LogInterval", 10))

    logging.info("Service Logger Started")

    while True:
        logging.info("Hello World")
        await asyncio.sleep(log_interval)

def handle_signal(signum, frame):
    logging.info(f"Received termination signal {signum}. Shutting down gracefully...")
    exit(0)

async def main():
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)  # Handles Ctrl+C for testing

    await service_loop()

if __name__ == "__main__":
    try:
        # Set up logging before starting the main loop
        log_file_path = read_registry_value("LogFilePath", "C:\\Windows\\Temp\\service.log")
        setup_logging(log_file_path)

        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Service stopped manually.")
    finally:
        logging.info("Exiting cleanly.")