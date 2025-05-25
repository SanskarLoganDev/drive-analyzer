# drive_analyzer/src/drive_analyzer/cli.py
import click
from scanner import scan_folder, save_report
from analyzer import load_report, top_subfolders, display_table
from web_app import create_app

@click.group()
def cli():
    """Drive Analyzer: scan and analyze directory sizes."""
    pass

@cli.command()
@click.option('--path', required=True, type=click.Path(exists=True), help='Folder to scan')
@click.option('--output', default='report.json', help='Output report file')
def scan(path, output):
    """Scan folder sizes and save report."""
    report = scan_folder(path)
    save_report(report, output)
    click.echo(f"Report saved to {output}")

@cli.command()
@click.option('--report', required=True, type=click.Path(exists=True), help='Scan report file')
@click.option('--path', required=True, help='Folder to analyze')
@click.option('--top', default=5, help='Number of top subfolders to show')
def analyze(report, path, top):
    """Analyze a scan report."""
    data = load_report(report)
    items = top_subfolders(data, path, top)
    display_table(items)

@cli.command()
@click.option('--report', required=True, type=click.Path(exists=True), help='Scan report file')
@click.option('--host', default='127.0.0.1', help='Host for web server')
@click.option('--port', default=5000, help='Port for web server')
def serve(report, host, port):
    """Serve a web UI to view report."""
    app = create_app(report)
    app.run(host=host, port=port)
    
    
if __name__ == "__main__":
    cli()
