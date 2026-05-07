import json
from pathlib import Path
from typing import Dict, List
from app.config.configuration import settings


def load_events(path: Path) -> List[Dict]:
    events = json.loads(path.read_text())
    return list(events)
