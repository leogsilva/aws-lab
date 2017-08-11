FROM msbuild:15

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

RUN Install-WindowsFeature NET-Framework-45-Core ; \
    Install-WindowsFeature NET-Framework-45-ASPNET ; \  
    Install-WindowsFeature Web-Asp-Net45

RUN Invoke-WebRequest "http://go.microsoft.com/fwlink/?LinkId=225702" -Outfile dotNetFx45_Full_x86_x64.exe -UseBasicParsing ; \
        Start-Process -FilePath 'dotNetFx45_Full_x86_x64.exe' -ArgumentList '/q', '/norestart' -Wait ; 
