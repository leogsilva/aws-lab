# escape=`
FROM microsoft/windowsservercore:10.0.14393.693
SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

ENV AWS_ACCESS_KEY_ID ""
ENV AWS_SECRET_ACCESS_KEY ""

RUN Install-PackageProvider -Name chocolatey -RequiredVersion 2.8.5.130 -Force; `
    Install-Package -Name microsoft-build-tools -RequiredVersion 14.0.25420.1 -Force; `
    Install-Package -Name netfx-4.5.2-devpack -RequiredVersion 4.5.5165101 -Force; `
    Install-Package -Name webdeploy -RequiredVersion 3.5.2 -Force;`
    Install-Package -Name python -Force


RUN Install-Package -Name nuget.commandline -RequiredVersion 3.4.3 -Force; `
    & C:\Chocolatey\bin\nuget install MSBuild.Microsoft.VisualStudio.Web.targets -Version 14.0.0.3

RUN setx /M PATH $($Env:PATH + ';' + ${Env:ProgramFiles(x86)} + '\MSBuild\14.0\Bin\')
RUN setx /M PATH $($Env:PATH + ';' + 'C:\Chocolatey\bin')

RUN setx /M PATH $($Env:PATH + ';' + 'C:\Python36')
RUN wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py
RUN python get-pip.py
RUN pip install awscli

ENTRYPOINT ["powershell"]
