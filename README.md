# Python Windows Service

## Overview
This project provides a Windows Service written in Python that logs messages at regular intervals. The service is being compiled into Windows [executable](PythonService.exe) via [pyinstaller](https://pyinstaller.org/en/stable/) and managed via [Install/Uninstall](install-uninstall.ps1) script.

## Features
- Runs as a Windows Service.
- Logs messages periodically to a specified log file.
- Uses Windows Registry for configuration.
- Supports automatic installation and uninstallation via PowerShell script.

## Requirements
- Windows OS 11
- Python installed via Windows Marketplace (I've hit some issues with the offical python dll, probably missing configuration)
- Python dependencies installed - the whole list could be found in the [Python script](PythonService.py)
- Windows Defender disabled (it removed my exe file every time I've tried to execute it)
- PowerShell (with Administrator privileges for installation)
- set execution policy to "Unrestricted" for Powershell

## Installation


### 1. Install the Service
Run the following PowerShell script as Administrator:
```powershell
.\install-uninstall.ps1
```
This script will:
- Create necessary registry keys for configuration.
- Install the service from `PythonService.exe`.
- Set the service to run as `NT SERVICE\PythonService`.
- Write into a log file with a default location `C:\Path\To\PythonService.log`
- Start the service automatically.

## Configuration
The service reads configuration values from the Windows Registry:
- `LogFilePath`: Path to the log file (Default: `C:\Path\To\PythonService.log`)
- `LogInterval`: Time interval (in seconds) between log entries (Default: `10` seconds)

To modify these values, edit the registry manually or modify `install-uninstall.ps1` before running it.

## Running the Service
Once installed, the service will run in the background. You can manage it using standard Windows Service commands:
```powershell
Start-Service -Name PythonService
Stop-Service -Name PythonService
Restart-Service -Name PythonService
Get-Service -Name PythonService
```

## Uninstallation
To uninstall the service, run:
```powershell
.\install-uninstall.ps1 uninstall
```
This script will:
- Stop and remove the service.
- Delete associated registry keys.
- Remove log files if necessary.

## Logging
Logs are stored in the file specified in the registry (default: `PythonService.log`). The logs include timestamps and service status updates. Other system logs and events could be found in Windows Event Viewer and Windows Services.

## Troubleshooting
- Ensure the script is run as Administrator.
- Check `PythonService.log` for error messages.
- Verify the registry keys under `HKLM:\SOFTWARE\PythonService`.
- Restart the service if it is not running.

## Known issues:
- The `install-uninstall.ps1` script is failing to start the service due to `The Python Service Example service terminated with the following service-specific error: Incorrect function.` This issue appeared after setting up the Service Virtual Account. Therefore, to see the service fully functioning, the Service Virtual Account should be removed.