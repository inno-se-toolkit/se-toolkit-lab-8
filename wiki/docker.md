# `Docker`

<h2>Table of contents</h2>

- [What is `Docker`](#what-is-docker)
- [Image](#image)
- [Container](#container)
  - [Why containers are useful](#why-containers-are-useful)
  - [Containers and host](#containers-and-host)
  - [Container ID](#container-id)
- [`DockerHub`](#dockerhub)
  - [`<your-dockerhub-username>`](#your-dockerhub-username)
- [Common `Docker` commands](#common-docker-commands)
  - [`docker run`](#docker-run)
    - [`docker run` typical pattern](#docker-run-typical-pattern)
    - [`docker run` useful flags](#docker-run-useful-flags)
  - [`docker ps`](#docker-ps)
    - [`docker ps` useful variants](#docker-ps-useful-variants)
- [Set up `Docker`](#set-up-docker)
  - [Install `Docker`](#install-docker)
  - [Start `Docker`](#start-docker)
  - [Remove all containers](#remove-all-containers)
- [Remove the container running at the port](#remove-the-container-running-at-the-port)
- [Troubleshooting](#troubleshooting)
  - [Image pull fails](#image-pull-fails)
  - [Port conflict (`port is already allocated`)](#port-conflict-port-is-already-allocated)
  - [DNS resolution errors (`getaddrinfo EAI_AGAIN`)](#dns-resolution-errors-getaddrinfo-eai_again)

## What is `Docker`

`Docker` is a platform for building and running [containers](#container).

Docs:

- [What is Docker?](https://docs.docker.com/get-started/docker-overview/)

## Image

An image is a packaged, read-only snapshot of an application and everything needed to run it — the OS files, runtime, libraries, and application code. The same image runs identically on any machine with `Docker` installed.

Running an image creates a [container](#container). One image can produce many containers.

## Container

A container is an isolated runtime for an application and its dependencies.

- A **runtime** is the software environment that executes the app: OS files, interpreter, system libraries.
- **Dependencies** are other software the app needs, such as a specific language version or a database driver.
- **Isolated** means each container has its own filesystem, processes, and network — it cannot affect other containers or the host machine.

### Why containers are useful

- The app runs consistently across machines.
- Dependencies are packaged with the app.
- Multiple services can run side-by-side with explicit ports and networks.

### Containers and host

<img alt="Containers and host" src="./images/docker/hierarchy.png" style="width:400px"></img>

[[source](https://rest-apis-flask.teclado.com/docs/docker_intro/what_is_docker_container/)]

### Container ID

A container ID is a unique string that `Docker` assigns to each [container](#container) when it is created.

`Docker` commands use the container ID (or its short prefix) to target a specific container — for example, to stop or inspect it.

You can view container IDs with [`docker ps`](#docker-ps).

For example:

```terminal
CONTAINER ID   IMAGE     ...
a3f5b9c2d1e4   my-app    ...
```

`a3f5b9c2d1e4` is the container ID (a short prefix of the full 64-character string).

## `DockerHub`

`DockerHub` is a public container registry where you can store and pull [Docker images](#image).

You can push a locally built image to `DockerHub` so that other machines (such as a VM) can pull and run it without building from source.

Docs:

- [`DockerHub`](https://hub.docker.com/)

### `<your-dockerhub-username>`

Your [`DockerHub`](#dockerhub) username (without `<` and `>`).

## Common `Docker` commands

- [`docker run`](#docker-run)
- [`docker ps`](#docker-ps)

### `docker run`

`docker run` starts a container from an image.

#### `docker run` typical pattern

```terminal
docker run --name <container-name> -p <host-port>:<container-port> <image-name>
```

#### `docker run` useful flags

- `-d` - run in background (detached mode).
- `--rm` - remove container after it exits.
- `-e KEY=VALUE` - pass environment variable.

### `docker ps`

`docker ps` shows running containers.

#### `docker ps` useful variants

- `docker ps` - only running containers.
- `docker ps -a` - all containers (including stopped).

## Set up `Docker`

Complete these steps:

1. [Install `Docker`](#install-docker).
2. [Start `Docker`](#start-docker).
3. [Remove all containers](#remove-all-containers).

### Install `Docker`

Follow the [installation instructions](https://docs.docker.com/get-started/get-docker/).

### Start `Docker`

If you installed `Docker Desktop`:

1. Open `Docker Desktop`.
2. Skip login.
3. Wait until you see `Engine running`.

### Remove all containers

> [!NOTE]
> If there are permission errors, replace `docker` with `sudo docker`.

1. To stop all running containers,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker stop $(docker ps -q) 2>/dev/null
   ```

   You should see removed [container IDs](#container-id).

2. To remove all stopped containers,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker container prune -f
   ```

   The output should be empty or similar to this:

   ```terminal
   ...
   Total reclaimed space: ...
   ```

3. To delete unused [volumes](./docker-compose.md#volume),

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker volume prune -f --all
   ```

   The output should be similar to this:

   ```terminal
   ...
   Total reclaimed space: ...
   ```

## Remove the container running at the port

1. To find the [container](#container) occupying the port,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker ps --filter "publish=<port>"
   ```

   Replace the placeholder `<port>` with the port number from the error message.

   The output should be similar to this:

   ```terminal
   CONTAINER ID     IMAGE     COMMAND   ...   PORTS
   <container-id>   my-app    ...       ...   <host>:<port>->8000/tcp
   ```

   The `<container-id>` is a hash like `a3f5b9c2d1e4`.

2. To force-remove the container,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker rm -f <container-id>
   ```

   Replace the placeholder `<container-id>` with the [container ID](#container-id) from the previous step.

3. To remove the [volume](./docker-compose.md#volume) left by the removed container,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker volume prune -f --all
   ```

   The output should be similar to this:

   ```terminal
   ...
   Total reclaimed space: ...
   ```

## Troubleshooting

<!-- no toc -->
- [Image pull fails](#image-pull-fails)
- [Port conflict (`port is already allocated`)](#port-conflict-port-is-already-allocated)
- [DNS resolution errors (`getaddrinfo EAI_AGAIN`)](#dns-resolution-errors-getaddrinfo-eai_again)

### Image pull fails

Steps to fix:

1. [Connect to the correct network](./vm.md#connect-to-the-correct-network).

### Port conflict (`port is already allocated`)

If `docker compose up` fails with an error like `Bind for <host>:<port> failed: port is already allocated`,
probably a container from a previous run is still occupying that port.

Steps to fix:

1. [Remove the container running at the port](#remove-the-container-running-at-the-port).

### DNS resolution errors (`getaddrinfo EAI_AGAIN`)

If the build hangs or you see [DNS](./computer-networks.md#dns) errors like `getaddrinfo EAI_AGAIN registry.npmjs.org`, [`Docker`](./docker.md#what-is-docker) cannot resolve [domain names](./computer-networks.md#domain-name).
This is a university network DNS issue.

Steps to fix:

1. To create the docker daemon directory if it doesn't exist,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   sudo mkdir -p /etc/docker/
   ```
  
2. To add `Google` DNS to `Docker`:

   1. [Run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

      ```terminal
      echo '{"dns": ["8.8.8.8", "8.8.4.4"]}' \
      | jq . \
      | sudo tee /etc/docker/daemon.json
      ```

      The output should look like this:

      ```json
      {
        "dns": [
          "8.8.8.8",
          "8.8.4.4"
        ]
      }
      ```

   2. [Type the password for the user `<user>`](./vm-access.md#type-the-password-for-the-user-user-remote).

3. To restart the `docker` service,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   sudo systemctl restart docker
   ```
