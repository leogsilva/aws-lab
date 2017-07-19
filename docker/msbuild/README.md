Here is a Dockerfile for building microsoft .net based applications.
Contains msbuild version 15.0, nuget and .NET devpack 4.6.2
To test this image, just build the sample project on examples directory on this repository

To build:
`docker build -t msbuild:15 .`

More similar projects:
* https://github.com/friism/dockerfiles/tree/master/vs-build-tools
* https://hub.docker.com/r/friism/vs-build-tools/
* https://github.com/alexellis/guidgenerator-aspnet

Reference article
* https://blog.alexellis.io/3-steps-to-msbuild-with-docker/