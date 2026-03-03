# `PostgreSQL` with `Docker`

<h2>Table of contents</h2>

- [What is `PostgreSQL` with `Docker`](#what-is-postgresql-with-docker)
- [Resetting the database](#resetting-the-database)

## What is `PostgreSQL` with `Docker`

<!-- TODO better section name -->

This wiki covers managing the `PostgreSQL` [container](./docker.md#container) in this project.

See also:

- [`Database`](./database.md#what-is-a-database) for database concepts.
- [`Docker Compose`](./docker-compose.md#what-is-docker-compose) for general `Docker Compose` commands.

## Resetting the database

The database is initialized from the file [`backend/app/data/init.sql`](../backend/app/data/init.sql) on the first start of the container with `PostgreSQL` (see the [service](./docker-compose.md#service) `postgres` in [`docker-compose.yml`](../docker-compose.yml)).

To reset the database to its initial state:

1. To stop the `postgres` service and remove its [volume](./docker-compose.md#volume),

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret down postgres -v
   ```

2. To re-create the database from [`init.sql`](../backend/app/data/init.sql),

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret up postgres --build
   ```
