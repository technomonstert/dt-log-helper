# Dynatrace Rule Helper – README

## Overview

`dynatrace-dpl-helper` (formerly **dynatrace‑rule‑helper**) is a **tiny command‑line utility** that turns a sample log line (or a JSON log record) into a **Dynatrace PARSE rule** written in the Dynatrace Pattern Language (DPL).  It is deliberately **zero‑dependency** (aside from Python >=3.8) and is meant for **Dynatrace‑focused users** who may not be comfortable with Python.

---

## 🎯 Who is this for?

- **Dynatrace engineers or admins** who want to create DPL rules quickly but have **no Python experience**.
- Teams that need a **step‑by‑step guide** from "install" to "paste rule into the UI".
- Anyone who prefers **clear Windows instructions** and a minimal learning curve.

---

## 📦 Installation (Windows – complete walk‑through)

1. **Install Python**
   - Go to https://www.python.org/downloads/windows/ and download the **latest stable release** (3.11.x works fine).
   - Run the installer. **IMPORTANT:** check **"Add Python to PATH"** on the first screen, then click **"Install Now"**.
   - After installation, open a **Command Prompt** (`Win + R`, type `cmd`, Enter) and verify:
     ```cmd
     python --version
     ```
     You should see something like `Python 3.11.x`.

2. **Upgrade pip** (the Python package manager) – still in the same Command Prompt:
   ```cmd
   python -m pip install --upgrade pip
   ```

3. **Install the helper**
   ```cmd
   pip install dynatrace-dpl-helper
   ```
   You’ll see a short success message.  The console script `dynatrace-dpl-helper` is now available.

---

## 🚀 Quick‑start (the classic DPL rule)

1. **Create a sample file** (you can copy‑paste this into a new file called `sample.json` in any folder, e.g., `C:\temp\sample.json`):
   ```json
   {
     "event.type": "LOG",
     "content": "Billed Duration: 5034"
   }
   ```
2. **Run the helper** (adjust the path to where you saved `sample.json`):
   ```cmd
   dynatrace-dpl-helper \
       -f C:\temp\sample.json \
       -l "Billed Duration:" \
       -v 5034 \
       -t INT \
       -a aws.billed.duration
   ```
   *If you prefer the `python -m` form, you can also run:*
   ```cmd
   python -m dynatrace_rule_helper.cli -f C:\temp\sample.json -l "Billed Duration:" -v 5034 -t INT -a aws.billed.duration
   ```
3. **Result** (printed to the console):
   ```
   PARSE(content, "LD 'Billed Duration:' SPACE? INT:aws.billed.duration")
   ```
4. **Paste the rule** into the Dynatrace UI:
   - Open Dynatrace → **Settings** → **Log Monitoring** → **Processing** → **Add rule**.
   - Paste the entire line (including the leading `PARSE(`) into the rule editor.
   - Click **Save**.

---

## 📋 All CLI flags (plain‑English description)

| Flag | Alias | Required? | What to put in | Example |
|------|-------|----------|----------------|---------|
| `-f` | `--file` | ✅ | Path to a **JSON** file (or a plain‑text file) that contains the sample log. | `C:\temp\sample.json` |
| `-l` | `--literal` | ✅ | The **exact literal string** you want to match (including spaces, punctuation). | `"Billed Duration:"` |
| `-v` | `--value` | ✅ | The **value** that follows the literal – this determines the matcher type if you don’t supply `-t`. | `5034` |
| `-t` | `--type` | ✅ | Desired **matcher type**. Common values:
- `INT` – integer numbers
- `FLOAT` – floating‑point numbers
- `STRING` – free text
- `LD` – literal‑delimiter pattern
- `TIMESTAMP` – datetime values
- `IPADDR` – IP addresses
- `URL` – URLs
- `JSONPATH` – for nested JSON extraction |
  `INT` |
| `-a` | `--alias` | ✅ | The **Dynatrace attribute name** where the extracted value will be stored. Use dot‑notation for nested attributes. | `aws.billed.duration` |
| `--custom` | – | ❌ | Provide a **full DPL fragment** (≥ 250 chars) if the built‑in matcher shortcuts are insufficient (e.g., `ENUM`, `REGEX`, `MASK`). The fragment is inserted verbatim. | `"ENUM('INFO':0,'WARN':1,'ERROR':2):my.field"` |
| `--dry-run` | – | ❌ | **Only print** the generated rule; do **not** write any files. Useful for CI pipelines. |
| `--verbose` | – | ❌ | Show **debug information** (how the tool inferred the matcher, limit checks, etc.). |
| `--export-pdf` | – | ❌ | Export a **PDF snapshot** of the rule. Provide a file path, e.g., `--export-pdf C:\temp\rule.pdf`. Requires `wkhtmltopdf` to be installed on the machine. |

---

## 🗂️ Sample files & where to put them

- **sample.json** – place it anywhere you like; just give the full path to `-f`.
- If you work with **nested JSON**, create a file like `nested.json`:
  ```json
  {
    "event.type": "LOG",
    "content": {
      "request": {"id": "abc123", "durationMs": 542},
      "status": "OK"
    }
  }
  ```
  Then call the tool with a JSONPath matcher:
  ```cmd
  dynatrace-dpl-helper -f C:\temp\nested.json -l "$.request.id,$.request.durationMs" -a request.id,request.duration -t JSONPATH,JSONPATH
  ```
  The output will contain two `JSON_PATH` fragments.

---

## 📤 What the output means (Dynatrace side)

- The **`PARSE(content, "…")`** line tells Dynatrace to look at the `content` field of a log event and apply the pattern inside.
- **`LD`** = *Literal‑Delimiter* – matches a literal string followed optionally by a delimiter (e.g., a space).
- **`INT`**, **`FLOAT`**, etc., are the *matcher types* that extract the value and bind it to the alias you supplied with `-a`.
- After the rule is saved, Dynatrace will start extracting the value for every future log that matches the pattern, making it available for dashboards, alerts, and analytics.

---

## 🛠️ Troubleshooting (common pitfalls for non‑Python users)

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `python` is not recognized | Python was not added to PATH during installation | Re‑run the installer and tick *Add Python to PATH* or add `C:\Python311\Scripts` and `C:\Python311\` to your system `PATH` manually. |
| `ModuleNotFoundError: No module named 'dynatrace_rule_helper'` | The package was installed for a different Python version | Run `python -m pip install dynatrace-dpl-helper` using the **same** `python` you invoke later (check with `where python`). |
| `JSONDecodeError` | The file supplied with `-f` is not valid JSON | Verify the file with a JSON validator (e.g., https://jsonlint.com) or use a plain‑text log file instead. |
| No output or empty rule | You omitted a required flag (`-f`, `-l`, `-v`, `-t`, `-a`) | Re‑run the command and ensure all required flags are present. |
| PDF export fails | `wkhtmltopdf` not installed or not in PATH | Download https://wkhtmltopdf.org/downloads.html, install, and add its `bin` folder to PATH. |
| “Rule too large – exceeds 10 KB” | The generated DPL string is longer than Dynatrace’s limit | Use a **custom fragment** (`--custom`) to split the rule or simplify the pattern. |

---

## 📚 Full documentation reference

- **Dynatrace Pattern Language (DPL) reference** – https://docs.dynatrace.com/docs/platform/grail/dynatrace-pattern-language
- **Log‑Processing examples (14 use cases)** – https://docs.dynatrace.com/docs/analyze-explore-automate/logs/lma-classic-log-processing/lma-log-processing-examples

---

## 📦 Development & contribution (for the curious)

If you *do* have Python experience and want to extend the helper (add a new matcher, improve tests, etc.), the repo is on GitHub:

```bash
git clone https://github.com/technomonstert/dt-log-helper.git
cd dt-log-helper
pip install -e .   # editable install for development
pytest -q          # run the test suite
```

Pull requests are welcome!

---

## 📜 License

`dynatrace-dpl-helper` is released under the **MIT License**.
