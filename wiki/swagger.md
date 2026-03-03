# `Swagger UI`

<h2>Table of contents</h2>

- [What is `Swagger UI`](#what-is-swagger-ui)
- [Open `Swagger UI`](#open-swagger-ui)
- [Authorize in `Swagger UI`](#authorize-in-swagger-ui)
- [Try an endpoint in `Swagger UI`](#try-an-endpoint-in-swagger-ui)

## What is `Swagger UI`

`Swagger UI` is an interactive web page that lets you explore and test a [REST API](./api.md#rest-api).

`FastAPI` auto-generates `Swagger UI` at the `/docs` path.

Actions:

- [What is `Swagger UI`](#what-is-swagger-ui)
- [Open `Swagger UI`](#open-swagger-ui)
- [Authorize in `Swagger UI`](#authorize-in-swagger-ui)
- [Try an endpoint in `Swagger UI`](#try-an-endpoint-in-swagger-ui)

## Open `Swagger UI`

**Locally** (services running on your machine):

1. Open <http://127.0.0.1:42001/docs> in a browser.

**On a deployed VM:**

1. Open in a browser: `http://<your-vm-ip-address>:<caddy-port>/docs`. Replace:

   - [`<your-vm-ip-address>`](./vm.md#your-vm-ip-address)
   - [`<caddy-port>`](./caddy.md#caddy-port)

## Authorize in `Swagger UI`

If the API requires authentication:

1. [Open `Swagger UI`](#open-swagger-ui).
2. Click the `Authorize` button (lock icon at the top right).
3. In the `Value` field, enter the [`<api-key>`](./api.md#api-key).
4. Click `Authorize`.
5. Click `Close`.

All subsequent requests will include the API key in the `Authorization` header.

## Try an endpoint in `Swagger UI`

1. [Open `Swagger UI`](#open-swagger-ui).
2. Click on an endpoint (e.g., `GET /items`).
3. Click `Try it out`.
4. Fill in parameters if needed.
5. Click `Execute`.
6. See the response below: status code, response body, headers.
