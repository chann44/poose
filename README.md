# Poose

A tiny SQLite migration tool in the spirit of
[goose](https://github.com/pressly/goose). Write migrations as plain `.sql`
files, apply them with a single command, and track applied state in a
`poose_migrations` table. Comes with a `textual` TUI for browsing migration
status and the live database schema.

## Features

- Plain `.sql` migration files — no Python required to write them
- `create`, `up`, `down`, `redo`, `reset`, `status`, `version`, `tui` commands
- Per-migration transactions (atomic)
- A terminal UI showing applied/pending migrations and every table's schema

## Install

```bash
uv sync
```

## Configure

Poose reads its settings from environment variables (a `.env` file in the
project root is picked up automatically):

| Variable          | Required | Default          | Purpose                                   |
| ------------------ | -------- | ----------------- | ------------------------------------------ |
| `DATABASE_URL`     | one of   | —                  | e.g. `sqlite:///./app.db`                  |
| `SQLITE_PATH`      | these    | —                  | Plain path to the SQLite file              |
| `MIGRATION_DIR`    | no       | `./migrations`     | Where `.sql` migration files live          |
| `MIGRATION_TABLE`  | no       | `poose_migrations` | Table used to track applied migrations     |

Either `DATABASE_URL` or `SQLITE_PATH` must be set.

Example `.env`:

```env
SQLITE_PATH=./app.db
MIGRATION_DIR=./migrations
```

## Usage

Run commands via `python -m poose.cli <command>` (or `uv run python -m poose.cli <command>`).

```bash
# scaffold a new migration file in MIGRATION_DIR
python -m poose.cli create add_users_table

# apply all pending migrations
python -m poose.cli up

# apply pending migrations up to (and including) a given version
python -m poose.cli up --to 20260101000002

# revert the last N applied migrations (default: 1)
python -m poose.cli down -n 2

# revert the most recent migration and reapply it
python -m poose.cli redo

# revert every applied migration
python -m poose.cli reset

# show every migration and whether it's applied or pending
python -m poose.cli status

# print the current (highest applied) version
python -m poose.cli version

# open the terminal UI
python -m poose.cli tui
```

### Writing a migration file

`create` scaffolds a file named `<timestamp>_<name>.sql` in `MIGRATION_DIR`.
Each file must contain an Up section and a Down section:

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

### TUI

`python -m poose.cli tui` opens a two-pane terminal UI:

- **Left (Migrations)** — every migration found in `MIGRATION_DIR`, marked
  `✓` if applied or `·` if pending.
- **Main (Database schema)** — every table currently in the database, with
  its columns and types.

Keybindings: `r` to refresh, `q` to quit.
