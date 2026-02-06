# Dynatrace Rule Helper – README

## Overview

`dynatrace-rule-helper` is a **command‑line utility** that turns a sample log line (or a JSON log record) into a **Dynatrace PARSE rule** written in the **Dynatrace Pattern Language (DPL)**.  It supports the full set of matchers documented in the Dynatrace *Log‑Processing* guide, can infer literals and matcher types automatically, and respects Dynatrace’s rule‑size limits.

## Installation

```bash
# Clone the repo (or copy the files into a folder)
git clone https://github.com/technomonstert/dt-log-helper.git
cd dt-log-helper

# Install in editable mode (recommended for development)
pip install -e .
```

## Quick start (classic DPL)

```bash
python -m dynatrace_rule_helper.cli \
    -f sample.json \
    -l "Billed Duration:" \
    -v 5034 \
    -t INT \
    -a aws.billed.duration
```

**Output**

```
PARSE(content, "LD 'Billed Duration:' SPACE? INT:aws.billed.duration")
```

> **Note:** The `sample.json` used in this example is shown below, so you don’t need to clone the repository to try it. If you do clone the repo, the same file is located at the repository root (`dt-log-helper/sample.json`).

### `sample.json`

```json
{
  "event.type": "LOG",
  "content": "Billed Duration: 5034"
}
```

Paste the resulting DPL line into **Settings → Log Monitoring → Processing → Add rule** in Dynatrace.

## OpenPipeline (YAML) output

Add `--open-pipeline` to get an OpenPipeline YAML snippet instead of classic DPL:

```bash
python -m dynatrace_rule_helper.cli \
    -f sample.json \
    -l "Billed Duration:" \
    -v 5034 \
    -t INT \
    -a aws.billed.duration \
    --open-pipeline
```

*(OpenPipeline generation is currently a stub – it will emit a minimal YAML structure that can be expanded later.)*

## Full documentation reference

- **Dynatrace Pattern Language (DPL) reference** – https://docs.dynatrace.com/docs/platform/grail/dynatrace-pattern-language
- **Log‑Processing examples (14 use cases)** – https://docs.dynatrace.com/docs/analyze-explore-automate/logs/lma-classic-log-processing/lma-log-processing-examples

## Adding a new matcher (developer guide)

1. Create a new file in `dynatrace_rule_helper/matcher/` that subclasses `BaseMatcher`.
2. Implement the `build()` method to return the appropriate DPL fragment.
3. Register the class in `dynatrace_rule_helper/matcher/__init__.py`.
4. Add unit tests under `tests/`.
5. Run the full test suite (`pytest -q`).

## Advanced usage

If you need matchers that are not covered by the built‑in shortcuts (e.g., `ENUM`, `REGEX`, `MASK`, `DROP`, `RENAME`, `MATH`), you can supply the full DPL fragment directly:

```bash
python -m dynatrace_rule_helper.cli \
    -f mylog.json \
    -a my.field \
    --custom "ENUM('INFO':0,'WARN':1,'ERROR':2):my.field"
```

The `--custom` flag bypasses automatic matcher creation and inserts the fragment verbatim, letting you leverage any DPL construct supported by Dynatrace.
