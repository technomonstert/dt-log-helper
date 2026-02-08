"""Core processing function – orchestrates loading the JSON log, applying matchers,
building the DPL rule, and enforcing limits.
"""

import json
from pathlib import Path
from typing import Optional, List

from dynatrace_rule_helper.engine.inference import infer_literal_from_value, guess_matcher_type
from dynatrace_rule_helper.engine.limits import enforce_rule_size, validate_literal, validate_fragment_count
from dynatrace_rule_helper.engine.pattern_builder import build_parse_rule

# Import concrete matcher classes
from dynatrace_rule_helper.matcher.timestamp import TimestampMatcher
from dynatrace_rule_helper.matcher.ld import LDMatcher
from dynatrace_rule_helper.matcher.int import IntMatcher
from dynatrace_rule_helper.matcher.float import FloatMatcher
from dynatrace_rule_helper.matcher.string import StringMatcher
from dynatrace_rule_helper.matcher.ipaddr import IPAddrMatcher
from dynatrace_rule_helper.matcher.url import URLMatcher
from dynatrace_rule_helper.matcher.json_matcher import JSONMatcher
# Future: import EnumMatcher, RegexMatcher, etc.

MATCHER_MAP = {
    "INT": IntMatcher,
    "FLOAT": FloatMatcher,
    "STRING": StringMatcher,
    "IPADDR": IPAddrMatcher,
    "URL": URLMatcher,
    "JSON": JSONMatcher,
    # "ENUM": EnumMatcher,
    # "REGEX": RegexMatcher,
    # "TIMESTAMP": TimestampMatcher (handled specially)
}

def process_log_file(
    file_path: str,
    literals: Optional[str] = None,
    values: Optional[str] = None,
    matcher_types: Optional[str] = None,
    aliases: str = "",
    enum_file: Optional[str] = None,
    open_pipeline: bool = False,
    verbose: bool = False,
    custom: Optional[str] = None,
) -> str:
    """Main entry point used by the CLI.

    Parameters
    ----------
    file_path: str
        Path to the JSON file containing a ``content`` field.
    literals: Optional[str]
        Comma‑separated literals (one per extraction). May be ``None`` – then inference is used.
    values: Optional[str]
        Comma‑separated sample values (used for literal inference and matcher guessing).
    matcher_types: Optional[str]
        Comma‑separated DPL matcher names (INT, FLOAT, STRING, …). If omitted we infer.
    aliases: str
        Comma‑separated export names – required.
    enum_file: Optional[str]
        Path to a JSON file with enum mappings (future support).
    open_pipeline: bool
        If True we would emit an OpenPipeline YAML snippet (stub for now).
    verbose: bool
        Enable debug prints.
    custom: Optional[str]
        Comma‑separated raw DPL fragment(s) that bypass automatic matcher creation.
    """
    # ------------------------------------------------------------------
    # 1️⃣ Load the JSON file
    # ------------------------------------------------------------------
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except Exception as exc:
        raise Exception(f"Failed to read JSON file: {exc}")

    content = data.get("content")
    if not content:
        raise Exception("JSON must contain a 'content' field with the raw log line.")

    # ------------------------------------------------------------------
    # 2️⃣ Parse CLI‑level CSV arguments into lists
    # ------------------------------------------------------------------
    alias_list = [a.strip() for a in aliases.split(",") if a.strip()]
    literal_list = [l.strip() for l in literals.split(",")] if literals else []
    value_list = [v.strip() for v in values.split(",")] if values else []
    type_list = [t.strip().upper() for t in matcher_types.split(",")] if matcher_types else []

    count = len(alias_list)
    if literal_list and len(literal_list) != count:
        raise Exception("Number of literals must match number of aliases.")
    if value_list and len(value_list) != count:
        raise Exception("Number of values must match number of aliases.")
    if type_list and len(type_list) != count:
        raise Exception("Number of matcher types must match number of aliases.")

    fragments: List[str] = []

    # Parse custom fragments if provided (they bypass automatic matcher creation)
    # Use a simple split only when multiple aliases are expected; otherwise keep the whole string.
    if custom and count == 1:
        custom_list = [custom]
    else:
        custom_list = [c.strip() for c in custom.split(",")] if custom else []

    # If custom fragments are supplied, we expect them to already be valid DPL fragments.
    # The alias list is still required for consistency, but we won\'t use it for building.
    if custom_list:
        if len(custom_list) != count:
            raise Exception("Number of custom fragments must match number of aliases.")
        fragments = custom_list
    else:
        # ------------------------------------------------------------------
        # 3️⃣ Build a matcher for each extraction request (original path)
        # ------------------------------------------------------------------
        for idx, alias in enumerate(alias_list):
            # Resolve literal and value for this alias
            literal = literal_list[idx] if literal_list else None
            value = value_list[idx] if value_list else None
            # If literal is missing but we have a value, infer it from content
            if not literal and value:
                literal, _ = infer_literal_from_value(content, value)
            if literal:
                validate_literal(literal)
            # Override matcher type if explicit types were provided
            if type_list:
                mtype = type_list[idx]
            else:
                # Determine matcher type – falling back to inference when missing
                if alias.lower() == "timestamp":
                    mtype = "TIMESTAMP"
                elif alias.lower() == "loglevel":
                    mtype = "UPPER"
                else:
                    if value:
                        mtype = guess_matcher_type(value)
                    else:
                        mtype = "STRING"
            # Special handling for timestamps – DPL has a dedicated function
            if mtype == "TIMESTAMP":
                pattern = TimestampMatcher.infer_pattern(content)
                if not pattern:
                    raise Exception("Could not infer a timestamp pattern from the log line.")
                matcher = TimestampMatcher(export_name=alias, pattern=pattern, literal=literal)
                fragments.append(matcher.build())
            elif mtype == "UPPER":
                # Upper‑case transformation – no literal needed
                fragments.append(f"UPPER:{alias}")
                continue
            else:
                MatcherCls = MATCHER_MAP.get(mtype)
                if not MatcherCls:
                    raise Exception(f"Unsupported matcher type: {mtype}")
                # JSONMatcher does not take a literal argument
                if MatcherCls.__name__ == "JSONMatcher":
                    matcher = MatcherCls(export_name=alias)
                else:
                    matcher = MatcherCls(export_name=alias, literal=literal)
                fragments.append(matcher.build())


    # ------------------------------------------------------------------
    # 4️⃣ Validate overall limits
    # ------------------------------------------------------------------
    validate_fragment_count(fragments)
    dpl_rule = build_parse_rule(fragments)
    enforce_rule_size(dpl_rule)

    # ------------------------------------------------------------------
    # 5️⃣ OpenPipeline stub – if the user requested it we would translate the
    #    fragments into an OpenPipeline YAML structure.  For now we just return
    #    the classic DPL string.
    # ------------------------------------------------------------------
    if open_pipeline:
        # Future implementation: translate fragments into OpenPipeline JSON/YAML.
        return dpl_rule  # placeholder
    return dpl_rule
