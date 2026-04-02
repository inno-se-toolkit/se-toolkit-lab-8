# Web API

<h2>Table of contents</h2>

- [What is a web API](#what-is-a-web-api)
- [Endpoint](#endpoint)
- [Resource](#resource)
- [Base URL](#base-url)
- [API key](#api-key)
  - [`<api-key>` placeholder](#api-key-placeholder)
- [API key rules](#api-key-rules)
  - [API key format](#api-key-format)
- [API types](#api-types)
  - [`HTTP` API](#http-api)

## What is a web API

A web API is an [API](./api.md#what-is-an-api) that a [web server](./web-infrastructure.md#web-server) exposes over a [protocol](./computer-networks.md#protocol). It accepts requests from [web clients](./web-infrastructure.md#web-client) and returns structured responses.

Docs:

- [An introduction to APIs: A comprehensive guide](https://zapier.com/blog/api/)
- [Introduction to web APIs](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Client-side_APIs/Introduction)

## Endpoint

An endpoint is a specific entry point of a [web API](#what-is-a-web-api), identified by a path (`/status`, `/items`, ...).

In a [`REST` API](./rest-api.md#what-is-a-rest-api), the [`HTTP` method](./http.md#http-request-method) is also part of the identity — `GET /status` and `POST /status` are different endpoints.

## Resource

A resource is an entity or piece of data that a [web API](#what-is-a-web-api) exposes to [clients](./web-infrastructure.md#web-client).

Each resource is identified by a path in an [endpoint](#endpoint) — for example, `/items` refers to a collection of items and `/items/{id}` refers to a single item.

## Base URL

The base [URL](./computer-networks.md#url) is the common prefix shared by all [endpoints](#endpoint) of a [web API](#what-is-a-web-api). It identifies the server and, optionally, a path prefix such as a version segment.

To form a complete request URL, append an endpoint path to the base URL:

| Part     | Example                            |
| -------- | ---------------------------------- |
| Base URL | `https://api.example.com/v1`       |
| Endpoint | `/items`                           |
| Full URL | `https://api.example.com/v1/items` |

## API key

An API key is a secret value used to [authenticate](./http-auth.md#http-authentication) a [client](./web-infrastructure.md#web-client) making requests to a [web API](#what-is-a-web-api).

### `<api-key>` placeholder

[API key](#api-key) (without `<` and `>`).

## API key rules

The [API key](#api-key) must be:

- an arbitrary string that follows the [API key format](#api-key-format)

- be designed by you unless it's explicitly stated that you must obtain it by an external provider.

- kept secret so that other people can't use your [API](#web-api) without your permission

### API key format

> [!NOTE]
> The goal is to make the key:
>
> - easy to remember
>
> - compatible with apps that use it

The API key string must:

- start and end with a lowercase latin letter (`a` to `z`)

- include only these characters:

  - lowercase latin letters (`a` to `z`)

  - minus (`-`)

Example:

- `a-tiny-secret-key`

## API types

A [web API](#what-is-a-web-api) is built on top of a [protocol](./computer-networks.md#protocol).

Common API types:

- [`HTTP` API](#http-api)
- [`REST` API](./rest-api.md#what-is-a-rest-api)

### `HTTP` API

An `HTTP` API is a [web API](#what-is-a-web-api) that uses the [`HTTP` protocol](./http.md#what-is-http) to accept requests and return responses.

It has no rules about URL structure or how [`HTTP` methods](./http.md#http-request-method) are used — any path and method combination is valid.
