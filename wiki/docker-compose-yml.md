# `docker-compose.yml`

<h2>Table of contents</h2>

- [What is `docker-compose.yml`](#what-is-docker-composeyml)
- [Services](#services)
  - [`app` service](#app-service)
  - [`postgres` service](#postgres-service)
  - [`pgadmin` service](#pgadmin-service)
  - [`caddy` service](#caddy-service)
- [Volumes](#volumes)
  - [`postgres_data`](#postgres_data)

## What is `docker-compose.yml`

[`docker-compose.yml`](../docker-compose.yml) is the [`Docker Compose`](./docker-compose.md#what-is-docker-compose) configuration file for this project. It defines four [services](./docker-compose.md#service) — [`app`](#app-service), [`postgres`](#postgres-service), [`pgadmin`](#pgadmin-service), [`caddy`](#caddy-service) — and one [volume](#volumes).

In this project, the services read their configuration from [environment variables](./environments.md#environment-variable) in [`.env.docker.secret`](./dotenv-docker-secret.md#what-is-envdockersecret).

Docs:

- [Compose file reference](https://docs.docker.com/reference/compose-file/)

## Services

### `app` service

The `app` service runs the [backend web server](./web-development.md#web-server).

It builds from the root [`Dockerfile`](../Dockerfile), which uses a multi-stage build: the first stage installs [`Python`](./python.md#what-is-python) dependencies with [`uv`](./python.md#uv), and the second stage runs the application.

Configuration in [`docker-compose.yml`](../docker-compose.yml):

- **`build: .`** — builds the [image](./docker.md#image) from the [`Dockerfile`](../Dockerfile) in the project root.
- **`restart: unless-stopped`** — restarts the [container](./docker.md#container) automatically unless it is explicitly stopped.
- **`ports`** — maps [`APP_HOST_ADDRESS`](./dotenv-docker-secret.md#app_host_address):[`APP_HOST_PORT`](./dotenv-docker-secret.md#app_host_port) on the [host](./computer-networks.md#host) to [`APP_CONTAINER_PORT`](./dotenv-docker-secret.md#app_container_port) inside the container.
- **`expose`** — makes `APP_CONTAINER_PORT` accessible to other services via [`Docker Compose` networking](./docker-compose.md#docker-compose-networking).
- **`environment`** — passes [environment variables](./environments.md#environment-variable) into the container. The values come from [`.env.docker.secret`](./dotenv-docker-secret.md#what-is-envdockersecret).
- **`depends_on`** — waits for the [`postgres` service](#postgres-service) to pass its [health check](./docker-compose.md#health-checks) before starting.

### `postgres` service

The `postgres` service runs a [`PostgreSQL`](./database.md#postgresql) [database server](./database.md#database-server).

Configuration in [`docker-compose.yml`](../docker-compose.yml):

- **`image`** — uses the `postgres:18.3-alpine` [image](./docker.md#image).
- **`restart: unless-stopped`** — restarts the [container](./docker.md#container) automatically unless it is explicitly stopped.
- **`environment`** — sets the database name ([`POSTGRES_DB`](./dotenv-docker-secret.md#postgres_db)), user ([`POSTGRES_USER`](./dotenv-docker-secret.md#postgres_user)), and password ([`POSTGRES_PASSWORD`](./dotenv-docker-secret.md#postgres_password)) from [`.env.docker.secret`](./dotenv-docker-secret.md#what-is-envdockersecret).
- **`ports`** — maps [`POSTGRES_HOST_ADDRESS`](./dotenv-docker-secret.md#postgres_host_address):[`POSTGRES_HOST_PORT`](./dotenv-docker-secret.md#postgres_host_port) on the [host](./computer-networks.md#host) to [`CONST_POSTGRESQL_DEFAULT_PORT`](./dotenv-docker-secret.md#const_postgresql_default_port) inside the container.
- **`volumes`** — mounts [`postgres_data`](#postgres_data) for persistent data storage and [`backend/app/data/init.sql`](../backend/app/data/init.sql) as the database initialization script. Scripts in `/docker-entrypoint-initdb.d/` run on the first startup of the container.
- **`healthcheck`** — runs `pg_isready` every 5 seconds to verify the database is ready to accept connections. Other services use this [health check](./docker-compose.md#health-checks) to wait before starting.

### `pgadmin` service

The `pgadmin` service runs [`pgAdmin`](./pgadmin.md#what-is-pgadmin), a web interface for managing [`PostgreSQL`](./database.md#postgresql) databases.

Configuration in [`docker-compose.yml`](../docker-compose.yml):

- **`image`** — uses the `dpage/pgadmin4:latest` [image](./docker.md#image).
- **`restart: unless-stopped`** — restarts the [container](./docker.md#container) automatically unless it is explicitly stopped.
- **`environment`** — sets the login email ([`PGADMIN_EMAIL`](./dotenv-docker-secret.md#pgadmin_email)) and password ([`PGADMIN_PASSWORD`](./dotenv-docker-secret.md#pgadmin_password)) from [`.env.docker.secret`](./dotenv-docker-secret.md#what-is-envdockersecret).
- **`ports`** — maps [`PGADMIN_HOST_ADDRESS`](./dotenv-docker-secret.md#pgadmin_host_address):[`PGADMIN_HOST_PORT`](./dotenv-docker-secret.md#pgadmin_host_port) on the [host](./computer-networks.md#host) to port `80` inside the container.
- **`depends_on`** — waits for the [`postgres` service](#postgres-service) to pass its [health check](./docker-compose.md#health-checks) before starting.

### `caddy` service

The `caddy` service runs [`Caddy`](./caddy.md#what-is-caddy), a [reverse proxy](./computer-networks.md#reverse-proxy) that serves [frontend](./web-development.md#frontend) files and forwards [API](./api.md#what-is-an-api) requests to the [`app` service](#app-service).

It builds from [`frontend/Dockerfile`](../frontend/Dockerfile), which uses a multi-stage build: the first stage builds the frontend with `Node.js`, and the second stage serves the output with `Caddy`.

Configuration in [`docker-compose.yml`](../docker-compose.yml):

- **`build: frontend/`** — builds the [image](./docker.md#image) from the [`Dockerfile`](../frontend/Dockerfile) in the `frontend/` directory.
- **`depends_on`** — waits for the `app` service to start before starting.
- **`environment`** — passes [`CADDY_CONTAINER_PORT`](./dotenv-docker-secret.md#caddy_container_port) and [`APP_CONTAINER_PORT`](./dotenv-docker-secret.md#app_container_port) from [`.env.docker.secret`](./dotenv-docker-secret.md#what-is-envdockersecret).
- **`ports`** — maps [`CADDY_HOST_ADDRESS`](./dotenv-docker-secret.md#caddy_host_address):[`CADDY_HOST_PORT`](./dotenv-docker-secret.md#caddy_host_port) on the [host](./computer-networks.md#host) to `CADDY_CONTAINER_PORT` inside the [container](./docker.md#container).
- **`volumes`** — mounts [`caddy/Caddyfile`](../caddy/Caddyfile) as the [`Caddy` configuration](./caddy.md#caddyfile).

See [`Caddy` in this project](./caddy.md#caddy-in-this-project) for how the `Caddyfile` routes requests.

## Volumes

[Volumes](./docker-compose.md#volume) are defined under the `volumes:` key at the top level of [`docker-compose.yml`](../docker-compose.yml).

### `postgres_data`

A named [volume](./docker-compose.md#volume) that stores [`PostgreSQL`](./database.md#postgresql) data. Data in this volume persists across container restarts.

The [`postgres` service](#postgres-service) mounts this volume at `/var/lib/postgresql/data`.

See [Resetting the database](./docker-postgres.md#resetting-the-database) to remove this volume and reinitialize the database.
