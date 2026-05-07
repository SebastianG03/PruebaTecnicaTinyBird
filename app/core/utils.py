import json
from pathlib import Path
from typing import Dict, List


def load_events() -> List[Dict]:
    events_file = Path("./data/events.json")
    events = json.loads(events_file.read_text().encode("utf-8"))

    return list(events)