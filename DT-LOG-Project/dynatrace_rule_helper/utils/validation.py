"""Simple validation helpers for the incoming JSON payload.
"""

def validate_log_record(record: dict) -> None:
    """Ensure the dict contains at least a ``content`` key.
    Raises ``ValueError`` if the requirement is not met.
    """
    if not isinstance(record, dict):
        raise ValueError("Log record must be a JSON object.")
    if "content" not in record:
        raise ValueError("Log record must contain a 'content' field.")
