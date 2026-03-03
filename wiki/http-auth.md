# HTTP authentication and authorization

<h2>Table of contents</h2>

- [HTTP authentication](#http-authentication)
- [HTTP authorization](#http-authorization)

## HTTP authentication

Authentication is the process of verifying the identity of a client making a request to an [API](./api.md#what-is-an-api).

In `HTTP` APIs, a common mechanism is an **API key** — a secret value the client sends with each request. The server checks the key and rejects unknown keys with `401 Unauthorized`.

The API key is sent in the `Authorization` header:

```http
Authorization: Bearer <api-key>
```

See [`<api-key>`](./api.md#api-key).

Docs:

- [HTTP authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication)

## HTTP authorization

Authorization is the process of determining whether an authenticated client has permission to access a specific [endpoint](./api.md#endpoint) or resource.

A client can be authenticated (identity verified) but still lack permission for certain resources.

Common `HTTP` status codes related to auth:

- [`401` (Unauthorized)](./http.md#401-unauthorized) — the client is not authenticated (missing or invalid API key).
- [`403` (Forbidden)](./http.md#403-forbidden) — the client is authenticated but not allowed to access this resource.
