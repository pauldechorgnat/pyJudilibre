import warnings

from pyjudilibre.exceptions import JudilibreValueError, JudilibreValueWarning

AVAILABLE_ACTIONS = set(["raise", "warn", "ignore"])


def check_value(
    value: str,
    value_name: str = "",
    allowed_values: list[str] = [],
    action_on_check: str = "raise",
) -> bool:
    """Function that check if a value is in a set of allowed values and acts on it.

    Args:
        value (str): value of the parameter to check
        value_name (str, optional): name of the parameter to check.
            Defaults to "".
        allowed_values (list[str], optional): list or set of allowed values.
            Defaults to [].
        action_on_check (str, optional): action to take if the check is not valid.
            Must be one of "raise", "warn" or "ignore"
            Defaults to "raise".

    Raises:
        ValueError: raised if the value of action_on_check is not valid.
        JudilibreValueError: raised if the value of the parameter is not valid.

    Returns:
        bool: True if the parameter is a valid value. False otherwise.
    """
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
