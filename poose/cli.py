from __future__ import annotations

import argparse
import sys

from .config import Conf
from .runner import Runner


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="migrate",
        description="SQLite migrations, goose-style",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("create").add_argument("name")

    up = sub.add_parser("up")
    up.add_argument("--to", default=None)

    down = sub.add_parser("down")
    down.add_argument("-n", "--steps", type=int, default=1)

    sub.add_parser("reset")
    sub.add_parser("redo")
    sub.add_parser("status")
    sub.add_parser("version")
    sub.add_parser("tui")
    return p


def _status(r: Runner) -> None:
    rows = r.status()
    if not rows:
        print("No migrations found.")
        return
    print(f"{'STATE':<8} {'VERSION':<16} {'NAME':<30} APPLIED AT")
    print("-" * 80)
    for s in rows:
        state = "applied" if s.applied else "pending"
        print(
            f"{state:<8} {s.migration.version:<16} "
            f"{s.migration.name:<30} {s.applied_at or '-'}"
        )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.cmd == "tui":
        from tui.app import PooseTUI

        PooseTUI(Conf.get_env()).run()
        return 0

    runner = Runner(Conf.get_env())

    match args.cmd:
        case "create":
            print(f"Created {runner.create(args.name)}")
        case "up":
            done = runner.up(to=args.to)
            print(
                f"Applied {len(done)} migration(s)."
                if done else "Already up to date."
            )
        case "down":
            done = runner.down(steps=args.steps)
            print(
                f"Reverted {len(done)} migration(s)."
                if done else "Nothing to revert."
            )
        case "reset":
            runner.reset()
            print("Database reset.")
        case "redo":
            runner.redo()
            print("Redid last migration.")
        case "status":
            _status(runner)
        case "version":
            print(runner.current_version() or "no migrations applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())