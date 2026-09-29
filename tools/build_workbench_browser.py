#!/usr/bin/env python3
"""Build a single-file offline prompt browser from the reviewed catalog."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def build() -> str:
    template = (ROOT / 'ai-workbench' / 'browser-template.html').read_text(encoding='utf-8')
    data = json.loads((ROOT / 'ai-workbench' / 'catalog.json').read_text(encoding='utf-8'))
    # Prevent closing a script element if future catalog text contains HTML.
    serialized = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    return template.replace('__WORKBENCH_DATA__', serialized)


if __name__ == '__main__':
    destination = ROOT / 'ai-workbench' / 'index.html'
    destination.write_text(build(), encoding='utf-8')
    print('Built ai-workbench/index.html (offline, no telemetry).')
