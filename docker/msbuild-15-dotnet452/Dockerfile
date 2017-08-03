FROM microsoft/windowsservercore

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]


RUN Invoke-WebRequest "https://download.microsoft.com/download/E/2/1/E21644B5-2DF2-47C2-91BD-63C560427900/NDP452-KB2901907-x86-x64-AllOS-ENU.exe" -OutFile NDP452-KB2901907-x86-x64-AllOS-ENU.exe -UseBasicParsing ; \
	Start-Process -FilePath 'NDP452-KB2901907-x86-x64-AllOS-ENU.exe' -ArgumentList '/q', '/norestart' -Wait; 

RUN Invoke-WebRequest "https://dist.nuget.org/win-x86-commandline/latest/nuget.exe" -OutFile "C:\windows\nuget.exe" -UseBasicParsing
RUN & nuget install MSBuild.Microsoft.VisualStudio.Web.targets -Version 14.0.0.3

RUN setx /M PATH $($Env:PATH + ';' + ${Env:ProgramFiles(x86)} + '\Microsoft Visual Studio\2017\BuildTools\MSBuild\15.0\Bin')