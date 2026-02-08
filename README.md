# Dynatrace Log Rule Helper

Generate Dynatrace log parsing rules from real log examples — without writing DPL by hand.

Dynatrace log processing rules use Dynatrace Pattern Language (DPL), a small but strict domain-specific language.
Writing these rules manually is slow, error-prone, and difficult to validate.

This tool takes a sample log line (JSON) and produces a ready-to-paste Dynatrace log processing rule.

No DPL expertise required.

---

## Why This Tool Exists

In Dynatrace, extracting fields from logs requires defining log processing rules using DPL constructs like:

- PARSE
- LD
- SPACE?
- INT, FLOAT, STRING

Common problems:
- One missing token breaks the rule
- No syntax validation in the UI
- No preview or test extraction
- Difficult to translate human-readable logs into DPL grammar

This tool solves that by translating log examples into valid DPL rules automatically.

---

## What This Tool Is (and Is Not)

### What it is
- A helper utility that converts log examples into Dynatrace log parsing rules
- A DPL rule generator
- A copy-paste companion for Dynatrace Log Monitoring configuration

### What it is not
- Not a Dynatrace API client
- Not a log ingestion tool
- Not a replacement for Dynatrace log processing

Python is only the implementation language — users do not need Python knowledge.

---

## Who Should Use This

- Dynatrace engineers working with log parsing
- SREs and observability engineers creating log-based attributes
- Anyone tired of manually writing DPL rules
- Teams building dashboards, alerts, and metrics from logs

---

## Installation

### From PyPI (recommended)

pip install dynatrace-dpl-helper

### From source

``git clone https://github.com/technomonstert/dt-log-helper.git
cd dt-log-helper
pip install -e .``

---




## Supported Command-Line Flags

| Short Flag | Long Flag | Description | Example |
|-----------|-----------|-------------|---------|
| `-f` | `--file` | Path to the sample log file (JSON or plain text) | `--file sample.json` |
| `-l` | `--literal` | Fixed text or JSONPath expression to match in the log | `--literal "Billed Duration:"` |
| `-v` | `--value` | Example value to extract from the log | `--value 5034` |
| `-t` | `--type` | Matcher type (`INT`, `FLOAT`, `STRING`, `JSONPATH`) | `--type INT` |
| `-a` | `--alias` | Attribute name to create in Dynatrace | `--alias aws.billed.duration` |
|  | `--dry-run` | Print the generated DPL rule without writing files | `--dry-run` |
|  | `--verbose` | Enable verbose/debug output | `--verbose` |

---

## Notes

- Multiple values can be provided as required.
- Attribute aliases do not need any order.



## Quick Start

### Input log example (Assuming this is the content of sample.json)

``{
  "content": "Billed Duration: 5034"
}``

### Command

``
dynatrace-dpl-helper --file sample.json --literal "Billed Duration:" --value 5034 --type INT --alias aws.billed.duration
``

### Output (DPL rule)
``
PARSE(content, "LD 'Billed Duration:' SPACE? INT:aws.billed.duration")
``
Paste this directly into:
``
Dynatrace → Settings → Log Monitoring → Processing → Add processing rule
``

```
Note:
This does not always produce syntactically valid DPL rules as this tool is still in development. Always validate this with test option provided at Dynatrace log processing rule creation page. 
```
---

## License

MIT License
