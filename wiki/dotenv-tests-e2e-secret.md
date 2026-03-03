# `.env.tests.e2e.secret`

- [What is `.env.tests.e2e.secret`](#what-is-envtestse2esecret)
- [`API_BASE_URL`](#api_base_url)
- [`API_KEY`](#api_key)

## What is `.env.tests.e2e.secret`

`.env.tests.e2e.secret` is an [`.env` file](./environments.md#env-file) that stores [environment variables](./environments.md#environment-variable) for running [end-to-end tests](./testing.md#end-to-end-tests).

Default values: [`.env.tests.e2e.example`](../.env.tests.e2e.example)

> It was added to [`.gitignore`](./git.md#gitignore) because it may contain [secrets](./environments.md#secrets) such as the [API key](#api_key) or the [VM IP address](./vm.md#your-vm-ip-address).

## `API_BASE_URL`

The base [URL](./web-development.md#url) of the deployed API.

Example: `http://10.93.24.1:42002`

## `API_KEY`

The secret key used to authorize [API](./api.md#what-is-an-api) requests. Must match [`API_KEY`](./dotenv-docker-secret.md#api_key) in [`.env.docker.secret`](./dotenv-docker-secret.md#what-is-envdockersecret) on the VM.
