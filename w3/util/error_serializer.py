from pydantic import ValidationError


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
