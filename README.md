# 🖥️ Drive Analyzer

A simple yet powerful Python CLI and web app to scan your drives, report folder sizes, and interactively explore the results.

---

## 🚀 Features

- Recursive scan of any folder or drive  
- Human-readable sizes with graceful formatting  
- Top-N analysis of largest subfolders in the terminal  
- Flask-powered web UI for interactive browsing  
- Zero external dependencies beyond PyPI packages  
- Cross-platform: works on Windows, macOS & Linux  

---

## 📦 Table of Contents

1. Installation 
2. Quickstart 
3. CLI Usage  
   - Scan
   - Analyze  
   - Serve 
4. Project Structure 
5. How It Works 
6. Contributing 


---

## 🔧 Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/SanskarLoganDev/drive-analyzer.git
   cd drive-analyzer
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## ⚡ Quickstart

Scan your entire C-drive (Windows) and open the web UI:

```bash
# 1. Generate the JSON report
python src/cli.py scan --path C:\ --output report.json

# 2. Serve it on http://localhost:8000
python src/cli.py serve --report report.json --host 0.0.0.0 --port 8000
```

---

## 💻 CLI Usage

All commands live under `src/cli.py`. If you installed with `pip install -e .`, you’ll have a `drive-analyzer` binary.

### `scan`

Generate a JSON report of folder sizes.

```bash
python src/cli.py scan \
  --path   C:\            # folder or drive to scan  
  --output report.json    # output file (relative or absolute)
```

### `analyze`

Inspect the report in your terminal.

```bash
python src/cli.py analyze \
  --report report.json    # path to your scan report  
  --path   C:\Users       # folder to drill into  
  --top    10             # show top-10 largest subfolders
```

### `serve`

Launch the web interface.

```bash
python src/cli.py serve \
  --report report.json    # path to your scan report  
  --host   0.0.0.0        # listen address  
  --port   8000           # HTTP port
```

---

## 📂 Project Structure

```
drive-analyzer/
├── requirements.txt
├── README.md
├── src/
│   ├── scanner.py      # walk & size folders
│   ├── analyzer.py     # aggregate & table-print data
│   ├── web_app.py      # Flask UI factory
│   └── cli.py          # Click-based entry point
└── tests/              # (optional) your pytest suite
```

---

## 🔍 How It Works

1. **`scanner.py`**

   * Uses `os.walk` to traverse directories
   * Sums `os.path.getsize()` per folder
   * Outputs JSON list of `{ path, size_bytes }`

2. **`analyzer.py`**

   * Loads JSON report
   * Buckets into first-level subfolders with `defaultdict`
   * Renders sorted Top-N via **Rich** tables

3. **`web_app.py`**

   * Inline Flask templates via `render_template_string`
   * Simple form for choosing `path` & `top N`
   * Renders HTML table with human-friendly sizes

4. **`cli.py`**

   * Click commands: `scan`, `analyze`, `serve`
   * Easy flag syntax & auto-generated help pages

---

## 🤝 Contributing

1. Fork this repo
2. Create a feature branch (`git checkout -b feature/XYZ`)
3. Commit your changes (`git commit -m "Add XYZ"`)
4. Push to your branch (`git push origin feature/XYZ`)
5. Open a Pull Request here

---

## 📄 License

Distributed under the MIT License.
