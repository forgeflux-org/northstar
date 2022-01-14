<div align="center">
  <h1>North Star </h1> 
  <b>A discovery service for ForgeFlux ecosystem</b>

[![Documentation](https://img.shields.io/badge/docs-master-blue)](https://forgeflux-org.github.io/northstar/openapi/)
[![Docker](https://img.shields.io/docker/pulls/forgedfed/northstar)](https://hub.docker.com/r/forgedfed/northstar)
[![Build](https://github.com/forgeflux-org/northstar/actions/workflows/linux.yml/badge.svg)](https://github.com/forgeflux-org/northstar/actions/workflows/linux.yml)
[![codecov](https://codecov.io/gh/forgeflux-org/northstar/branch/master/graph/badge.svg?token=0100H4ECG4)](https://codecov.io/gh/forgeflux-org/northstar)

</div>

## Why

ForgeFlux allows for multiple
[interfaces](https://github.com/forgeflux-org/interface) to be run against
a single software forge. Also, the protocol is flexible enough to
support multiple types of software forges(GitLab, GitHub, etc). The
protocol's decentralised nature makes it impossible to create a constant
record of which interfaces service forges.

So we created a discovery service which stores records of interfaces and
the forges they service. This is very similar to the way DNS works. In
DNS, hostname is resolved to IP address. Here, software forge URL is
resolved to URLs of interfaces that service the queried forge.

## Live instance

A live instance is available at
[https://northstar.forgeflux.org/](https://northstar.forgeflux.org/).

## API Specification

OpenAPI specification is available at
[https://forgeflux-org.github.io/northstar/](https://forgeflux-org.github.io/northstar/).

## Deployment

Docker images are run against every commit on `master`. We are currently
in alpha status, expect breaking changes while deploying images
tagged `latest`.

We'll freeze code once we have a stable release.

```bash
docker run -d \
	-v /path/to/your/northstar/config.toml:/home/northstar/app/config/settings.toml
	-p 3001:3000 \
	forgedfed/northstar
```

## Hacking

This codebase is fairly straight forward, see [Makefile](./Makefile) for
some helpful commands.
