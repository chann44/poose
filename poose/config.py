from dataclasses import dataclass, field
import os
from pathlib import Path

from dotenv import load_dotenv

@dataclass
class Conf:
    path: Path
    dir: str
    table: str = "poose_migrations"

    @classmethod
    def get_env(cls) -> 'Conf': 
        raw = os.getenv("DATABASE_URL") or os.getenv("SQLITE_PATH")
        if not raw:
            raise RuntimeError("Set database url")
        if raw.startswith("sqlite:///"):
            raw = raw[len("sqlite:///"):]
        elif raw.startswith("sqlite://"):
            raw = raw[len("sqlite://"):]
        
        path = Path(raw).expanduser().resolve()
        dir = Path(
            os.getenv("MIGRATION_DIR", "./migrations")
        ).expanduser().resolve()
        table = os.getenv("MIGRATION_TABLE", "poose_migrations")
        return cls(path=path, dir=dir, table=table)




    
     
    