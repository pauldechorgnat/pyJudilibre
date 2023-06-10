import warnings

from pyjudilibre.exceptions import JudilibreValueError, JudilibreValueWarning

AVAILABLE_ACTIONS = set(["raise", "warn", "ignore"])


def check_value(
    value: str,
    value_name: str = "",
    allowed_values: list[str] = [],
    action_on_check: str = "raise",
) -> bool:
    if action_on_check not in AVAILABLE_ACTIONS:
        raise ValueError(
            "'action_on_check' should be one of ['raise', 'warn', 'ignore']. "
            f"Received '{action_on_check}'"
        )

    if value not in allowed_values:
        if action_on_check == "raise":
            raise JudilibreValueError(
                f"'{value}' is not a valid value for parameter '{value_name}'"
            )
        elif action_on_check == "warn":
            warnings.warn(
                f"'{value}' is not a valid value for parameter '{value_name}'",
                category=JudilibreValueWarning,
            )
        elif action_on_check == "ignore":
            return False

    return True
