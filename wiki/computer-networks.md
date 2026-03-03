# Computer networks

<h2>Table of contents</h2>

- [What is a network](#what-is-a-network)
- [Machine](#machine)
- [Internet](#internet)
- [IP address](#ip-address)
  - [IPv4](#ipv4)
  - [IPv6](#ipv6)
- [Host](#host)
  - [Hostname](#hostname)
    - [`localhost`](#localhost)
    - [`127.0.0.1`](#127001)
    - [`0.0.0.0`](#0000)
  - [Remote host](#remote-host)
- [Port](#port)
  - [Port number](#port-number)
  - [System port](#system-port)
  - [User port](#user-port)
  - [Listen on a port](#listen-on-a-port)
- [`Wi-Fi`](#wi-fi)
  - [`Wi-Fi` network](#wi-fi-network)
- [Reverse proxy](#reverse-proxy)
  - [Forward request](#forward-request)

## What is a network

A network (formally "computer network") is a group of interconnected [machines](#machine) that can communicate and share resources over wired or wireless connections.

## Machine

A machine is a physical or virtual computer.

Examples: a personal laptop, a university server, a [virtual machine](./vm.md#what-is-a-vm).

## Internet

The Internet is a global [network](#what-is-a-network) that connects millions of smaller networks worldwide.

It uses standardized communication protocols (such as `TCP/IP`) to link billions of devices, enabling communication and access to information across the globe.

## IP address

An IP address (Internet Protocol address) is a numerical label assigned to each device connected to a [network](#what-is-a-network).

It identifies the device and its location in the network.

Example: `10.93.24.1` ([IPv4](#ipv4)).

### IPv4

`IPv4` (Internet Protocol version 4) uses 32-bit addresses, written as four decimal numbers separated by dots.

Example: `10.93.24.1`, `127.0.0.1`.

It supports approximately 4.3 billion unique addresses.

### IPv6

`IPv6` (Internet Protocol version 6) uses 128-bit addresses, written as eight groups of four hexadecimal digits separated by colons.

Example: `2001:db8::1`.

It was introduced to address the exhaustion of [IPv4](#ipv4) addresses and supports a vastly larger address space.

## Host

A host is any [machine](#machine) that:

- is connected to a [network](#what-is-a-network);
- has an [IP address](#ip-address).

Hosts can send and receive data over the network.

Examples: computers, servers, [virtual machines](./vm.md#what-is-a-vm).

### Hostname

A hostname is a human-readable label assigned to a [host](#host) on a [network](#what-is-a-network).

It is used to identify the host instead of its [IP address](#ip-address).

Examples: [`localhost`](#localhost), `my-server`, [`vm.innopolis.university`](./vm.md#go-to-the-vms-site).

#### `localhost`

`localhost` is a [hostname](#hostname) that refers to the current [host](#host).

It resolves to the loopback [IP address](#ip-address) `127.0.0.1`.

Connections to `localhost` never leave the host — they are handled entirely within the [operating system](./operating-system.md#what-is-an-operating-system).

#### `127.0.0.1`

`127.0.0.1` is the loopback [IP address](#ip-address). [`localhost`](#localhost) resolves to this address.

#### `0.0.0.0`

`0.0.0.0` is a special [IP address](#ip-address) that means "all network interfaces on this [host](#host)."

When a [process](./operating-system.md#process) that [listens on a port](#listen-on-a-port) is bound to `0.0.0.0`, it accepts connections from any network interface — including [`localhost`](#localhost) and external networks. In contrast, binding to `127.0.0.1` restricts connections to the local host only.

This is commonly used to make a service accessible from outside the [machine](#machine) (e.g., from your laptop to a [virtual machine](./vm.md#what-is-a-vm)).

### Remote host

A remote [host](#host) is a host that is not the [local host](#localhost) — it is accessed over a [network](#what-is-a-network).

Example: [your VM](./vm.md#your-vm) you connect to via [`SSH`](./ssh.md#what-is-ssh) is a remote host.

## Port

A [*network port*](https://en.wikipedia.org/wiki/Port_(computer_networking)) (or simply *port*) is a [numbered](#port-number) communication endpoint on a [host](#host).

### Port number

A port number is a numerical identifier used in networking to distinguish between different [processes](./operating-system.md#process) running on a single [host](#host).

Only one process can bind to a specific port number on a given network interface.

### System port

The port numbers in the range from 0 to 1023 are the **well-known ports** or **system ports**.
They are used by system processes that provide widely used types of network services.
[[source](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers#Well-known_ports)]

### User port

A **user port** (or **registered port**) is a [network port](#port) designated for use with a certain protocol or application.
[[source](https://en.wikipedia.org/wiki/Registered_port)]

### Listen on a port

When a [process](./operating-system.md#process) "listens on a port", it means the process has bound itself to a specific [network port number](#port-number) and is waiting for incoming network connections on that [port](#port).

The [operating system](./operating-system.md#what-is-an-operating-system) allocates the port to that process, and any incoming network traffic directed to that port will be handled by the listening process.

This is how [services](./operating-system.md#service) like [web servers](./web-development.md#web-server), [`SSH` daemons](./ssh.md#ssh-daemon), or [databases](./database.md#what-is-a-database) accept connections from [clients](./web-development.md#web-client).

A port can only be listened on by one process at a time.

## `Wi-Fi`

`Wi-Fi` is a wireless technology that allows [machines](#machine) to connect to a [network](#what-is-a-network) without physical cables.

It uses radio waves to transmit data between devices and a wireless access point (a router).

### `Wi-Fi` network

A `Wi-Fi` network is a [network](#what-is-a-network) that [machines](#machine) connect to using [`Wi-Fi`](#wi-fi).

Each `Wi-Fi` network has a name (called SSID) that identifies it to nearby devices.

Example: `UniversityStudent`, `Home_Network`.

## Reverse proxy

A reverse proxy is a server that sits in front of a backend [service](./web-development.md#service) and forwards incoming client requests to it.

<!-- TODO update -->

### Forward request

<!-- TODO add section content -->