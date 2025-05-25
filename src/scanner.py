# drive_analyzer/src/scanner.py
import os
import json


def scan_folder(path):
    """
    Walks the directory tree starting at `path` and returns a list of dicts
    with 'path' and total 'size_bytes' for each folder.
    """
    report = []
    for root, dirs, files in os.walk(path):
        total = 0
        for f in files:
            fp = os.path.join(root, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                # skip files we can't access
                pass
        report.append({'path': root, 'size_bytes': total})
    return report


def save_report(report, output_path):
    """
    Saves the report as a JSON file to `output_path`.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)