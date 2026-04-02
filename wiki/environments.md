# Environments

<h2>Table of contents</h2>

- [What is an environment](#what-is-an-environment)
- [Deployment environment](#deployment-environment)
  - [Development environment](#development-environment)
  - [Integration environment](#integration-environment)
  - [Staging environment](#staging-environment)
  - [Production environment](#production-environment)
- [Environment variable](#environment-variable)
  - [Create the environment variable `<variable>` with the value `<value>` in the current shell session](#create-the-environment-variable-variable-with-the-value-value-in-the-current-shell-session)
  - [Inspect environment variables](#inspect-environment-variables)
- [Common environment variables](#common-environment-variables)
  - [`PATH` environment variable](#path-environment-variable)
  - [Inspect `PATH`](#inspect-path)
- [`.env` file](#env-file)
  - [Set the `<variable>` to `<value>` in the `.env` file at `<file-path>`](#set-the-variable-to-value-in-the-env-file-at-file-path)
- [Secrets](#secrets)
  - [Unencrypted secrets](#unencrypted-secrets)
  - [Unencrypted secrets in the repo](#unencrypted-secrets-in-the-repo)
  - [Store encrypted secrets in the repo](#store-encrypted-secrets-in-the-repo)
  - [Add files containing secrets to `.gitignore`](#add-files-containing-secrets-to-gitignore)
- [Feature flag](#feature-flag)

## What is an environment

An environment ([deployment environment](#deployment-environment)) is a specific configuration of hardware, software, and [environment variables](#environment-variable) in which an application runs.

Different environments serve different purposes in the software development lifecycle: writing code, testing, and serving end users.

## Deployment environment

A program can run in multiple [deployment environments](https://github.com/inno-se/the-guide?tab=readme-ov-file#environments).

Each development environment may need a specific set of [environment variables](#environment-variable). This set can be different for each environment.

### Development environment

The development environment is where developers write, run, and test code locally.

It typically uses development-friendly settings: detailed error messages, local databases, and debug tools.

Docs:

- [Development environment](https://github.com/inno-se/the-guide?tab=readme-ov-file#development-environment)

### Integration environment

The integration environment is where code from multiple developers is merged and tested together.

It verifies that separate components work correctly when combined.

Docs:

- [Integration environment](https://github.com/inno-se/the-guide?tab=readme-ov-file#integration-environment)

### Staging environment

The staging environment closely mirrors production.

It is used to perform final verification before deploying changes to the [production environment](#production-environment).

Docs:

- [Staging environment](https://github.com/inno-se/the-guide?tab=readme-ov-file#staging-environment)

### Production environment

The production environment is the live environment where end users access the application.

It uses production settings: minimal error output, real data, and performance-optimised configuration.

Docs

- [Production environment](https://github.com/inno-se/the-guide?tab=readme-ov-file#production-environment)

## Environment variable

Environment variables are named values that are available to a program running in a particular [deployment environment](#deployment-environment).

### Create the environment variable `<variable>` with the value `<value>` in the current shell session

1. To create an environment variable in the current [shell session](./shell.md#shell-session),

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   <variable>=<value>
   ```

   Replace the placeholders:

   - `<variable>` with the name of the variable.

     Example: `VARIABLE_NAME`.

   - `<value>` with the value of the variable.

     Example: `VARIABLE_VALUE`.

     > 🟦 **Note**
     >
     > The `VARIABLE_VALUE` is a string.

   Example:

   ```terminal
   VARIABLE_NAME=VARIABLE_VALUE
   ```

### Inspect environment variables

1. To list all currently available environment variables,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   env
   ```

2. You should see a list of environment variables in the `<env-variable-name>=<env-variable-value>` format.

## Common environment variables

These [environment variables](#environment-variable) are available in most [operating systems](./operating-system.md#what-is-an-operating-system):

- [`PATH`](#path-environment-variable)

### `PATH` environment variable

`PATH` contains a list of [directories](./file-system.md#directory) separated by `:`.

When you run a command in the [terminal](./vs-code.md#vs-code-terminal), the system looks for the [program](./software-types.md#program) in each directory listed in `PATH`, from left to right.

### Inspect `PATH`

1. [Check the current shell in the `VS Code Terminal`](./vs-code.md#check-the-current-shell-in-the-vs-code-terminal).
2. To view the `PATH` [environment variable](#environment-variable),

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   echo $PATH
   ```

3. You should see a list of directories separated by `:`.

## `.env` file

A `.env` file ("dotenv file") is a file that contains a list of [environment variables](#environment-variable) in the `<env-variable-name>=<env-variable-value>` format.

Examples:

- [`.env.docker.example`](../.env.docker.example)

Docs:

- [(`dotenv`) Security - `.env`](https://www.dotenv.org/docs/security/env.html)
- [(`Docker Compose`) `.env` file syntax](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/#env-file-syntax)

### Set the `<variable>` to `<value>` in the `.env` file at `<file-path>`

1. (LOCAL):

    1. [Open the file at `<file-path>` using `code`](./vs-code.md#open-the-file-or-the-directory-using-code).

   (REMOTE):

    1. To open the file at `<file-path>` using `nano`,

       [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

       ```terminal
       nano <file-path>
       ```

2. Navigate to the line that has `<variable-name>`.

   The text should look similar to this:

   ```terminal
   <variable-name>=SOME_VALUE
   ```

   Example:

   ```terminal
   VARIABLE_NAME=SOME_VALUE
   ```

3. Move the pointer using arrows on the keyboard (`UpArrow`, `DownArrow`, `LeftArrow`, `RightArrow`).

4. Delete `SOME_VALUE` using the keyboard (`Backspace` or `Delete`).

5. Type `<value>`.

   The text should look similar to this:

   ```terminal
   <variable-name>=<value>
   ```

   Example:

   ```terminal
   VARIABLE_NAME=SOME_NEW_VALUE
   ```

6. To write the changes:

   1. Press `Ctrl+O`.
   2. Press `Enter`.

7. To close the editor, press `Ctrl+X`.

## Secrets

Secrets are values that only specific people may know such as passwords, personal tokens, private keys, etc.

Secrets are sometimes stored in [`.env` files](#env-file).

### Unencrypted secrets

Unencrypted secrets are secrets that can be used as-is.

For example, a password can be copied to enter a site.

### Unencrypted secrets in the repo

Don't store unencrypted secrets in the repo.

Don't store in the repo files (e.g., [`.env` files](#env-file)) that contain unencrypted secrets.

If you add files containing secrets to the repo, bad people may steal the secrets from your repo and hack your app.

Therefore, you should use any of these methods:

<!-- no toc -->
- [Store encrypted secrets in the repo](#store-encrypted-secrets-in-the-repo)
- [Add files containing secrets to `.gitignore`](#add-files-containing-secrets-to-gitignore)

### Store encrypted secrets in the repo

If you want to store secrets in the repo, encrypt them first using a [tool](https://github.com/inno-se/the-guide?tab=readme-ov-file#secrets).

Then, you can commit the file containing the secrets.

### Add files containing secrets to `.gitignore`

Match in [`.gitignore`](./git.md#gitignore) all files that can contain [unencrypted secrets](#unencrypted-secrets-in-the-repo) so that these secrets don't get added to the repo.

## Feature flag

A feature flag (also called a feature toggle) is a mechanism that enables or disables a feature at runtime without deploying new code. Feature flags let teams decouple deployment from release, enabling gradual rollouts, `A/B` testing, and quick rollbacks.
