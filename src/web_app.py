# drive_analyzer/src/drive_analyzer/web_app.py
from flask import Flask, render_template_string, request
import os
import json
from humanfriendly import format_size

TEMPLATE = '''
<!doctype html>
<title>Drive Analyzer Report</title>
<h1>Drive Analyzer Report</h1>
<form method="get">
  <label>Path to analyze: <input name="path" value="{{ path }}"></label>
  <label>Top N: <input name="top" type="number" value="{{ top }}"></label>
  <button type="submit">Update</button>
</form>
<table border=1 cellpadding=5 cellspacing=0>
  <tr><th>Rank</th><th>Subfolder</th><th>Size</th></tr>
  {% for idx, sub, size in data %}
    <tr>
      <td>{{ idx }}</td>
      <td>{{ sub }}</td>
      <td>{{ size }}</td>
    </tr>
  {% endfor %}
</table>
'''

def create_app(report_path):
    """
    Factory to create the Flask app for viewing the report.
    """
    app = Flask(__name__)
    with open(report_path, 'r', encoding='utf-8') as f:
        report_data = json.load(f)

    @app.route('/')
    def index():
        path = request.args.get('path', default=os.path.dirname(report_path))
        top = int(request.args.get('top', 5))
        # compute cumulative sizes per first-level subfolder
        base = os.path.normpath(path)
        counts = {}
        for entry in report_data:
            p = os.path.normpath(entry['path'])
            if p.startswith(base + os.sep):
                rel = os.path.relpath(p, base)
                first = rel.split(os.sep)[0]
                counts[first] = counts.get(first, 0) + entry['size_bytes']
        sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top]
        data = [(i+1, sub, format_size(size)) for i, (sub, size) in enumerate(sorted_items)]
        return render_template_string(TEMPLATE, data=data, path=path, top=top)

    return app