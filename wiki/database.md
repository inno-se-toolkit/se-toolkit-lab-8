# Database

<h2>Table of contents</h2>

- [What is a database](#what-is-a-database)
- [Database server](#database-server)
- [`PostgreSQL`](#postgresql)
- [`pgAdmin`](#pgadmin)
- [`SQL`](#sql)
- [Database schema](#database-schema)
- [Database row](#database-row)
- [ERD](#erd)
  - [ERD notations](#erd-notations)
    - [ERD in Chen notation](#erd-in-chen-notation)
    - [ERD in crow's foot notation](#erd-in-crows-foot-notation)
- [EERD](#eerd)

## What is a database

A database is an organized collection of data that can be accessed, managed, and updated.

Databases store data in structures such as tables (rows and columns).

## Database server

A database server is software that manages one or more databases and handles queries from clients (applications).

Examples of database servers: [`PostgreSQL`](./postgresql.md#what-is-postgresql), `MySQL`, `SQLite`.

## `PostgreSQL`

[`PostgreSQL`](./postgresql.md#what-is-postgresql) is a popular open-source relational database server.

Docs:

- [Official PostgreSQL docs](https://www.postgresql.org/docs/)

<!-- TODO move to postgres.md -->
<!-- TODO update docker-postgres to reference postgres.md -->

## `pgAdmin`

See [`pgAdmin`](./pgadmin.md#what-is-pgadmin).

## `SQL`

See [`SQL`](./sql.md#what-is-sql).

## Database schema

The database schema defines the structure of the database: tables, columns, data types, and constraints.

You can [inspect columns](./pgadmin.md#browse-columns-in-the-table) of a table in [`pgAdmin`](./pgadmin.md#what-is-pgadmin).

> [!NOTE]
> The column names in the database must match the field names in the [`Python`](./python.md#what-is-python) code.
> If they don't match, the application will fail to read data from the database.

## Database row

<!-- TODO -->

## ERD

ERD (Entity-relationship diagram) is a visual representation of a data model.

<!-- TODO improve description -->

### ERD notations

#### ERD in Chen notation

See [Chen notation](https://www.red-gate.com/blog/chen-erd-notation/).

#### ERD in crow's foot notation

See [Crow’s Foot Notation](https://www.red-gate.com/blog/crow-s-foot-notation/).

## EERD

<!-- TODO add section content -->