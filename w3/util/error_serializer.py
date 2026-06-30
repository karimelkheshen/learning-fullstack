from pydantic import ValidationError


def has_only_semantic_errors(exc: ValidationError) -> bool:
    """
    returns true if every error is a value_error (custom validator failure)
    false if any error is structural (missing field, wrong type, etc)
    """
    return all(err["type"] == "value_error" for err in exc.errors())


def serialize_validation_errors(exc: ValidationError) -> list[dict]:
    """turns a pydantic validation error into something json can handle"""
    errors = []
    for err in exc.errors():
        errors.append(
            {
                "type": err.get("type"),
                "loc": err.get("loc"),
                "msg": err.get("msg"),
                "input": err.get("input"),
            }
        )
    return errors
