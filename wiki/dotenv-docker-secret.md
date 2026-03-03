# `.env.docker.secret`

<h2>Table of contents</h2>

- [What is `.env.docker.secret`](#what-is-envdockersecret)
- [`app`](#app)
  - [`APP_NAME`](#app_name)
  - [`APP_DEBUG`](#app_debug)
  - [`APP_RELOAD`](#app_reload)
  - [`APP_CONTAINER_ADDRESS`](#app_container_address)
  - [`APP_CONTAINER_PORT`](#app_container_port)
  - [`APP_HOST_ADDRESS`](#app_host_address)
  - [`APP_HOST_PORT`](#app_host_port)
  - [`APP_ENABLE_INTERACTIONS`](#app_enable_interactions)
  - [`APP_ENABLE_LEARNERS`](#app_enable_learners)
  - [`API_KEY`](#api_key)
- [`postgres`](#postgres)
  - [`POSTGRES_DB`](#postgres_db)
  - [`POSTGRES_USER`](#postgres_user)
  - [`POSTGRES_PASSWORD`](#postgres_password)
  - [`POSTGRES_HOST_ADDRESS`](#postgres_host_address)
  - [`POSTGRES_HOST_PORT`](#postgres_host_port)
- [`pgadmin`](#pgadmin)
  - [`PGADMIN_EMAIL`](#pgadmin_email)
  - [`PGADMIN_PASSWORD`](#pgadmin_password)
  - [`PGADMIN_HOST_ADDRESS`](#pgadmin_host_address)
  - [`PGADMIN_HOST_PORT`](#pgadmin_host_port)
- [`caddy`](#caddy)
  - [`CADDY_CONTAINER_PORT`](#caddy_container_port)
  - [`CADDY_HOST_ADDRESS`](#caddy_host_address)
  - [`CADDY_HOST_PORT`](#caddy_host_port)
- [Constants](#constants)
  - [`CONST_POSTGRESQL_SERVICE_NAME`](#const_postgresql_service_name)
  - [`CONST_POSTGRESQL_SERVER_NAME`](#const_postgresql_server_name)
  - [`CONST_POSTGRESQL_DEFAULT_PORT`](#const_postgresql_default_port)

## What is `.env.docker.secret`

`.env.docker.secret` is an [`.env` file](./environments.md#env-file) that stores [environment variables](./environments.md#environment-variable) for [`Docker Compose`](./docker-compose.md#what-is-docker-compose).

The values are substituted into [`docker-compose.yml`](../docker-compose.yml) when running commands with the `--env-file` flag (e.g., `docker compose --env-file .env.docker.secret up --build`).

Default values: [`.env.docker.example`](../.env.docker.example)

> [!NOTE]
> It was added to [`.gitignore`](./git.md#gitignore) because you may specify there
> [secrets](./environments.md#secrets) such as the [API key](#api_key) or the [address of your VM](./vm.md#your-vm-ip-address).

> [!TIP]
> No edits are needed for local development.
> The default values in [`.env.docker.example`](../.env.docker.example) work out of the box.

## `app`

Variables for the backend [`app` service](./docker-compose-yml.md#app-service).

### `APP_NAME`

The display name of the application.

Default: `"Learning Management Service"`

### `APP_DEBUG`

Enables debug mode in the [web server](./web-development.md#web-server). When `true`, the server returns detailed error messages.

Default: `false`

### `APP_RELOAD`

Enables auto-reload. When `true`, the [web server](./web-development.md#web-server) restarts automatically when source files change.

Default: `false`

### `APP_CONTAINER_ADDRESS`

The [IP address](./computer-networks.md#ip-address) the app [listens on](./computer-networks.md#listen-on-a-port) inside the [container](./docker.md#container). [`0.0.0.0`](./computer-networks.md#0000) means all network interfaces.

Default: `0.0.0.0`

### `APP_CONTAINER_PORT`

The [port number](./computer-networks.md#port-number) the app [listens on](./computer-networks.md#listen-on-a-port) inside the [container](./docker.md#container).

Default: `8000`

### `APP_HOST_ADDRESS`

The [IP address](./computer-networks.md#ip-address) exposed on the [host](./computer-networks.md#host). [`127.0.0.1`](./computer-networks.md#127001) restricts access to the local machine only.

Default: `127.0.0.1`

### `APP_HOST_PORT`

The [port number](./computer-networks.md#port-number) exposed on the [host](./computer-networks.md#host) for accessing the app.

Default: `42001`

### `APP_ENABLE_INTERACTIONS`

A [feature flag](./web-development.md#feature-flag) for enabling the `/interactions` endpoint.

Default: `true`

### `APP_ENABLE_LEARNERS`

A [feature flag](./web-development.md#feature-flag) for enabling the `/learners` endpoint.

Default: `true`

### `API_KEY`

The secret key used to authorize [API](./api.md#what-is-an-api) requests. See [API key authentication](./security.md#api-key-authentication).

Default: `my-secret-api-key`

## `postgres`

Variables for the [`postgres` service](./docker-compose-yml.md#postgres-service).

### `POSTGRES_DB`

The name of the [database](./database.md#what-is-a-database) created on the first startup.

Default: `db-lab-4`

### `POSTGRES_USER`

The username for the [`PostgreSQL`](./database.md#postgresql) database.

Default: `postgres`

### `POSTGRES_PASSWORD`

The password for the [`PostgreSQL`](./database.md#postgresql) database.

Default: `postgres`

### `POSTGRES_HOST_ADDRESS`

The [IP address](./computer-networks.md#ip-address) exposed on the [host](./computer-networks.md#host). [`127.0.0.1`](./computer-networks.md#127001) restricts access to the local machine only.

Default: `127.0.0.1`

### `POSTGRES_HOST_PORT`

The [port number](./computer-networks.md#port-number) exposed on the [host](./computer-networks.md#host) for accessing [`PostgreSQL`](./database.md#postgresql).

Default: `42004`

## `pgadmin`

Variables for the [`pgadmin` service](./docker-compose-yml.md#pgadmin-service).

### `PGADMIN_EMAIL`

The email used to log in to [`pgAdmin`](./pgadmin.md#what-is-pgadmin).

Default: `admin@example.com`

### `PGADMIN_PASSWORD`

The password used to log in to [`pgAdmin`](./pgadmin.md#what-is-pgadmin).

Default: `admin`

### `PGADMIN_HOST_ADDRESS`

The [IP address](./computer-networks.md#ip-address) exposed on the [host](./computer-networks.md#host). [`0.0.0.0`](./computer-networks.md#0000) accepts connections from any network interface.

Default: `0.0.0.0`

### `PGADMIN_HOST_PORT`

The [port number](./computer-networks.md#port-number) exposed on the [host](./computer-networks.md#host) for accessing [`pgAdmin`](./pgadmin.md#what-is-pgadmin).

Default: `42003`

## `caddy`

Variables for the [`caddy` service](./docker-compose-yml.md#caddy-service).

### `CADDY_CONTAINER_PORT`

The [port number](./computer-networks.md#port-number) that [`Caddy`](./caddy.md#what-is-caddy) [listens on](./computer-networks.md#listen-on-a-port) inside the [container](./docker.md#container).

Default: `80`

### `CADDY_HOST_ADDRESS`

The [IP address](./computer-networks.md#ip-address) exposed on the [host](./computer-networks.md#host). [`0.0.0.0`](./computer-networks.md#0000) accepts connections from any network interface.

Default: `0.0.0.0`

### `CADDY_HOST_PORT`

The [port number](./computer-networks.md#port-number) exposed on the [host](./computer-networks.md#host) for accessing [`Caddy`](./caddy.md#what-is-caddy).

Default: `42002`

## Constants

Values that should not be changed. They are defined here for convenient referencing in [`docker-compose.yml`](../docker-compose.yml).

### `CONST_POSTGRESQL_SERVICE_NAME`

The [`Docker Compose` service name](./docker-compose.md#service-name) for [`PostgreSQL`](./database.md#postgresql). Other [services](./docker-compose.md#service) use this name to connect to the database via [`Docker Compose` networking](./docker-compose.md#docker-compose-networking).

Default: `postgres`

### `CONST_POSTGRESQL_SERVER_NAME`

The display name for the [`PostgreSQL`](./database.md#postgresql) server in [`pgAdmin`](./pgadmin.md#what-is-pgadmin).

Default: `postgres-lab-4`

### `CONST_POSTGRESQL_DEFAULT_PORT`

The default [port number](./computer-networks.md#port-number) [`PostgreSQL`](./database.md#postgresql) [listens on](./computer-networks.md#listen-on-a-port) inside the [container](./docker.md#container).

Default: `5432`
