# File system

<h2>Table of contents</h2>

- [What is a file system](#what-is-a-file-system)
- [File](#file)
  - [File name](#file-name)
  - [Extension](#extension)
  - [Location](#location)
- [Directory](#directory)
- [Path](#path)
  - [Absolute path](#absolute-path)
  - [Relative path](#relative-path)
- [Special paths](#special-paths)
  - [Root directory (`/`)](#root-directory-)
  - [Home directory (`~`)](#home-directory-)
  - [Current directory (`.`)](#current-directory-)
  - [Parent directory (`..`)](#parent-directory-)
  - [`Desktop` directory](#desktop-directory)
  - [`<directory-path>`](#directory-path)
  - [`<file-path>`](#file-path)

## What is a file system

A file system is the method an [operating system](./operating-system.md) uses to organize and store data on a storage device.

It defines how [files](#file) are named, stored, and retrieved.

Docs:

- [File system (Wikipedia)](https://en.wikipedia.org/wiki/File_system)

## File

A file is a named collection of data stored on the [file system](#what-is-a-file-system).
Files contain data such as text, code, images, or other content.

### File name

The file name identifies the file within its [directory](#directory).

Example: for the file [`wiki/file-system.md`](./file-system.md), the file name is `file-system.md`.

### Extension

The extension is the suffix after the last `.` in the file name.
It indicates the file type or [format](./file-formats.md).

Example: `README.md` has the extension `.md`.

### Location

The location of a file is its containing [directory](#directory).

Example: for the file `/home/user/project/README.md`, the location is `/home/user/project/`.

## Directory

A directory (a.k.a. "folder" on `Windows`) is a special type of [file](#file) that contains other files and directories.

Directories nest inside one another, forming a tree structure rooted at the [root directory](#root-directory-).

## Path

A path points to a [location](#location) in the [filesystem](#what-is-a-file-system).

### Absolute path

Starts from the [root directory](#root-directory-) or the [home directory](#home-directory-).

Examples:

1. `/home/inno-se-toolkit/Desktop/` (`Linux` / `macOS`)
2. `C:/Users/inno-se-toolkit/Desktop/` (`Windows`)

### Relative path

Starts from the current directory.

Examples:

- `backend/app/`
- `./docs/`

## Special paths

### Root directory (`/`)

The root directory is the top-level [directory](#directory) of the file system.
All other files and directories are contained within it.

Its [absolute path](#absolute-path) is `/`.

### Home directory (`~`)

Shortcut for the [absolute path](#absolute-path) for the [user](./operating-system.md#user) home [directory](#directory).

### Current directory (`.`)

The [relative path](#relative-path) for the [directory](#directory) you are currently in.

Examples:

- For the directory [`wiki/`](../wiki), the current directory path is [`wiki/.`](../wiki/.).

### Parent directory (`..`)

The [relative path](#relative-path) for the parent directory of the [directory](#directory).
The parent is always a directory.

Examples:

- For the directory [`wiki/images/`](../wiki/images), the parent directory path is [`wiki/images/..`](../wiki/images/..) which is [`wiki/`](../wiki).

### `Desktop` directory

The `Desktop` directory is the folder that corresponds to the desktop on your screen.

`Windows`: `C:/Users/<username>/Desktop/`
`Linux`: `~/Desktop/` (see [home directory (`~`)](#home-directory-))
`macOS`: `~/Desktop/`
`WSL`: `~/Desktop/`

### `<directory-path>`

The [path](#path) of a [directory](#directory) (without `<` and `>`).

### `<file-path>`

The [path](#path) of a [file](#file) (without `<` and `>`).
