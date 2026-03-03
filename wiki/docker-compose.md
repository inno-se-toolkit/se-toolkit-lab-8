# `Docker Compose`

<h2>Table of contents</h2>

- [What is `Docker Compose`](#what-is-docker-compose)
- [`docker-compose.yml`](#docker-composeyml)
- [Service](#service)
  - [Service name](#service-name)
- [`Docker Compose` networking](#docker-compose-networking)
- [Volume](#volume)
- [Health checks](#health-checks)
- [Actions](#actions)
  - [Stop and remove all containers](#stop-and-remove-all-containers)
  - [Stop and remove all containers and volumes](#stop-and-remove-all-containers-and-volumes)
  - [Stop and remove all containers, volumes, and images](#stop-and-remove-all-containers-volumes-and-images)

## What is `Docker Compose`

`Docker Compose` runs multi-container apps from a [`docker-compose.yml`](#docker-composeyml) file.

Example of the file: [`docker-compose.yml`](../docker-compose.yml).

See also:

- [`Docker`](./docker.md) for general `Docker` concepts ([images](./docker.md#image), [containers](./docker.md#container), etc.).

## `docker-compose.yml`

## Service

A service is a named entry under the `services:` key in [`docker-compose.yml`](#docker-composeyml). It defines how to build or pull an [image](./docker.md#image) and run it as a [container](./docker.md#container).

For example, this project defines four services in [`docker-compose.yml`](../docker-compose.yml): `app`, `postgres`, `pgadmin`, and `caddy`.

### Service name

<!-- TODO -->

## `Docker Compose` networking

`Docker Compose` creates a [network](./computer-networks.md#what-is-a-network) where [services](#service) can reach each other by their [service name](#service-name).

Docs:

- [Networking in Compose](https://docs.docker.com/compose/how-tos/networking/)

## Volume

A volume is persistent storage managed by `Docker`. Data in a volume survives [container](./docker.md#container) restarts.

Volumes are defined in [`docker-compose.yml`](#docker-composeyml):

```yaml
volumes:
  postgres_data:
```

A [service](#service) can mount a volume to store data:

```yaml
services:
  postgres:
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

## Health checks

A health check is a command that `Docker` runs periodically to check if a [container](./docker.md#container) is healthy.

Other [services](#service) can wait for a container to be healthy before starting:

```yaml
services:
  app:
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```

## Actions

<!-- TODO all - not globally -->

### Stop and remove all containers

1. To stop all running [services](#service) and remove [containers](./docker.md#container),

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret down
   ```

### Stop and remove all containers and volumes

1. To stop all running [services](#service), remove [containers](./docker.md#container), and remove [volumes](#volume),

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret down -v
   ```

### Stop and remove all containers, volumes, and images

1. To stop all running [services](#service), remove [containers](./docker.md#container), remove [volumes](#volume), and remove [images](./docker.md#image),

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret down -v --rmi all
   ```
