$serviceName = "PythonService"
$pythonExe = ".\PythonService.exe"
$regPath = "HKLM:\SOFTWARE\PythonService"
$cwd = (Get-Item .).FullName

function Create-RegistryEntries {
    if (!(Test-Path $regPath)) {
        New-Item -Path $regPath -Force | Out-Null
    }
    Set-ItemProperty -Path $regPath -Name "LogFilePath" -Value "${cwd}\PythonService.log"
    Set-ItemProperty -Path $regPath -Name "LogInterval" -Value 10
    Write-Host "Registry keys created successfully."
}

function Install-Service {
    Create-RegistryEntries

    # Install the service using pywin32
    & $pythonExe install
    
    # Set service to run as LocalService
    sc.exe config $serviceName obj= "NT SERVICE\$serviceName"

    # Grant permissions for all files in the working folder
    icacls "$cwd" /grant "NT SERVICE\${serviceName}:(RX)"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Service installed successfully."
        Start-Service -Name $serviceName
        Write-Host "Service started."
    } else {
        Write-Host "Failed to create service. Ensure you're running this script as Administrator."
    }
}

function Uninstall-Service {
    Stop-Service -Name $serviceName -Force -ErrorAction SilentlyContinue
    & $pythonExe remove
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