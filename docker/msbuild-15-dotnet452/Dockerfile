FROM microsoft/windowsservercore

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

RUN Invoke-WebRequest "https://aka.ms/vs/15/release/vs_BuildTools.exe" -OutFile vs_BuildTools.exe -UseBasicParsing ; \
	Start-Process -FilePath 'vs_BuildTools.exe' -ArgumentList '--quiet', '--norestart', '--locale en-US' -Wait ; \
	Remove-Item .\vs_BuildTools.exe ; \
	Remove-Item -Force -Recurse 'C:\Program Files (x86)\Microsoft Visual Studio\Installer'

RUN Invoke-WebRequest "https://download.microsoft.com/download/E/2/1/E21644B5-2DF2-47C2-91BD-63C560427900/NDP452-KB2901907-x86-x64-AllOS-ENU.exe" -OutFile NDP452-KB2901907-x86-x64-AllOS-ENU.exe -UseBasicParsing ; \
	Start-Process -FilePath 'NDP452-KB2901907-x86-x64-AllOS-ENU.exe' -ArgumentList '/q', '/norestart' -Wait; 

RUN Invoke-WebRequest "https://download.microsoft.com/download/4/3/B/43B61315-B2CE-4F5B-9E32-34CCA07B2F0E/NDP452-KB2901951-x86-x64-DevPack.exe" -OutFile NDP452-KB2901951-x86-x64-DevPack.exe -UseBasicParsing ; \
	Start-Process -FilePath 'NDP452-KB2901951-x86-x64-DevPack.exe' -ArgumentList '/q', '/norestart' -Wait; 


RUN Invoke-WebRequest "https://dist.nuget.org/win-x86-commandline/latest/nuget.exe" -OutFile "C:\windows\nuget.exe" -UseBasicParsing
RUN & nuget install MSBuild.Microsoft.VisualStudio.Web.targets -Version 14.0.0.3

RUN setx /M PATH $($Env:PATH + ';' + ${Env:ProgramFiles(x86)} + '\Microsoft Visual Studio\2017\BuildTools\MSBuild\15.0\Bin')