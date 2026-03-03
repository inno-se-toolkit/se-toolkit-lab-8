# `Caddy`

<h2>Table of contents</h2>

- [What is `Caddy`](#what-is-caddy)
  - [`Caddyfile`](#caddyfile)
- [`Caddy` in this project](#caddy-in-this-project)
  - [`Caddyfile` in this project](#caddyfile-in-this-project)
  - [`Caddy` serves frontend files](#caddy-serves-frontend-files)
  - [`Caddy` forwards requests to backend](#caddy-forwards-requests-to-backend)
  - [`<caddy-port>`](#caddy-port)

## What is `Caddy`

`Caddy` is an open-source [web server](./web-development.md#web-server) and [reverse proxy](./computer-networks.md#reverse-proxy).

`Caddy` is configured via a [`Caddyfile`](#caddyfile).

See [`Caddy` in this project](#caddy-in-this-project).

Docs:

- [Caddy](https://caddyserver.com/docs/)

### `Caddyfile`

A `Caddyfile` is `Caddy`'s configuration file. It defines which port `Caddy` [listens](./computer-networks.md#listen-on-a-port) on and where to [forward requests](./computer-networks.md#forward-request).

Docs:

- [Caddyfile concepts](https://caddyserver.com/docs/caddyfile/concepts)
- [Environment variables in `Caddyfile`](https://caddyserver.com/docs/caddyfile/concepts#environment-variables)

## `Caddy` in this project

### `Caddyfile` in this project

In this project, the [`Caddyfile`](#caddyfile) is at [`caddy/Caddyfile`](../caddy/Caddyfile).

This configuration:

- Reads the value of [`CADDY_CONTAINER_PORT`](./dotenv-docker-secret.md#caddy_container_port) in [`.env.docker.secret`](./dotenv-docker-secret.md#what-is-envdockersecret).
- Makes `Caddy` [listen on the port](./computer-networks.md#listen-on-a-port) listen on this port inside a [`Docker` container](./docker.md#container).
- [Serves frontend files](#caddy-serves-frontend-files)
- [Forwards requests to backend](#caddy-forwards-requests-to-backend)

### `Caddy` serves frontend files

`Caddy` serves static [front-end](./web-development.md#frontend) files from `/srv` for all other paths. The `try_files` directive falls back to `index.html` for client-side routing.

### `Caddy` forwards requests to backend

<!-- TODO Rename API endpoints -> API paths? -->

`Caddy` routes [API endpoints](./api.md#endpoint) (`/items*`, `/learners*`, `/interactions*`, `/docs*`, `/openapi.json`) to the [`app` service](./docker-compose-yml.md#app-service).

### `<caddy-port>`

The [port number](./computer-networks.md#port-number) (without `<` and `>`) which `Caddy` [listens on](./computer-networks.md#listen-on-a-port).

The port number is the value of [`CADDY_HOST_PORT`](./dotenv-docker-secret.md#caddy_host_port) in [`.env.docker.secret`](./dotenv-docker-secret.md#what-is-envdockersecret).

Example: `42000`.
