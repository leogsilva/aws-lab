FROM msbuild:15

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

RUN Invoke-WebRequest "https://download.microsoft.com/download/E/2/1/E21644B5-2DF2-47C2-91BD-63C560427900/NDP452-KB2901907-x86-x64-AllOS-ENU.exe" -OutFile NDP452-KB2901907-x86-x64-AllOS-ENU.exe -UseBasicParsing ; \
	Start-Process -FilePath 'NDP452-KB2901907-x86-x64-AllOS-ENU.exe' -ArgumentList '/q', '/norestart' -Wait; 

RUN Invoke-WebRequest "https://download.microsoft.com/download/4/3/B/43B61315-B2CE-4F5B-9E32-34CCA07B2F0E/NDP452-KB2901951-x86-x64-DevPack.exe" -OutFile NDP452-KB2901951-x86-x64-DevPack.exe -UseBasicParsing ; \
	Start-Process -FilePath 'NDP452-KB2901951-x86-x64-DevPack.exe' -ArgumentList '/q', '/norestart' -Wait; 
