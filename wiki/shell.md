# Shell

<h2>Table of contents</h2>

- [What is a shell](#what-is-a-shell)
  - [Login shell](#login-shell)
- [Shell variants](#shell-variants)
  - [`bash`](#bash)
  - [`Git Bash` (`Windows`)](#git-bash-windows)
  - [`zsh`](#zsh)
- [Shell prompt](#shell-prompt)
- [Shell command](#shell-command)
- [Current working directory](#current-working-directory)
  - [Show the current working directory (full path)](#show-the-current-working-directory-full-path)
  - [Check the current directory is `<directory-name>`](#check-the-current-directory-is-directory-name)
  - [Navigate directories](#navigate-directories)
- [Useful commands](#useful-commands)
  - [Check what shell is running](#check-what-shell-is-running)

## What is a shell

An [operating system](./operating-system.md) shell is a computer program that provides relatively broad and direct access to the system on which it runs.
[[source](https://en.wikipedia.org/wiki/Shell_(computing))]

### Login shell

A login shell is started when a user logs in to the system, for example via [`SSH`](./ssh.md#what-is-ssh).
It reads login-specific configuration files such as `~/.bash_profile` or `~/.profile`.

> [!NOTE]
> A `VS Code` terminal is typically a non-login shell and reads `~/.bashrc` instead.

## Shell variants

### `bash`

`Bash` (short for "Bourne Again SHell") is an interactive command interpreter and scripting language developed for `Unix`-like operating systems (e.g., [`Linux`](./linux.md#what-is-linux)).
[[source]]

> [!NOTE]
> `Bash` is the default login shell for `Ubuntu`.

`bash` is the most common shell in learning materials and server docs.

> [!NOTE]
> On `Windows`, you must to [open a directory in `WSL`](./vs-code.md#windows-only-open-the-directory-in-wsl) to run `bash`.

See also: [`Bash`](./bash.md).

### `Git Bash` (`Windows`)

`Git Bash` is a terminal shipped with `Git for Windows`.
It provides a Unix-like shell environment on Windows.

### `zsh`

`zsh` is the default shell on modern `macOS` and is also common on Linux.
Most `bash` commands in this course work in `zsh` as well.

## Shell prompt

The shell prompt is the text the shell displays before each command, indicating it is ready to accept input.
It typically shows the current [user](./operating-system.md#user), machine name, and [working directory](#current-working-directory).

A typical `bash` prompt looks like:

```terminal
username@hostname:~/directory$
```

> [!NOTE]
> The `$` at the end indicates a regular user.
> A `#` indicates the [root](./linux.md#the-root-user) (admin) user.

## Shell command

A shell command is text you type at the [shell prompt](#shell-prompt) and execute by pressing `Enter`.
It consists of a command name, optionally followed by arguments and flags.

```terminal
<command> [flags] [arguments]
```

Example:

```terminal
ls -a .
```

Here `ls` is the command, `-a` is a flag (include hidden files), and `.` is the argument (the [current directory](#current-working-directory)).

## Current working directory

The current working directory is the directory where commands run by default.

### Show the current working directory (full path)

1. To show the current working directory,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   pwd
   ```

### Check the current directory is `<directory-name>`

1. [Show the current working directory](#show-the-current-working-directory-full-path).
2. It should end in `<directory-name>`.

### Navigate directories

1. To navigate to a directory,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   cd /
   cd ~
   cd ..
   ```

To list files in the current working directory,

[run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

```terminal
ls
```

When a command fails with "No such file or directory", verify your current directory first using `pwd`.

## Useful commands

These commands run programs:

- `pwd` - show current directory.
- `ls` - list files.
- `cd <dir>` - go to a directory.
- `cat <file-path>` - print the content of a file at the [`<file-path>`](./file-system.md#file-path).

### Check what shell is running

1. To check what shell is running,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   echo "$SHELL"
   ```
