from __future__ import annotations

import re
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass

from .config import Conf
from .parser import Migration, load_all, split_statements
from . import templates


@dataclass
class Status:
    migration: Migration
    applied: bool
    applied_at: str | None


class Runner:
    def __init__(self, cfg: Conf):
        self.cfg = cfg
        self._ensure_version_table()


    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.cfg.path)
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
        finally:
            conn.close()

    def _ensure_version_table(self) -> None:
        with self._connect() as conn:
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.cfg.table} (
                    version    TEXT PRIMARY KEY,
                    name       TEXT NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    # ---- state ------------------------------------------------------------

    def applied(self) -> dict[str, str]:
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT version, applied_at FROM {self.cfg.table}"
            ).fetchall()
        return {str(r[0]): str(r[1]) for r in rows}

    def current_version(self) -> str | None:
        applied = self.applied()
        return max(applied) if applied else None


    def all_migrations(self) -> list[Migration]:
        return load_all(self.cfg.dir)

    def pending(self) -> list[Migration]:
        applied = self.applied()
        return [m for m in self.all_migrations() if m.version not in applied]

    def status(self) -> list[Status]:
        applied = self.applied()
        return [
            Status(m, m.version in applied, applied.get(m.version))
            for m in self.all_migrations()
        ]


    def _run_block(self, statements: list[str]) -> None:
        """Execute a list of statements in a single transaction."""
        with self._connect() as conn:
            try:
                for stmt in statements:
                    conn.execute(stmt)
                conn.commit()
            except Exception:
                conn.rollback()
                raise

    def up(self, to: str | None = None) -> list[Migration]:
        todo = self.pending()
        if to:
            todo = [m for m in todo if m.version <= to]

        done: list[Migration] = []
        for m in todo:
            print(f"  ↑ {m}")
            stmts = split_statements(m.up_sql)
            # Run statements + version insert in ONE transaction.
            with self._connect() as conn:
                try:
                    for stmt in stmts:
                        conn.execute(stmt)
                    conn.execute(
                        f"INSERT INTO {self.cfg.table} (version, name) "
                        f"VALUES (?, ?)",
                        (m.version, m.name),
                    )
                    conn.commit()
                except Exception:
                    conn.rollback()
                    raise
            done.append(m)
        return done

    def down(self, steps: int = 1) -> list[Migration]:
        applied = self.applied()
        if not applied:
            return []

        by_version = {m.version: m for m in self.all_migrations()}
        versions = sorted(applied, reverse=True)[:steps]

        reverted: list[Migration] = []
        for v in versions:
            m = by_version.get(v)
            if not m:
                print(f"  ! no file for version {v}, skipping")
                continue
            print(f"  ↓ {m}")
            stmts = split_statements(m.down_sql)
            with self._connect() as conn:
                try:
                    for stmt in stmts:
                        conn.execute(stmt)
                    conn.execute(
                        f"DELETE FROM {self.cfg.table} WHERE version = ?",
                        (v,),
                    )
                    conn.commit()
                except Exception:
                    conn.rollback()
                    raise
            reverted.append(m)
        return reverted

    def reset(self) -> None:
        applied = self.applied()
        if applied:
            self.down(steps=len(applied))

    def redo(self) -> None:
        if self.down(steps=1):
            self.up()

    def create(self, name: str) -> str:
        if not re.match(r"^[A-Za-z0-9_]+$", name):
            raise ValueError("name must be alphanumeric/underscore")
        self.cfg.dir.mkdir(parents=True, exist_ok=True)
        filename = f"{templates.version_now()}_{name}.sql"
        path = self.cfg.dir / filename
        path.write_text(templates.render(), encoding="utf-8")
        return str(path)