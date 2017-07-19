FROM msbuild:15
SHELL ["powershell"]

COPY . 'C:\\build\\'
WORKDIR 'C:\\build\\'

RUN ["nuget.exe", "restore"]
RUN ["msbuild.exe", "C:\\build\\GuidGenerator.sln"]

## Usage: build image, then create container and copy out the bin directory.

CMD ["powershell"]

