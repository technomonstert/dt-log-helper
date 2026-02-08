# Dynatrace Alert‑Insights (internal multi‑tenant utility)

## 📖 Overview
`dt-alert-insights` is a **private, internal** command‑line tool that helps you quickly answer the question:
> *"Why didn’t a Dynatrace alert fire for this problem?"*

It works against **any number of Dynatrace tenants** using a **single master OAuth client**. The tool also validates that entities comply with **mandatory tags** and **naming conventions** you define in JSON rule files.

---

## 📁 Repository layout (inside your workspace)
```
<repo-root>/
│   README.md           # this file
│   setup.py
│   requirements.txt
│   .gitignore
│   oauth.json          # **master OAuth credentials** (git‑ignored)
│   tenants.json        # **tenant label → base URL map** (git‑ignored)
│
├─ dt_alert_insights/   # Python package
│   ├─ __init__.py
│   ├─ cli.py            # entry point (console script)
│   ├─ core.py           # OAuth helper (single token for all tenants)
│   ├─ utils/
│   │   └─ validator.py  # rule engine (mandatory tags, naming)
│   └─ rules/
│       ├─ mandatory_tags.json      # list of tags that must exist
│       └─ naming_convention.json   # naming‑rule definitions
```

---

## 🔐 Authentication – master OAuth & tenant list (separate files)

### 1️⃣ Create `oauth.json` (master client)
```json
{
  "clientId": "YOUR_MASTER_CLIENT_ID",
  "clientSecret": "YOUR_MASTER_CLIENT_SECRET"
}
```
**How to obtain the client**
1. In **any** Dynatrace tenant go to **Settings → Integration → Dynatrace API**.
2. Click **Create client**, give it a name like `alert‑insights‑master`.
3. Assign the scopes **ReadConfig**, **ReadProblem**, **ReadMetrics**.
4. Copy the **Client ID** and **Client Secret** into the file above.

> The generated token works for **all** tenant URLs, so you only maintain one secret.

### 2️⃣ Create `tenants.json` (label → URL map)
```json
{
  "tenants": {
    "prod-eu": "https://prod-eu.live.dynatrace.com",
    "staging-us": "https://staging-us.live.dynatrace.com",
    "dev-apac": "https://dev-apac.live.dynatrace.com"
    // add more entries as you spin up new environments
  }
}
```
*The JSON key (`prod-eu`, `staging-us`, …) is the **tenant label** you will pass with the `-T/--tenant` flag. If you omit the flag, the tool runs against **all** entries.*

### 3️⃣ Keep both files **out of version control**
Both `oauth.json` and `tenants.json` are listed in `.gitignore`. Store them on an internal, access‑controlled file share or inject them at runtime from a secret manager (Vault, Azure Key Vault, etc.).

---

## 🛠️ Installation (on any dev machine)
```bash
# Clone the repository (or copy the folder from the workspace)
git clone <your‑private‑repo‑url>
cd dynatrace-alert-insights

# Install edit‑able (recommended for internal development)
pip install -e .
```
The console script **`dt-alert-insights`** is now available in your environment.

---

## 🚀 Running the tool
### Single‑tenant execution
```bash
dt-alert-insights \
    -c /secure/config/oauth.json \
    -t /secure/config/tenants.json \
    -T prod-eu \
    -p PROBLEM-ABC12345
```
### Run against **all** tenants (omit `-T`)
```bash
dt-alert-insights \
    -c /secure/config/oauth.json \
    -t /secure/config/tenants.json \
    -p PROBLEM-XYZ789
```
### Optional PID (internal problem ID)
```bash
dt-alert-insights \
    -c ./oauth.json \
    -t ./tenants.json \
    -p PROBLEM-XYZ789 \
    --pid 0b1c2d3e4f5a6b7c8d9e
```
*The output is grouped per tenant, shows any missing mandatory tags, naming‑rule violations, metric recency, and whether a suppression window is active. Fix the reported items, re‑run the command, and when all sections are `PASS/INFO` you can close the ticket.*

---

## 📄 Adding / updating rules
All rule files live under `dt_alert_insights/rules/`.

### Mandatory tags
Edit `dt_alert_insights/rules/mandatory_tags.json` – an array of tag keys that **must be present** on the entity.
```json
[
  "environment",
  "service",
  "team",
  "cost-center"
]
```
### Naming conventions
Edit `dt_alert_insights/rules/naming_convention.json`. Supported keys (the validator can be extended in `utils/validator.py`):
| Key | Type | Meaning |
|-----|------|---------|
| `must_contain_underscore` | boolean | Require an underscore (`_`) in the entity name |
| `regex` | string | Full regular expression the name must match |
| `must_start_with` | string | Prefix that the name must start with |
| `must_end_with` | string | Suffix that the name must end with |
Example:
```json
{
  "must_contain_underscore": true,
  "regex": "^[a-z0-9_]+$",
  "must_start_with": "svc_",
  "must_end_with": "_prod"
}
```
### Custom rule files
You can drop any additional JSON/YAML file in the same folder and import it inside `utils/validator.py`. For example, create `event_name_rules.json` and add a method `check_event_name()` that returns a list of violations. The validator is deliberately simple so you can shape it to your organization’s needs.

---

## 📦 What’s inside the repo (already added to the workspace)
- `setup.py`, `requirements.txt`, `.gitignore`
- **Package**: `dt_alert_insights/`
  - `__init__.py` (empty – marks the package)
  - `cli.py` – parses flags, loads `oauth.json` & `tenants.json`, runs diagnostics.
  - `core.py` – master‑OAuth helper that fetches **one** token and re‑uses it for every tenant.
  - `utils/validator.py` – rule engine implementation.
  - `rules/mandatory_tags.json` – starter list of mandatory tags.
  - `rules/naming_convention.json` – starter naming‑rule definition.

You can now push this folder to your private Git server, clone it on your office laptop, and continue development.

---

## 🛡️ Security checklist
- Keep `oauth.json` and `tenants.json` out of Git (`.gitignore`).
- Store the master client with **read‑only** scopes only.
- Rotate the client secret periodically or when a team member leaves.
- Review rule files before committing – they may contain business‑specific naming conventions.

---

**Happy hacking!** If you need any additional extensions (batch mode, auto‑fix, HTML report, secret‑manager integration) just add new sub‑commands to `cli.py` and update the README accordingly.
