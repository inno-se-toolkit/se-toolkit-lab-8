# Web development

<h2>Table of contents</h2>

- [Web server and web client](#web-server-and-web-client)
  - [Web server](#web-server)
  - [Web client](#web-client)
- [Backend](#backend)
- [Frontend](#frontend)
- [Protocol](#protocol)
- [Data format](#data-format)
  - [`JSON`](#json)
    - [`JSON` data types](#json-data-types)
    - [Example of `JSON` data](#example-of-json-data)
  - [`Protobuf`](#protobuf)
- [Send a `GET` request](#send-a-get-request)
  - [Send a `GET` request using a browser](#send-a-get-request-using-a-browser)
  - [Send a `GET` request using `curl`](#send-a-get-request-using-curl)
- [Pretty-print the `JSON` response](#pretty-print-the-json-response)
  - [Pretty-print the `JSON` response using `jq`](#pretty-print-the-json-response-using-jq)
  - [Pretty-print the `JSON` response using a browser](#pretty-print-the-json-response-using-a-browser)
- [URL](#url)
  - [Purpose](#purpose)
  - [Components of a URL](#components-of-a-url)
  - [URL example](#url-example)
- [Service](#service)
- [Feature flag](#feature-flag)
- [HTML](#html)
- [CSS](#css)
- [JavaScript](#javascript)
- [CDN](#cdn)

## Web server and web client

### Web server

A web server is software that delivers content or services to [web clients](#web-client) over the [Internet](./computer-networks.md#internet) using a [protocol](#protocol).

> [!NOTE]
> We refer to a web server as software only.
>
> Other sources may refer to it as hardware too.
>
> Example: [What is a web server](https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_web_server).

### Web client

A web client is software that requests content from a [web server](#web-server) and displays the received content.

Web clients include browsers (`Chrome`, `Firefox`) and command-line tools ([`curl`](#send-a-get-request-using-curl)).

## Backend

<!-- TODO -->

## Frontend

<!-- TODO -->

## Protocol

A protocol is a set of rules that define how data is transmitted and received over a network. In web development, protocols govern communication between [web servers and web clients](#web-server-and-web-client).

## Data format

### `JSON`

`JSON` (`JavaScript Object Notation`) is a lightweight, text-based data interchange format that is easy for humans to read and write, and easy for machines to parse and generate.

It is language-independent but derived from `JavaScript` and commonly used in web applications to transmit data between a [server and a client](#web-server-and-web-client).

See [Learn `JSON` in Y minutes](https://learnxinyminutes.com/json/).

#### `JSON` data types

`JSON` supports basic data types like strings, numbers, booleans, arrays, and objects, making it ideal for representing structured data. Its simplicity and compatibility with most programming languages have made it the de facto standard for API responses and configuration files.

#### Example of `JSON` data

```json
{
  "name": "John Doe",
  "age": 35,
  "active": true,
  "skills": ["Python", "JavaScript", "Go"]
}
```

### `Protobuf`

`Protobuf` (`Protocol Buffers`) is a binary serialization format developed by `Google` for structured data exchange between applications. It's a language-neutral, platform-neutral mechanism for serializing structured data, similar to `XML` or `JSON` but more compact and faster.

`Protobuf` uses `.proto` files to define data structures, which are then compiled into language-specific classes for various programming languages. It's commonly used in microservices architectures and API communications where efficiency and schema evolution are important.

## Send a `GET` request

### Send a `GET` request using a browser

1. Open the URL in a browser.

   The browser will send the `GET` query by default.

### Send a `GET` request using `curl`

See [`curl`](./useful-programs.md#send-a-get-request-with-curl).

## Pretty-print the `JSON` response

### Pretty-print the `JSON` response using `jq`

1. [Install `jq`](./useful-programs.md#jq) if not installed.
2. To pretty-print the `JSON` response,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   <command-that-produces-json-response> | jq .
   ```

   [Pipe the output](./bash.md#pipe-the-stdout) to `jq`.

Example:

```terminal
curl -s https://jsonplaceholder.typicode.com/todos/1 | jq .
```

### Pretty-print the `JSON` response using a browser

`Chrome`:

1. click `Pretty-print`.

`Firefox`:

1. Click `Raw Data`.
2. Click `Pretty Print`.

<!-- TODO other browsers -->

## URL

<!-- TODO move to computer networks -->

A URL (`Uniform Resource Locator`) is a reference or address used to identify and locate resources on the Internet. It's commonly known as a "web address" and specifies the location of a resource on a web server as well as the protocol used to access it.

### Purpose

URLs are used by web browsers and other applications to retrieve resources like web pages, images, videos, and API endpoints. They provide a standardized way to locate and access resources across the Internet.

### Components of a URL

A typical URL consists of several components:

- **Scheme/Protocol**: Specifies how to access the resource (e.g., `http`, `https`, `ftp`).
- **[Host](./computer-networks.md#host)/Domain**: The server where the resource is located (e.g., `www.example.com`).
- **[Port](./computer-networks.md#port)** (optional): The specific port number on the server (e.g., `:8080`).
- **Path**: The location of the specific resource on the server (e.g., `/folder/page.html`).
- **Query parameters** (optional): Additional data passed to the server (e.g., `?param1=value1&param2=value2`).
- **Fragment** (optional): Points to a specific section within the resource (e.g., `#section1`).

### URL example

```text
https://www.example.com:8080/search?q=cats&page=1#results
```

Where:

- Scheme: `https`
- Host: `www.example.com`
- Port: `8080`
- Path: `/search`
- Query: `?q=cats&page=1`
- Fragment: `#results`

## Service

A service is an application (or part of a system) that exposes endpoints and performs a focused responsibility.

Examples:

- Course materials service.
- Authentication service.
- Recommendation service.

A service can call other services over the network, but to the client it still appears as endpoints that return responses.

## Feature flag

A feature flag (also called a feature toggle) is a mechanism that enables or disables a feature at runtime without deploying new code. Feature flags let teams decouple deployment from release, enabling gradual rollouts, `A/B` testing, and quick rollbacks.

## HTML

`HTML` (`HyperText Markup Language`) is the standard language for structuring content on the web. An `HTML` file defines the structure and content of a web page using tags.

## CSS

`CSS` (`Cascading Style Sheets`) is a language for styling `HTML` content — controlling layout, colors, fonts, and other visual properties.

## JavaScript

`JavaScript` is a programming language that runs in the browser and makes web pages interactive. It can update content, respond to events, and communicate with servers.

## CDN

A `CDN` (`Content Delivery Network`) is a network of distributed servers that delivers static files (such as `HTML`, `CSS`, and `JavaScript`) to users from a location close to them. Serving files from a `CDN` reduces load on the origin server and improves response time.
