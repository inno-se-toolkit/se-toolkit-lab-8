# LMS API

<h2>Table of contents</h2>

- [About the LMS API](#about-the-lms-api)
- [LMS API key](#lms-api-key)
  - [`<lms-api-key>` placeholder](#lms-api-key-placeholder)

## About the LMS API

The LMS API (Learning Management System API) is a [web API](./web-api.md#what-is-a-web-api) built with [`FastAPI`](https://fastapi.tiangolo.com/) that provides [endpoints](./web-api.md#endpoint) for managing learning data.

The [LMS frontend](./lms-client-web-react.md#about-the-lms-frontend) uses the LMS API to display items and dashboard charts.
[`Caddy`](./gateway.md#caddy) serves as a [reverse proxy](./web-infrastructure.md#reverse-proxy) that [forwards requests to the backend](./gateway.md#forward-requests-to-the-backend).

Docs:

- [`FastAPI`](https://fastapi.tiangolo.com/)

## LMS API key

The [API key](./web-api.md#api-key) that is used to authorize requests to the [LMS API](#about-the-lms-api) in:

- The [`Swagger UI`](./swagger.md#authorize-in-swagger-ui)
- The [LMS frontend](./lms-client-web-react.md#authentication)

The key must follow the [API key rules](./web-api.md#api-key-rules).

You store the key in [`LMS_API_KEY`](./dotenv-docker-secret.md#lms_api_key) in [`.env.docker.secret`](./dotenv-docker-secret.md#what-is-envdockersecret).

### `<lms-api-key>` placeholder

The [LMS API key](#lms-api-key) (without `<` and `>`).
