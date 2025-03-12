$serviceName = "PythonService"
$scriptPath = "C:\Users\valushka\service.py"
$pythonExe = "C:\Program Files\Python313\python.exe"
$regPath = "HKLM:\SOFTWARE\PythonService"

function Create-RegistryEntries {
    if (!(Test-Path $regPath)) {
        New-Item -Path $regPath -Force | Out-Null
    }
    Set-ItemProperty -Path $regPath -Name "LogFilePath" -Value "C:\Windows\Temp\service.log"
    Set-ItemProperty -Path $regPath -Name "LogInterval" -Value 10
    Write-Host "Registry keys created successfully."
}

function Install-Service {
    # Install the service using pywin32
    & $pythonExe $scriptPath install
    
    # Set service to run as LocalService
    sc.exe config $serviceName obj= "NT AUTHORITY\LocalService"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Service installed successfully."
        Start-Service -Name $serviceName
        Write-Host "Service started."
        Create-RegistryEntries
    } else {
        Write-Host "Failed to create service. Ensure you're running this script as Administrator."
    }
}

function Uninstall-Service {
    Stop-Service -Name $serviceName -Force -ErrorAction SilentlyContinue
    & $pythonExe $scriptPath remove
    Remove-Item -Path $regPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Service uninstalled successfully."
}

# Ensure the script is running as Administrator (for installation only)
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Start-Process powershell.exe -ArgumentList "-File `"$PSCommandPath`"" -Verb RunAs
    exit
}

if ($args[0] -eq "uninstall") {
    Uninstall-Service
} else {
    Install-Service
}