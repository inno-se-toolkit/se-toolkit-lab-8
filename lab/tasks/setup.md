# Lab setup

- [1. Required steps](#1-required-steps)
  - [1.1. (UPD) Find a partner](#11-upd-find-a-partner)
  - [1.2. Start creating a VM](#12-start-creating-a-vm)
  - [1.3. Set up your fork](#13-set-up-your-fork)
    - [1.3.1. Sign in on `GitHub`](#131-sign-in-on-github)
    - [1.3.2. (UPD) Fork the course instructors' repo](#132-upd-fork-the-course-instructors-repo)
    - [1.3.3. (UPD) Go to your fork](#133-upd-go-to-your-fork)
    - [1.3.4. (UPD) Enable issues](#134-upd-enable-issues)
    - [1.3.5. (UPD) Add a classmate as a collaborator](#135-upd-add-a-classmate-as-a-collaborator)
    - [1.3.6. (UPD) Protect your `main` branch](#136-upd-protect-your-main-branch)
  - [1.4. Set up programs](#14-set-up-programs)
    - [1.4.1. (UPD) Set up `VS Code`](#141-upd-set-up-vs-code)
    - [1.4.2. (UPD) Set up `Docker`](#142-upd-set-up-docker)
    - [1.4.3. (UPD) (`Windows` only) Set the default shell for the `VS Code Terminal`](#143-upd-windows-only-set-the-default-shell-for-the-vs-code-terminal)
    - [1.4.4. Set up `Git`](#144-set-up-git)
  - [1.5. (UPD) Open in `VS Code` the `software-engineering-toolkit` directory](#15-upd-open-in-vs-code-the-software-engineering-toolkit-directory)
  - [1.6. Clone your fork](#16-clone-your-fork)
    - [1.6.1. (UPD) Copy your fork URL](#161-upd-copy-your-fork-url)
    - [1.6.2. (UPD) Clone your fork](#162-upd-clone-your-fork)
  - [1.7. (UPD) Open the cloned repo and set up `VS Code`](#17-upd-open-the-cloned-repo-and-set-up-vs-code)
  - [1.8. Continue creating a VM](#18-continue-creating-a-vm)
  - [1.9. Set up `Python`](#19-set-up-python)
    - [1.9.1. Install `uv`](#191-install-uv)
    - [1.9.2. (UPD) Set up `Python` in `VS Code`](#192-upd-set-up-python-in-vs-code)
  - [1.10. (UPD) Prepare `Docker`](#110-upd-prepare-docker)
  - [1.11. Start the services](#111-start-the-services)
    - [1.11.1. (UPD) Set up the `Docker` environment](#1111-upd-set-up-the-docker-environment)
    - [1.11.2. (UPD) Start the services using `Docker Compose`](#1112-upd-start-the-services-using-docker-compose)
  - [1.12. Observe containers and services](#112-observe-containers-and-services)
    - [1.12.1. (UPD) Open a new `VS Code Terminal`](#1121-upd-open-a-new-vs-code-terminal)
    - [1.12.2. (UPD) List running containers](#1122-upd-list-running-containers)
    - [1.12.3. (UPD) See logs of the running services](#1123-upd-see-logs-of-the-running-services)
  - [1.13. (UPD) Set up `Swagger UI`](#113-upd-set-up-swagger-ui)
  - [1.14. Set up `pgAdmin`](#114-set-up-pgadmin)
    - [1.14.1. (UPD) Connect `pgAdmin` to the database](#1141-upd-connect-pgadmin-to-the-database)
    - [1.14.2. (UPD) Inspect the tables](#1142-upd-inspect-the-tables)
  - [1.15. (UPD) Stop the services](#115-upd-stop-the-services)
  - [1.16. Set up the autochecker](#116-set-up-the-autochecker)
    - [1.16.1. (UPD) Log in to the autochecker](#1161-upd-log-in-to-the-autochecker)
    - [1.16.2. (UPD) Prepare your VM for checking](#1162-upd-prepare-your-vm-for-checking)
  - [1.17. (UPD) Set up a coding agent](#117-upd-set-up-a-coding-agent)
- [2. Optional steps](#2-optional-steps)
  - [2.1. (UPD) Set up `Nix`](#21-upd-set-up-nix)
  - [2.2. (UPD) Set up `direnv`](#22-upd-set-up-direnv)
  - [2.3. Learn to go back after clicking a link](#23-learn-to-go-back-after-clicking-a-link)
  - [2.4. Set up the shell prompt](#24-set-up-the-shell-prompt)
  - [2.5. Customize the `Source Control`](#25-customize-the-source-control)
  - [2.6. Get familiar with `GitLens`](#26-get-familiar-with-gitlens)
  - [2.7. Create a label for tasks](#27-create-a-label-for-tasks)
  - [2.8. View `Markdown` files in `VS Code`](#28-view-markdown-files-in-vs-code)

## 1. Required steps

> [!IMPORTANT]
> Some steps have the `(UPD)` label.
>
> These steps must be completed to get the right setup for this lab,
> even if you have completed similar steps in the previous lab.

> [!NOTE]
> We provide all of the hardest steps in the lab setup
> so that TAs can help you get the right setup during the lab.
>
> Tasks are more or less easy when you have the right setup.

### 1.1. (UPD) Find a partner

1. Find a partner for this lab.
2. Sit next to them.

> [!IMPORTANT]
> You work on tasks independently from your partner.
>
> You and your partner work together when reviewing each other's work.

### 1.2. Start creating a VM

> [!NOTE]
> Skip this step if you can [connect to your VM](../../wiki/vm.md#connect-to-the-vm).

[Create a subscription](../../wiki/vm.md#create-a-subscription) to be able to create a VM.

> [!TIP]
> Subscription approval may take time.
> Continue with the next steps while you wait — you will
> [finish creating the VM](#18-continue-creating-a-vm) later.

### 1.3. Set up your fork

#### 1.3.1. Sign in on `GitHub`

1. Sign in on [`GitHub`](https://github.com/).
2. [Find `<your-github-username>`](../../wiki/github.md#find-your-github-username).

#### 1.3.2. (UPD) Fork the course instructors' repo

1. [Fork the course instructors' repo](../../wiki/github.md#fork-a-repo).

   The course instructors' repo [URL](../../wiki/web-development.md#url) is <https://github.com/inno-se-toolkit/se-toolkit-lab-4>.

#### 1.3.3. (UPD) Go to your fork

1. [Go to your fork](../../wiki/github.md#go-to-your-fork).

   The [URL](../../wiki/web-development.md#url) of your fork should look like `https://github.com/<your-github-username>/se-toolkit-lab-4`.

#### 1.3.4. (UPD) Enable issues

1. [Enable issues](../../wiki/github.md#enable-issues).

#### 1.3.5. (UPD) Add a classmate as a collaborator

1. [Add a collaborator](../../wiki/github.md#add-a-collaborator) — your partner.
2. Your partner should add you as a collaborator in their repo.

> [!NOTE]
> It's OK if your collaborator can't change `Settings` in your repo.

#### 1.3.6. (UPD) Protect your `main` branch

> [!NOTE]
> Branch protection prevents accidental pushes directly to `main`.
> This enforces the PR workflow and ensures all changes are reviewed.

1. [Protect the `main` branch](../../wiki/github.md#protect-a-branch).

### 1.4. Set up programs

#### 1.4.1. (UPD) Set up `VS Code`

1. (Optional) [Read about `VS Code`](../../wiki/vs-code.md#what-is-vs-code).
2. [Set up `VS Code`](../../wiki/vs-code.md#set-up-vs-code).

#### 1.4.2. (UPD) Set up `Docker`

1. (Optional) [Read about `Docker`](../../wiki/docker.md#what-is-docker).
2. [Install `Docker`](../../wiki/docker.md#install-docker) if it's not installed.
3. [Start `Docker`](../../wiki/docker.md#start-docker).

#### 1.4.3. (UPD) (`Windows` only) Set the default shell for the `VS Code Terminal`

1. [Check the current shell in the `VS Code Terminal`](../../wiki/vs-code.md#check-the-current-shell-in-the-vs-code-terminal).
2. If it's not `bash` or `zsh`, [set the default shell](../../wiki/vs-code.md#windows-only-set-the-default-shell-for-the-vs-code-terminal).
3. [Check the current shell](../../wiki/vs-code.md#check-the-current-shell-in-the-vs-code-terminal) again.

#### 1.4.4. Set up `Git`

1. (Optional) [Read about `Git`](../../wiki/git.md#what-is-git).
2. [Install `Git`](https://git-scm.com/install/) if it's not installed.
3. (Optional) [Configure `Git`](../../wiki/git.md#configure-git).

### 1.5. (UPD) Open in `VS Code` the `software-engineering-toolkit` directory

1. Inside the [`Desktop` directory](../../wiki/file-system.md#desktop-directory),
   create the directory `software-engineering-toolkit`.

   Skip this step if this directory exists.

2. [Open in `VS Code` the directory](../../wiki/vs-code.md#open-the-directory):
   `software-engineering-toolkit`.
3. (`Windows` only) [Reopen the directory in `WSL`](../../wiki/vs-code.md#windows-only-reopen-the-directory-in-wsl) if you didn't do that before.

### 1.6. Clone your fork

#### 1.6.1. (UPD) Copy your fork URL

1. [Go to your fork](#133-upd-go-to-your-fork).
2. Copy [`<your-fork-url>`](../../wiki/github.md#your-fork-url).

   It should look like `https://github.com/<your-github-username>/se-toolkit-lab-4`.

   See [`<your-github-username>`](../../wiki/github.md#your-github-username).

#### 1.6.2. (UPD) Clone your fork

1. [Clone your fork](../../wiki/git-vscode.md#clone-the-repository):

   - Replace `<repo-url>` with [`<your-fork-url>`](../../wiki/github.md#your-fork-url).
   - Replace `<repo-name>` with `se-toolkit-lab-4`.

### 1.7. (UPD) Open the cloned repo and set up `VS Code`

> [!IMPORTANT]
> Go by the links in the steps below and complete the checks ("You should see ...").
> Otherwise, your setup will be broken.

1. [Open in `VS Code` the directory](../../wiki/vs-code.md#open-the-directory):
   `se-toolkit-lab-4`.
2. [Check the current shell in the `VS Code Terminal`](../../wiki/vs-code.md#check-the-current-shell-in-the-vs-code-terminal).
3. [Install the recommended `VS Code` extensions](../../wiki/vs-code.md#install-the-recommended-vs-code-extensions).

<details><summary>Troubleshooting</summary>

<h4>The terminal shell is not <code>bash</code> or <code>zsh</code></h4>

Go back to [step 1.4.3](#143-upd-windows-only-set-the-default-shell-for-the-vs-code-terminal) and set the default shell.

<h4>Recommended extensions did not install</h4>

Reload the `VS Code` window: press `Ctrl+Shift+P`, type `Reload Window`, and press `Enter`.

</details>

### 1.8. Continue creating a VM

> [!NOTE]
> Don't overwrite the key if it already exists.
> You can use the key that you created before for the new VM.

If you can't [connect to your VM](../../wiki/vm.md#connect-to-the-vm), complete these steps:

1. [Set up `SSH`](../../wiki/ssh.md#set-up-ssh).
2. [Create a VM using the subscription](../../wiki/vm.md#create-a-vm-using-the-subscription).

### 1.9. Set up `Python`

> [!NOTE]
> See [What is `Python`](../../wiki/python.md#what-is-python).

#### 1.9.1. Install `uv`

> [!NOTE]
> See [`uv`](../../wiki/python.md#uv).

1. [Install `uv`](../../wiki/python.md#install-uv).

#### 1.9.2. (UPD) Set up `Python` in `VS Code`

> [!NOTE]
> The dependencies have been updated in this project version.

1. [Set up `Python` in `VS Code`](../../wiki/python.md#set-up-python-in-vs-code).

### 1.10. (UPD) Prepare `Docker`

> [!NOTE]
> Old containers and volumes from a previous lab version may conflict with the updated services.
> Stop running containers, remove stopped containers, and delete unused volumes so you start with a clean state.

1. [Start `Docker`](../../wiki/docker.md#start-docker).
2. [Clean up `Docker`](../../wiki/docker.md#clean-up-docker).

### 1.11. Start the services

> [!NOTE]
> See [service](../../wiki/docker-compose.md#service).

#### 1.11.1. (UPD) Set up the `Docker` environment

1. To copy the [`.env.docker.example`](../../.env.docker.example) file to the [`.env.docker.secret`](../../wiki/dotenv-docker-secret.md#what-is-envdockersecret) file,

   [run in the `VS Code Terminal`](../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   cp .env.docker.example .env.docker.secret
   ```

#### 1.11.2. (UPD) Start the services using `Docker Compose`

> [!NOTE]
> [`Docker Compose`](../../wiki/docker-compose.md#what-is-docker-compose) reads environment variables from [`.env.docker.secret`](../../wiki/dotenv-docker-secret.md#what-is-envdockersecret)
> and uses them to configure the containers defined in [`docker-compose.yml`](../../docker-compose.yml).

1. To start the services,

   [run in the `VS Code Terminal`](../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret up --build
   ```

   Wait for the services to start. You should see log output from the `app`, `postgres`, `pgadmin`, and `caddy` containers.

   <details><summary>Troubleshooting</summary>

   <h4>Port conflict (<code>port is already allocated</code>)</h4>

   Stop the process that uses the port, then retry.

   <h4>Containers exit immediately</h4>

   To rebuild all containers from scratch,

   [run in the `VS Code Terminal`](../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret down -v
   docker compose --env-file .env.docker.secret up --build
   ```

   <h4>Image pull fails</h4>

   Check your internet connection. If you are behind a proxy, configure `Docker` to use it.

   </details>

> [!NOTE]
> The database is initialized from [`backend/app/data/init.sql`](../../backend/app/data/init.sql) only on the **first** start of the `PostgreSQL` container.
>
> If you need to re-initialize the database (e.g., after pulling upstream changes to `init.sql`), see [Resetting the database](../../wiki/docker-postgres.md#resetting-the-database).

### 1.12. Observe containers and services

#### 1.12.1. (UPD) Open a new `VS Code Terminal`

1. [Open a new `VS Code Terminal`](../../wiki/vs-code.md#open-a-new-vs-code-terminal).

#### 1.12.2. (UPD) List running containers

1. To list running containers,

   [run in the `VS Code Terminal`](../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret ps
   ```

1. To look at services and their statuses specifically,

   ```terminal
   docker compose --env-file .env.docker.secret ps --format "table {{.Service}}\t{{.Status}}"
   ```

   You should see a similar output:

   ```terminal
   SERVICE    STATUS
   app        Up 3 minutes
   caddy      Up 3 minutes
   pgadmin    Up 3 minutes
   postgres   Up 3 minutes (healthy)
   ```

#### 1.12.3. (UPD) See logs of the running services

1. To see logs for all services,

   [run in the `VS Code Terminal`](../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret logs
   ```

   You should see log output from the `app`, `postgres`, `pgadmin`, and `caddy` services.

2. To see logs for the `postgres` service,

   [run in the `VS Code Terminal`](../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret logs postgres
   ```

   You should see only the `postgres` service logs,
   including a line like `database system is ready to accept connections`.

### 1.13. (UPD) Set up `Swagger UI`

1. [Open `Swagger UI`](../../wiki/swagger.md#open-swagger-ui).

   You should see the [`Swagger UI`](../../wiki/swagger.md#what-is-swagger-ui) page with the [API](../../wiki/api.md#what-is-an-api) documentation.

   <img alt="Swagger UI" src="../images/tasks/setup/swagger-ui.png" style="width:400px"></img>

### 1.14. Set up `pgAdmin`

#### 1.14.1. (UPD) Connect `pgAdmin` to the database

> [!NOTE]
> [`pgAdmin`](../../wiki/pgadmin.md#what-is-pgadmin) takes 2-3 minutes to start after you have started the services.

1. [Open `pgAdmin`](../../wiki/pgadmin.md#open-pgadmin).
2. [Connect `pgAdmin` to the `PostgreSQL` server](../../wiki/pgadmin.md#connect-to-the-postgresql-server).

<details><summary>Troubleshooting</summary>

<h4><code>pgAdmin</code> page does not load</h4>

`pgAdmin` takes 2–3 minutes to start. Wait and refresh the page.

<h4>Connection to the server refused</h4>

Make sure the services are running. Go back to [step 1.11.2](#1112-upd-start-the-services-using-docker-compose) and start them.

</details>

#### 1.14.2. (UPD) Inspect the tables

1. [Browse the data in the `interacts` table](../../wiki/pgadmin.md#browse-data-in-the-table).

   You should see rows of data stored in the database.

   <img alt="Interaction logs" src="../images/tasks/setup/database-interaction-logs.png" style="width:400px"></img>

   These are records of what [`learner`s](../../docs/design/domain-model.md#learner) did with [`item`s](../../docs/design/domain-model.md#item) (courses, labs, tasks, steps).
   `learner`s [`attempt`ed](../../docs/design/domain-model.md#attempt), [`complete`d](../../docs/design/domain-model.md#complete) or just [`view`ed](../../docs/design/domain-model.md#view) `item`s.

2. Verify that the following tables also exist:
   - `item`
   - `learner`

### 1.15. (UPD) Stop the services

1. [Check that the current directory is `se-toolkit-lab-4`](../../wiki/shell.md#check-the-current-directory-is-directory-name).
2. [Stop and remove all containers and volumes](../../wiki/docker-compose.md#stop-and-remove-all-containers-and-volumes).

### 1.16. Set up the autochecker

> [!NOTE]
> The autochecker is a bot that checks your repository and VM.

#### 1.16.1. (UPD) Log in to the autochecker

1. Open in `Telegram`: <https://t.me/auchebot>.
2. Log in.

#### 1.16.2. (UPD) Prepare your VM for checking

1. [Connect to your VM](../../wiki/vm.md#connect-to-the-vm).
2. [Set up your VM for the autochecker](../../wiki/vm-autochecker.md#set-up-the-vm-for-autochecker).

### 1.17. (UPD) Set up a coding agent

A coding agent can help you write code, explain concepts, and debug issues.

<div style="display:flex;flex-wrap:wrap;gap:10px">
  <img alt="Qwen request" src="../images/tasks/setup/qwen-request.png" style="width:300px"></img>
  <img alt="Qwen response" src="../images/tasks/setup/qwen-response.png" style="width:300px"></img>
</div>

- Method 1: [Set up a `Qwen Code`-based agent](../../wiki/coding-agents.md#set-up-qwen-code-based-agent).
- Method 2: [Choose another coding agent](../../wiki/coding-agents.md#choose-a-coding-agent).

---

## 2. Optional steps

These enhancements can make your life easier:

<!-- no toc -->
- [Set up `Nix`](#21-upd-set-up-nix)
- [Set up `direnv`](#22-upd-set-up-direnv)
- [Learn to go back after clicking a link](#23-learn-to-go-back-after-clicking-a-link)
- [Set up the shell prompt](#24-set-up-the-shell-prompt)
- [Customize the `Source Control`](#25-customize-the-source-control)
- [Get familiar with `GitLens`](#26-get-familiar-with-gitlens)
- [Create a label for tasks](#27-create-a-label-for-tasks)
- [View `Markdown` files in `VS Code`](#28-view-markdown-files-in-vs-code)

### 2.1. (UPD) Set up `Nix`

1. (Optional) [Read about `Nix`](../../wiki/nix.md#what-is-nix).
2. [Set up `Nix`](../../wiki/nix.md#set-up-nix).

### 2.2. (UPD) Set up `direnv`

1. (Optional) [Read about `direnv`](../../wiki/direnv.md#what-is-direnv).
2. [Set up `Nix`](#21-upd-set-up-nix).
3. [Set up `direnv`](../../wiki/direnv.md#set-up-direnv).

### 2.3. Learn to go back after clicking a link

<!-- TODO formulate not as a note -->

> [!NOTE]
> Shortcuts for going back after clicking a link:
>
> - `VS Code` — see the [shortcut](../../wiki/vs-code.md#shortcut-go-back).
> - `Firefox` — `Alt+ArrowLeft`.
> - Other browsers — google.

### 2.4. Set up the shell prompt

`Starship` shows your current `Git` branch, status, and other useful info directly in your [shell prompt](../../wiki/shell.md#shell-prompt) in almost any terminal, including the [`VS Code Terminal`](../../wiki/vs-code.md#vs-code-terminal).

Complete these steps:

1. [Install `Starship`](https://github.com/starship/starship#-installation).
2. [Open the `VS Code Terminal`](../../wiki/vs-code.md#open-the-vs-code-terminal).

   You should see something similar to this:

   <img alt="Starship in the VS Code Terminal" src="../../wiki/images/starship/terminal-prompt.png" style="width:400px"></img>

### 2.5. Customize the `Source Control`

1. [Open the `Source Control`](../../wiki/vs-code.md#open-the-source-control).
2. Click three dots to the right of `SOURCE CONTROL`.
3. Put checkmarks only near `Changes` and `GitLens` to see only these views.

   <img alt="Changes and GitLens" src="../../wiki/images/vs-code/source-control-allowed-views.png" style="width:400px"></img>

### 2.6. Get familiar with `GitLens`

[`GitLens`](../../wiki/gitlens.md#what-is-gitlens) helps you work with `Git` in `VS Code`.

Complete these steps:

1. [See all branches](../../wiki/gitlens.md#see-all-branches).
2. [Look at the commit graph](../../wiki/gitlens.md#look-at-the-commit-graph).
3. [Inspect the current branch](../../wiki/gitlens.md#inspect-the-current-branch).
4. [Inspect the remotes](../../wiki/gitlens.md#inspect-the-remotes).

### 2.7. Create a label for tasks

[Labels](../../wiki/github.md#label) help you filter and organize issues.

With a `task` label, you can see in one view all issues created for lab tasks.

> [!TIP]
> If you create the `task` label before creating issues, your issues will have this label automatically as configured in the [issue form](../../.github/ISSUE_TEMPLATE/01-task.yml).

Complete these steps:

1. [Create](../../wiki/github.md#create-a-label) the `task` label.
2. [Add the label to issues](../../wiki/github.md#add-a-label-to-issues).
3. [See all issues with the label](../../wiki/github.md#see-all-issues-with-a-label).

### 2.8. View `Markdown` files in `VS Code`

If you want to view [`README.md`](../../README.md) and other `Markdown` files in `VS Code` instead of on `GitHub`:

1. [Install the recommended `VS Code` extensions](../../wiki/vs-code.md#install-the-recommended-vs-code-extensions).
2. [Open the file](../../wiki/vs-code.md#open-the-file):
   [`README.md`](../../README.md).
3. [Open the `Markdown` preview](../../wiki/vs-code.md#open-the-markdown-preview).
