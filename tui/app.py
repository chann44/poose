from __future__ import annotations

import sqlite3

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Header, Label, ListItem, ListView, Static

from poose.config import Conf
from poose.runner import Runner


def _table_schemas(cfg: Conf) -> list[tuple[str, str, list[tuple[str, str]]]]:
    """Return (table_name, create_sql, [(column_name, column_type), ...]) for every table."""
    conn = sqlite3.connect(cfg.path)
    try:
        rows = conn.execute(
            "SELECT name, sql FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' "
            "ORDER BY name"
        ).fetchall()
        tables = []
        for name, sql in rows:
            cols = conn.execute(f"PRAGMA table_info('{name}')").fetchall()
            columns = [(c[1], c[2]) for c in cols]
            tables.append((name, sql or "", columns))
        return tables
    finally:
        conn.close()


class PooseTUI(App):
    CSS = """
    Horizontal {
        height: 1fr;
    }

    #sidebar {
        width: 44;
        background: $surface;
        border-right: solid $background;
    }

    #sidebar-title {
        padding: 1 1 0 1;
        text-style: bold;
    }

    #main-panel {
        padding: 1 2;
        background: $panel;
    }

    #main-title {
        text-style: bold;
        padding-bottom: 1;
    }
    """

    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, cfg: Conf | None = None):
        super().__init__()
        self.cfg = cfg or Conf.get_env()
        self.runner = Runner(self.cfg)

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("Migrations", id="sidebar-title")
                yield ListView(id="migration-list")
            with VerticalScroll(id="main-panel"):
                yield Label("Database schema", id="main-title")
                yield Static(id="schema-view")
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_data()

    def action_refresh(self) -> None:
        self.refresh_data()

    def refresh_data(self) -> None:
        self._load_migrations()
        self._load_schema()

    def _load_migrations(self) -> None:
        list_view = self.query_one("#migration-list", ListView)
        list_view.clear()
        statuses = self.runner.status()
        if not statuses:
            list_view.append(ListItem(Label("No migrations found.")))
            return
        for s in statuses:
            mark = "[green]✓[/]" if s.applied else "[yellow]·[/]"
            list_view.append(ListItem(Label(f"{mark} {s.migration}")))

    def _load_schema(self) -> None:
        schema_view = self.query_one("#schema-view", Static)
        tables = _table_schemas(self.cfg)
        if not tables:
            schema_view.update("No tables in database.")
            return

        blocks = []
        for name, _, columns in tables:
            header = f"[b $accent]{name}[/]"
            if columns:
                body = "\n".join(
                    f"  {cname:<24} {ctype or 'ANY'}" for cname, ctype in columns
                )
            else:
                body = "  (no columns)"
            blocks.append(f"{header}\n{body}")

        schema_view.update("\n\n".join(blocks))


def run() -> None:
    PooseTUI().run()


if __name__ == "__main__":
    run()
