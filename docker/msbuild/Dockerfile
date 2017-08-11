FROM microsoft/dotnet-framework:4.6.2

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]


RUN mkdir 'C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools'
COPY BuildTools.zip .
RUN Expand-Archive .\BuildTools.zip 'C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools'
RUN Invoke-WebRequest "https://download.microsoft.com/download/E/F/D/EFD52638-B804-4865-BB57-47F4B9C80269/NDP462-DevPack-KB3151934-ENU.exe" -Outfile NDP462-DevPack-KB3151934-ENU.exe -UseBasicParsing ; \
        Start-Process -FilePath 'NDP462-DevPack-KB3151934-ENU.exe' -ArgumentList '/Quiet', '/NoRestart' -Wait ; 


RUN Invoke-WebRequest "https://dist.nuget.org/win-x86-commandline/latest/nuget.exe" -OutFile "C:\windows\nuget.exe" -UseBasicParsing
RUN & nuget install MSBuild.Microsoft.VisualStudio.Web.targets -Version 14.0.0.3

RUN setx /M PATH $($Env:PATH + ';' + ${Env:ProgramFiles(x86)} + '\Microsoft Visual Studio\2017\BuildTools\MSBuild\15.0\Bin')