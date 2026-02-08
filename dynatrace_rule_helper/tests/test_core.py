# Dynatrace Rule Helper – test suite (partial)

import json
import pathlib
import sys

import pytest

from dynatrace_rule_helper.engine.core import process_log_file

# Fixtures – paths to the example JSON files (to be added later)
FIXTURE_DIR = pathlib.Path(__file__).parent / "fixtures"

def load_fixture(name: str) -> str:
    return str(FIXTURE_DIR / name)

# Example 1 – fix timestamp & loglevel (from docs)
def test_example1_timestamp_and_loglevel():
    fixture = load_fixture("example1.json")
    rule = process_log_file(
        file_path=fixture,
        literals="",
        values="",
        matcher_types="",
        aliases="timestamp,loglevel",
    )
    # Expected fragments (order may vary but should contain both)
    assert "TIMESTAMP('MMMMM d, yyyy HH:mm:ss'):timestamp" in rule
    assert "UPPER:loglevel" in rule
    assert rule.startswith("PARSE(content, ")

# Example 2 – billed duration numeric extraction
def test_example2_billed_duration():
    fixture = load_fixture("example2.json")
    rule = process_log_file(
        file_path=fixture,
        literals="Billed Duration:",
        values="5034",
        matcher_types="INT",
        aliases="aws.billed.duration",
    )
    assert "LD 'Billed Duration:' SPACE? INT:aws.billed.duration" in rule

# Example 3 – JSON field extraction (simple payload)
def test_example3_json_field():
    fixture = load_fixture("example3.json")
    rule = process_log_file(
        file_path=fixture,
        literals="",
        values="",
        matcher_types="JSON",
        aliases="payload",
    )
    assert "JSON:payload" in rule

# Example 4 – multiple LD extractions in one rule
def test_example6_enum_custom():
    # Suppose we want to map loglevel strings to numeric enum values
    fixture = load_fixture("example2.json")  # reuse example2 which has loglevel INFO
    # Use custom DPL fragment to create ENUM matcher
    custom_fragment = "ENUM('INFO':0,'WARN':1,'ERROR':2):loglevel_enum"
    rule = process_log_file(
        file_path=fixture,
        literals="",
        values="",
        matcher_types="",
        aliases="loglevel_enum",
        custom=custom_fragment,
    )
    assert "ENUM('INFO':0,'WARN':1,'ERROR':2):loglevel_enum" in rule

# Add more tests for ENUM, REGEX, ARRAY, MASK, DROP, etc. as needed.
