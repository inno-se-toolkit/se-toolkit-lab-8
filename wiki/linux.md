# `Linux`

<h2>Table of contents</h2>

- [What is `Linux`](#what-is-linux)
- [User](#user)
- [Group](#group)
  - [The `root` user](#the-root-user)
  - [A non-root user](#a-non-root-user)
- [Permissions](#permissions)
- [`Linux` administration](#linux-administration)
  - [Get my current user](#get-my-current-user)
  - [The `sudo` command](#the-sudo-command)
  - [Create a non-root user](#create-a-non-root-user)
  - [Inspect ports](#inspect-ports)
    - [See listening TCP ports](#see-listening-tcp-ports)
    - [Inspect a specific port](#inspect-a-specific-port)
  - [Troubleshooting](#troubleshooting)
    - [Service is running but a request fails](#service-is-running-but-a-request-fails)

## What is `Linux`

`Linux` is a family of [operating systems](./operating-system.md) commonly used for servers and [virtual machines](./vm.md).

There are multiple [`Linux` distros](./linux-distros.md#what-is-a-linux-distro).

## User

See [User](./operating-system.md#user).

## Group

See [Group](./operating-system.md#group).

### The `root` user

`root` is the administrator [user](#user).

### A non-root user

<!-- TODO -->

## Permissions

<!-- TODO -->

## `Linux` administration

`Linux` administration covers system-level tasks such as managing [users](./operating-system.md#user), [groups](./operating-system.md#group), and permissions on a [`Linux`](./linux.md#what-is-linux) system.

### Get my current user

1. To get the current user,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   whoami
   ```

### The `sudo` command

`sudo` runs a command with elevated permissions.

To run a command with elevated permissions,

[run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

```terminal
sudo <command>
```

### Create a non-root user

`root` is useful for initial setup, but daily work should be done with a regular user.

For `Ubuntu`/`Debian` systems:

1. To create a new user,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   sudo adduser <username>
   ```

2. To allow the user to run administrative commands,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   sudo usermod -aG sudo <username>
   ```

3. To switch to that user,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   su - <username>
   ```

4. To verify the current user,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   whoami
   id
   ```

If you plan to log in via `SSH` as that user, copy `authorized_keys` to the new user's home and fix permissions before logging out from `root`.

### Inspect ports

Use the following commands to inspect [ports](./computer-networks.md#port) on a [host](./computer-networks.md#host).

- [See listening TCP ports](#see-listening-tcp-ports)
- [Inspect a specific port](#inspect-a-specific-port)

#### See listening TCP ports

To see all listening TCP ports,

[run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

```terminal
ss -ltn
```

#### Inspect a specific port

To inspect a specific port,

[run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

```terminal
ss -ltn 'sport = :42000'
```

### Troubleshooting

#### Service is running but a request fails

Verify both:

1. The process is listening on the expected port.
2. You are using the correct host and port in your request.
