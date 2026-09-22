
import re
from dataclasses import dataclass
from pathlib import Path


FILE_RE = re.compile(r"^(\d+)_(.+)\.sql$")
UP_RE   = re.compile(r"--\s*\+migrate\s+Up", re.IGNORECASE)
DOWN_RE = re.compile(r"--\s*\+migrate\s+Down", re.IGNORECASE)


@dataclass
class Migration:
    version: str
    name: str
    path: Path
    up_sql: str
    down_sql: str

    def __str__(self) -> str:
        return f"{self.version}_{self.name}"


def parse_file(path: Path) -> Migration:
    m = FILE_RE.match(path.name)
    if not m:
        raise ValueError(
            f"Bad migration filename {path.name!r}: "
            f"expected <version>_<name>.sql"
        )
    version, name = m.group(1), m.group(2)
    content = path.read_text(encoding="utf-8")

    up = UP_RE.search(content)
    down = DOWN_RE.search(content)
    if not up or not down:
        raise ValueError(
            f"{path.name}: file must contain "
            f"'-- +migrate Up' and '-- +migrate Down'"
        )
    if down.start() < up.start():
        raise ValueError(f"{path.name}: Down must come after Up")

    up_sql = content[up.end():down.start()].strip()
    down_sql = content[down.end():].strip()
    return Migration(
        version=version,
        name=name,
        path=path,
        up_sql=up_sql,
        down_sql=down_sql,
    )


def split_statements(sql: str) -> list[str]:
   
    if "-- +statement" in sql:
        parts = re.split(r"--\s*\+statement", sql)
        return [p.strip() for p in parts if p.strip()]

    lines = [ln for ln in sql.splitlines()
             if not ln.strip().startswith("--")]
    cleaned = "\n".join(lines)
    return [s.strip() for s in cleaned.split(";") if s.strip()]


def load_all(directory: Path) -> list[Migration]:
    if not directory.exists():
        return []
    migrations = [parse_file(p) for p in sorted(directory.glob("*.sql"))]
    seen: set[str] = set()
    for m in migrations:
        if m.version in seen:
            raise RuntimeError(f"Duplicate version {m.version}")
        seen.add(m.version)
    return migrations
