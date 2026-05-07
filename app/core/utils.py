import json
from pathlib import Path
from typing import Dict, List
from app.config.configuration import settings

def load_events() -> List[Dict]:
    events_file = Path(settings.events_file)
    events = json.loads(events_file.read_text())

    return list(events)