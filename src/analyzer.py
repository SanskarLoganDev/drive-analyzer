# drive_analyzer/src/analyzer.py
import os
import json
from humanfriendly import format_size
from collections import defaultdict
from rich.table import Table
from rich.console import Console

def load_report(report_path):
    """
    Loads a JSON report from `report_path`.
    """
    with open(report_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def top_subfolders(report, path, n=5):
    """
    Returns the top `n` subfolders under `path` by cumulative size.
    """
    counts = defaultdict(int)
    base = os.path.normpath(path)
    for entry in report:
        p = os.path.normpath(entry['path'])
        if p.startswith(base + os.sep):
            rel = os.path.relpath(p, base)
            first = rel.split(os.sep)[0]
            counts[first] += entry['size_bytes']
    items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return items[:n]


def display_table(items):
    """
    Displays the list of (subfolder, size) tuples in a rich table.
    """
    console = Console()
    table = Table(title="Top Subfolders")
    table.add_column("Rank", justify="center")
    table.add_column("Subfolder")
    table.add_column("Size", justify="right")
    for i, (sub, size) in enumerate(items, start=1):
        table.add_row(str(i), sub, format_size(size))
    console.print(table)
