import re
from dataclasses import dataclass
FILE_RE = re.compile(r"^(\d+)_(.+)\.sql$")
UP_RE   = re.compile(r"--\s*\+migrate\s+Up", re.IGNORECASE)
DOWN_RE = re.compile(r"--\s*\+migrate\s+Down", re.IGNORECASE)

@dataclass
class Migration:
    pass

def parse_file():
    pass


def statments():
    pass


def all():
    pass


