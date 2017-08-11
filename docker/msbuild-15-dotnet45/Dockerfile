FROM microsoft/dotnet-framework:4.6.2

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

RUN Install-WindowsFeature NET-Framework-45-Core ; \
    Install-WindowsFeature NET-Framework-45-ASPNET ; \  
    Install-WindowsFeature Web-Asp-Net45

RUN Invoke-WebRequest "https://aka.ms/vs/15/release/vs_BuildTools.exe" -OutFile vs_BuildTools.exe -UseBasicParsing ; \
	Start-Process -FilePath 'vs_BuildTools.exe' -ArgumentList '--quiet', '--norestart', '--locale en-US' -Wait ; \
	Remove-Item .\vs_BuildTools.exe ;
RUN Invoke-WebRequest "http://go.microsoft.com/fwlink/?LinkId=225702" -Outfile dotNetFx45_Full_x86_x64.exe -UseBasicParsing ; \
        Start-Process -FilePath 'dotNetFx45_Full_x86_x64.exe' -ArgumentList '/Quiet', '/NoRestart' -Wait ; 

RUN Invoke-WebRequest "https://dist.nuget.org/win-x86-commandline/latest/nuget.exe" -OutFile "C:\windows\nuget.exe" -UseBasicParsing
RUN & nuget install MSBuild.Microsoft.VisualStudio.Web.targets -Version 14.0.0.3

RUN setx /M PATH $($Env:PATH + ';' + ${Env:ProgramFiles(x86)} + '\Microsoft Visual Studio\2017\BuildTools\MSBuild\15.0\Bin')