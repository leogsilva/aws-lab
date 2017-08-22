FROM msbuild:15

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

WORKDIR 'C:\\' 
COPY . 'C:\\'
RUN Start-Process -FilePath 'C:\\dotNetFx45_Full_x86_x64.exe' -ArgumentList '/q', '/norestart' -Wait ; 
