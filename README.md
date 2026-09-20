# Poose 

A tiny, dependency-free database migration tool in the spirit of
[goose](https://github.com/pressly/goose). Write migrations as plain `.sql`
files, apply them with a single command, and track state in a
`schema_migrations` table.

Works with **any** database that has a Python DB-API 2.0 driver —
PostgreSQL, MySQL, MariaDB, SQLite, SQL Server, and more. No ORM, no
magic — just a cursor and a DSN.

## Features

- Plain `.sql` migration files — no Python required to write them
- `up`, `down`, `redo`, `reset`, `status`, `version`, `create` commands
- Per-migration transactions (atomic)
- Pluggable drivers — add a new database in ~15 lines
- Portable state table (`schema_migrations`) that runs everywhere
- Zero runtime deps except `python-dotenv` (and a driver of your choice)

