# Observe the interaction of system components

<h4>Time</h4>

~25 min

<h4>Purpose</h4>

Trace a request from [`Swagger UI`](../../../wiki/swagger.md#what-is-swagger-ui) through the [API](../../../wiki/api.md#what-is-an-api) to the [database](../../../wiki/database.md#what-is-a-database) using the [browser developer tools](../../../wiki/browser-developer-tools.md#what-are-browser-developer-tools) and [`pgAdmin`](../../../wiki/pgadmin.md#what-is-pgadmin).

<h4>Context</h4>

Before adding new features, you will deploy the system to your VM and confirm it works.
Then you will send requests and observe how data flows through the components: browser → API → database.

<h4>Diagram</h4>

```mermaid
sequenceDiagram
    actor Developer
    participant Browser as "Browser (Swagger UI)"
    participant Caddy as "Caddy<br/>(Reverse Proxy)"
    participant API as "FastAPI<br/>(API Server)"
    participant DB as "PostgreSQL<br/>(Database)"
    participant pgAdmin as "pgAdmin<br/>(DB UI)"

    Note over Developer,pgAdmin: Task Flow: POST /learners/ → Verify in Database

    Developer->>Browser: Open Swagger UI<br/>http://<your-vm-ip-address>:<caddy-port>/docs
    Browser->>Caddy: GET /docs
    Caddy-->>Browser: Swagger UI HTML/JS

    Note over Developer,Browser: Authorize with API_KEY

    Developer->>Browser: POST /learners/<br/>{name: "John Doe", email: "john-doe@email.com"}
    Browser->>Caddy: POST /learners/<br/>Authorization: Bearer API_KEY
    Caddy->>API: Proxy POST /learners/

    API->>API: verify_api_key()
    API->>API: Validate request body<br/>(LearnerCreate)
    API->>DB: INSERT INTO learner<br/>(name, email)<br/>RETURNING *

    DB-->>API: New row:<br/>{id: 6, name: "John Doe",<br/>email: "john-doe@email.com",<br/>enrolled_at: ...}

    API-->>Caddy: 201 Created<br/>JSON response
    Caddy-->>Browser: 201 Created
    Browser-->>Developer: Display response

    Note over Developer,pgAdmin: Verification Flow: Check database in pgAdmin

    Developer->>pgAdmin: Open pgAdmin<br/>http://<your-vm-ip-address>:<pgadmin-port>
    Developer->>pgAdmin: Run SQL query:<br/>SELECT * FROM learner<br/>ORDER BY id DESC LIMIT 5
    pgAdmin->>DB: Execute SQL query
    DB-->>pgAdmin: Return rows of 'learner'
    pgAdmin-->>Developer: Display data output<br/>(CSV format)

    Note right of Developer: Verify: New row matches<br/>the Swagger UI response
```

See:

- [`<your-vm-ip-address>`](../../../wiki/vm.md#your-vm-ip-address)
- [`<caddy-port>`](../../../wiki/caddy.md#caddy-port)
- [`<pgadmin-port>`](../../../wiki/pgadmin.md#pgadmin-port)

<h4>Table of contents</h4>

- [1. Steps](#1-steps)
  - [1.1. Create a `Lab Task` issue](#11-create-a-lab-task-issue)
  - [1.2. Deploy the back-end to the VM](#12-deploy-the-back-end-to-the-vm)
    - [1.2.1. Connect and get the code](#121-connect-and-get-the-code)
    - [1.2.2. Prepare the environment](#122-prepare-the-environment)
    - [1.2.3. Start the services](#123-start-the-services)
  - [1.3. Open `Swagger UI`](#13-open-swagger-ui)
  - [1.4. Open the browser developer tools](#14-open-the-browser-developer-tools)
  - [1.5. Send a request using `Swagger UI`](#15-send-a-request-using-swagger-ui)
  - [1.6. Inspect the request using browser developer tools](#16-inspect-the-request-using-browser-developer-tools)
  - [1.7. Verify in `pgAdmin`](#17-verify-in-pgadmin)
  - [1.8. Send another request and check the database](#18-send-another-request-and-check-the-database)
  - [1.9. Write comments for the issue](#19-write-comments-for-the-issue)
    - [1.9.1. Comment 1: write the request as `fetch` code](#191-comment-1-write-the-request-as-fetch-code)
    - [1.9.2. Comment 2: write the response](#192-comment-2-write-the-response)
    - [1.9.3. Comment 3: attach the file with the data output from `pgAdmin`](#193-comment-3-attach-the-file-with-the-data-output-from-pgadmin)
    - [1.9.4. Comment 4: paste the ERD from `pgAdmin`](#194-comment-4-paste-the-erd-from-pgadmin)
  - [1.10. Close the issue](#110-close-the-issue)
- [2. Acceptance criteria](#2-acceptance-criteria)

## 1. Steps

### 1.1. Create a `Lab Task` issue

Title: `[Task] Observe System Component Interaction`

### 1.2. Deploy the back-end to the VM

<!-- no toc -->
- [1.2.1. Connect and get the code](#121-connect-and-get-the-code)
- [1.2.2. Prepare the environment](#122-prepare-the-environment)
- [1.2.3. Start the services](#123-start-the-services)

#### 1.2.1. Connect and get the code

1. [Connect to your VM](../../../wiki/vm.md#connect-to-the-vm).
2. To clone your fork on the VM (skip this step if already cloned),

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   git clone <your-fork-url> se-toolkit-lab-4
   ```

   Replace [`<your-fork-url>`](../../../wiki/github.md#your-fork-url).

3. To navigate to the project directory,

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   cd se-toolkit-lab-4
   ```

4. To pull the changes from your fork,

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   git pull
   ```

#### 1.2.2. Prepare the environment

1. [Clean up `Docker`](../../../wiki/docker.md#clean-up-docker).

2. To create the [`.env.docker.secret`](../../../wiki/dotenv-docker-secret.md#what-is-envdockersecret) file (if it does not exist),

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   cp .env.docker.example .env.docker.secret
   ```

#### 1.2.3. Start the services

1. To start the services in [background](../../../wiki/operating-system.md#background-process),

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret up --build -d
   ```

2. To check that the containers are running,

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret ps --format "table {{.Service}}\t{{.Status}}"
   ```

   You should see all four services running with the status `Up`:

   ```terminal
   SERVICE    STATUS
   app        Up 50 seconds
   caddy      Up 49 seconds
   pgadmin    Up 50 seconds
   postgres   Up 55 seconds (healthy)
   ```

   <!-- TODO link to this generic troubleshooting section in wiki -->

   <details><summary>Troubleshooting</summary>

   <h4>Port conflict (<code>port is already allocated</code>)</h4>

   [Clean up `Docker`](../../../wiki/docker.md#clean-up-docker), then run the `docker compose up` command again.

   <h4>Containers exit immediately</h4>

   To rebuild all containers from scratch,

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret down -v
   docker compose --env-file .env.docker.secret up --build -d
   ```

   </details>

### 1.3. Open `Swagger UI`

1. Open in a browser: `http://<your-vm-ip-address>:<caddy-port>/docs`. Replace:

   - [`<your-vm-ip-address>`](../../../wiki/vm.md#your-vm-ip-address)
   - [`<caddy-port>`](../../../wiki/caddy.md#caddy-port)

2. [Authorize](../../../wiki/swagger.md#authorize-in-swagger-ui) with [`API_KEY`](../../../wiki/dotenv-docker-secret.md#api_key) from [`.env.docker.secret`](../../../wiki/dotenv-docker-secret.md#what-is-envdockersecret).

   You should see the [`Swagger UI`](../../../wiki/swagger.md#swagger-ui) page with the [API](../../../wiki/api.md#what-is-an-api) documentation and available [endpoints](../../../wiki/api.md#endpoint).

   <!-- TODO write troubleshooting in wiki -->

   <details><summary>Troubleshooting</summary>

   <h4>Page does not load</h4>

   Verify that all [`Docker` containers](../../../wiki/docker.md#container) are running (see [1.2.3. Start the services](#123-start-the-services)).

   <h4>Authorization fails</h4>

   Check that the [`API_KEY`](../../../wiki/dotenv-docker-secret.md#api_key) value in [`.env.docker.secret`](../../../wiki/dotenv-docker-secret.md#what-is-envdockersecret) matches the one you entered in `Swagger UI`.

   </details>

### 1.4. Open the browser developer tools

> [!NOTE]
> See [What are browser developer tools](../../../wiki/browser-developer-tools.md#what-are-browser-developer-tools).

1. [Open the `Network` tab](../../../wiki/browser-developer-tools.md#open-the-network-tab).

### 1.5. Send a request using `Swagger UI`

1. In [`Swagger UI`](../../../wiki/swagger.md#what-is-swagger-ui), expand the `POST /learners/` endpoint.
2. Click `Try it out`.
3. Enter a [request payload](../../../wiki/http.md#http-request-payload) in [`JSON`](../../../wiki/file-formats.md#json) format, for example:

   ```json
   {
     "name": "John Doe",
     "email": "john-doe@email.com"
   }
   ```

4. Click `Execute`.

   In `Server response`, you should see:
   - `Code`: 201
   - `Details` -> `Response body`:

     ```json
     {
       "email": "john-doe@email.com",
       "id": 6,
       "enrolled_at": "2026-03-02 17:46:34.261004",
       "name": "John Doe"
     }
     ```

### 1.6. Inspect the request using browser developer tools

1. [Inspect the request to `/learners`](../../../wiki/browser-developer-tools.md#inspect-a-request).

   **Note:** you've already completed the initial steps.

   You should see headers, payload, response.

### 1.7. Verify in `pgAdmin`

> [!NOTE]
> The [API](../../../wiki/api.md#what-is-an-api) transformed the [`JSON`](../../../wiki/file-formats.md#json) from your request into a row in the `learner` table.

1. [Open `pgAdmin`](../../../wiki/pgadmin.md#open-pgadmin).
2. [Run a query](../../../wiki/pgadmin.md#run-the-query) on the `learner` table:

   ```sql
   SELECT * FROM learner ORDER BY id DESC LIMIT 5;
   ```

3. Verify that the data that you sent via [`Swagger UI`](../../../wiki/swagger.md#what-is-swagger-ui) appears as a row in the `Data Output` tab.

### 1.8. Send another request and check the database

1. In [`Swagger UI`](../../../wiki/swagger.md#what-is-swagger-ui), send another `POST /learners/` request with different values.
2. In [`pgAdmin`](../../../wiki/pgadmin.md#what-is-pgadmin), run the query again.
3. Verify the new row appears.
4. Try changing only the `"name"` or only the `"email"`. What happens then?

### 1.9. Write comments for the issue

> [!NOTE]
> Select the last successful `POST /learners/` request.

<!-- no toc -->
- [Comment 1: write the request as `fetch` code](#191-comment-1-write-the-request-as-fetch-code)
- [Comment 2: write the response](#192-comment-2-write-the-response)
- [Comment 3: attach the file with the data output from `pgAdmin`](#193-comment-3-attach-the-file-with-the-data-output-from-pgadmin)
- [Comment 4: paste the ERD from `pgAdmin`](#194-comment-4-paste-the-erd-from-pgadmin)

#### 1.9.1. Comment 1: write the request as `fetch` code

1. [Copy the selected request as `fetch` code](../../../wiki/browser-developer-tools.md#copy-the-request-as-fetch-code).
2. Paste this [`JavaScript`](../../../wiki/programming-language.md#javascript) code in a [`Markdown` code block](../../../wiki/file-formats.md#markdown-code-block).

   Format of the block (see in [`Markdown` preview](../../../wiki/vs-code.md#open-the-markdown-preview) if you read in `VS Code`):

   ~~~
   ```js
   <fetch-code>
   ```
   ~~~

   Example:

   ~~~
   ```js
   fetch("http://10.93.24.1:42002/learners/", {
      "headers": {
         "accept": "application/json",
   ...
   ```
   ~~~

#### 1.9.2. Comment 2: write the response

1. [Copy the response](../../../wiki/browser-developer-tools.md#copy-the-response) to the selected request.
2. Paste the response as [`JSON`](../../../wiki/file-formats.md#json) in a [`Markdown` code block](../../../wiki/file-formats.md#markdown-code-block).

   Format of the block (see in [`Markdown` preview](../../../wiki/vs-code.md#open-the-markdown-preview) if you read in `VS Code`):

   ~~~
   ```json
   <response>
   ```
   ~~~

   Example:

   ~~~
   ```json
   {"id":6,"name":"John Doe","email":"john-doe@email.com","enrolled_at":"2026-03-02 17:46:34.261004"}
   ```
   ~~~

#### 1.9.3. Comment 3: attach the file with the data output from `pgAdmin`

1. [Save to a file the data output](../../../wiki/pgadmin.md#save-to-file-the-query-data-output) that you got when verifying in the [`pgAdmin`](../../../wiki/pgadmin.md#what-is-pgadmin) that a new row appeared.

   Example of the content in that file:

   ```csv
   "id","name","email","enrolled_at"
   6,"John Doe","john-doe@email.com","2026-03-02 17:46:34.261004"
   5,"Eve Adams","eve@example.com","2025-10-15 11:00:00"
   ...
   ```

2. Attach the file in the comment.

#### 1.9.4. Comment 4: paste the ERD from `pgAdmin`

1. [View the ERD in Chen notation](../../../wiki/pgadmin.md#view-the-erd-in-chen-notation).
2. Make a screenshot where all three tables are fully visible.
3. Paste the screenshot.

### 1.10. Close the issue

Close the issue.

---

## 2. Acceptance criteria

- [ ] Issue has the correct title.
- [ ] Comment 1 includes the request as `fetch` code.
- [ ] Comment 2 includes the response as `JSON` code.
- [ ] Comment 3 includes a `CSV` table with tabs as separators.
- [ ] Comment 4 includes a screenshot of the ERD.
- [ ] Issue is closed.
