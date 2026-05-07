import json
from pathlib import Path
from typing import Dict, List


def load_events(path: Path) -> List[Dict]:
    events = json.loads(path.read_text())
    return list(events)
