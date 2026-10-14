<div align="center">

<img src="assets/logo.png" width="200" alt="Poose">

# Poose

**A tiny SQLite migration tool, in the spirit of [goose](https://github.com/pressly/goose)**

[![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![TUI](https://img.shields.io/badge/TUI-Textual-9575ff)](https://github.com/Textualize/textual)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![License](https://img.shields.io/badge/license-MIT-21bb4a.svg)](#license)

*Write migrations as plain `.sql`. Apply them with one command. Done.*

</div>

## Features

- **Plain `.sql` migrations** — no Python required to write them
- **One-command everything** — `create`, `up`, `down`, `redo`, `reset`, `status`, `version`, `tui`
- **Atomic by default** — each migration runs in its own transaction
- **Built-in TUI** — browse applied/pending migrations and the live database schema

## Install

```bash
uv sync
```

> [!TIP]
> Requires **Python 3.12+**. Poose reads a `.env` file from your project root automatically.

## Configure

| Variable          | Required    | Default            | Purpose                               |
| ----------------- | ----------- | ------------------ | ------------------------------------- |
| `DATABASE_URL`    | one of these | —                 | e.g. `sqlite:///./app.db`             |
| `SQLITE_PATH`     | ↳           | —                  | Plain path to the SQLite file         |
| `MIGRATION_DIR`   | no          | `./migrations`     | Where `.sql` migration files live     |
| `MIGRATION_TABLE` | no          | `poose_migrations` | Table used to track applied migrations |

Example `.env`:

```env
SQLITE_PATH=./app.db
MIGRATION_DIR=./migrations
```

## Usage

Run commands via `python -m poose.cli <command>` (or `uv run python -m poose.cli <command>`).

```bash
# scaffold a new migration file in MIGRATION_DIR
poose create add_users_table

# apply all pending migrations
poose up

# apply pending migrations up to (and including) a given version
poose up --to 20260101000002

# revert the last N applied migrations (default: 1)
poose down -n 2

# revert the most recent migration and reapply it
poose redo

# revert every applied migration
poose reset

# show every migration and whether it's applied or pending
poose status

# print the current (highest applied) version
poose version

# open the terminal UI
poose tui
```

> [!NOTE]
> Shown above as `poose <command>` for readability — use `python -m poose.cli <command>` until the PyPI package ships with a `poose` entry point.

### Writing a migration

`create` scaffolds a file named `<timestamp>_<name>.sql` in `MIGRATION_DIR`.
Each file must contain an **Up** section and a **Down** section:

```sql
-- +migrate Up
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- +migrate Down
DROP TABLE users;
```

To run multiple statements in a section, either separate them with `;` or,
if a statement itself contains semicolons, split them explicitly with
`-- +statement`:

```sql
-- +migrate Up
CREATE TABLE users (id INTEGER PRIMARY KEY);
-- +statement
CREATE INDEX idx_users_id ON users(id);
```

## TUI

```bash
python -m poose.cli tui
```

Opens a two-pane terminal UI:

- **Left (Migrations)** — every migration found in `MIGRATION_DIR`, marked
  `✓` if applied or `·` if pending.
- **Main (Database schema)** — every table currently in the database, with
  its columns and types.

Keybindings: `r` to refresh, `q` to quit.

## License

[MIT](#license) © 2026 [Chann](https://github.com/chann44)
