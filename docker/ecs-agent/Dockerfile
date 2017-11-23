# escape=`
FROM microsoft/windowsservercore:10.0.14393.693
SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

ENV AWS_ACCESS_KEY_ID ""
ENV AWS_SECRET_ACCESS_KEY ""

#RUN Install-PackageProvider -Name chocolatey -RequiredVersion 2.8.5.130 -Force; `
#    Install-Package -Name git -Force -Verbose; `
#    Install-Package -Name jdk8 -ProviderName chocolatey -Force -Verbose; `
#    Install-Package -Name docker -RequiredVersion 17.10.0 -Force -Verbose; `
#    Install-Package -Name python -RequiredVersion 3.6.0 -Force

RUN iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); refreshenv
RUN choco install jdk8 -y ; choco install docker -y ; choco install python -y

RUN Invoke-WebRequest -Uri 'https://repo.jenkins-ci.org/releases/org/jenkins-ci/plugins/swarm-client/3.4/swarm-client-3.4.jar' -OutFile 'C:\\swarm-client-3.4.jar'
RUN setx /M PATH $($Env:PATH + ';' + 'C:\Chocolatey\bin')

RUN setx /M PATH $($Env:PATH + ';' + 'C:\Python36')
COPY get-pip.py /
RUN python /get-pip.py
RUN pip install awscli

ENTRYPOINT ["powershell"]
