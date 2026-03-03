# API

<h2>Table of contents</h2>

- [What is an API](#what-is-an-api)
- [Endpoint](#endpoint)
- [`REST` API](#rest-api)
- [Base URL](#base-url)
- [What is an API key](#what-is-an-api-key)
  - [`<api-key>`](#api-key)
- [`FastAPI`](#fastapi)

## What is an API

An API (`Application Programming Interface`) is a set of rules that lets programs communicate with each other.

A web API exposes [endpoints](#endpoint) that clients can call over `HTTP`.

Docs:

- [An introduction to APIs: A comprehensive guide](https://zapier.com/blog/api/)

## Endpoint

An endpoint is a specific [API](#what-is-an-api) entry point identified by:

- HTTP method (`GET`, `POST`, `PUT`, `DELETE`, ...).
- Path (`/status`, `/items`, ...).

Example:

- `GET /status` is one endpoint.
- `POST /status` is a different endpoint.

## `REST` API

A REST API (`Representational State Transfer`) is a style of API design that uses `HTTP` methods and noun-based resource paths.

Key principles:

- **Resources** are identified by paths: `/items`, `/learners`, `/interactions`.
- **`HTTP` methods** define the action:
  - `GET` — read a resource.
  - `POST` — create a new resource.
  - `PUT` — update an existing resource.
  - `DELETE` — remove a resource.
- **Status codes** indicate the result: `200`, `201`, `404`, etc.

Example:

| Action               | Method | Path           | Status code |
| -------------------- | ------ | -------------- | ----------- |
| List all items       | `GET`  | `/items`       | `200`       |
| Get one item         | `GET`  | `/items/{id}`  | `200`/`404` |
| Create an item       | `POST` | `/items`       | `201`       |
| Update an item       | `PUT`  | `/items/{id}`  | `200`/`404` |

## Base URL

<!-- TODO -->

## What is an API key

<!-- TODO -->

### `<api-key>`

The value that you use to authenticate in the API.

## `FastAPI`

<!-- TODO -->