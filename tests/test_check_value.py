import pytest

from pyjudilibre.exceptions import JudilibreValueError, JudilibreValueWarning
from pyjudilibre.utils import check_value


def test_check_value():
    result = check_value(
        value="a",
        value_name="my_variable",
        allowed_values=["a", "b", "c"],
        action_on_check="raise",
    )

    assert result is True

    result = check_value(
        value="a",
        value_name="my_variable",
        allowed_values=["a", "b", "c"],
        action_on_check="warn",
    )

    assert result is True

    result = check_value(
        value="a",
        value_name="my_variable",
        allowed_values=["a", "b", "c"],
        action_on_check="ignore",
    )

    assert result is True

    with pytest.raises(ValueError):
        result = check_value(
            value="a",
            value_name="my_variable",
            allowed_values=["a", "b", "c"],
            action_on_check="other_action",
        )


def test_check_value_wrong():
    with pytest.raises(JudilibreValueError):
        check_value(
            value="d",
            value_name="my_variable",
            allowed_values=["a", "b", "c"],
            action_on_check="raise",
        )

    with pytest.warns(JudilibreValueWarning):
        check_value(
            value="d",
            value_name="my_variable",
            allowed_values=["a", "b", "c"],
            action_on_check="warn",
        )

    result = check_value(
        value="d",
        value_name="my_variable",
        allowed_values=["a", "b", "c"],
        action_on_check="ignore",
    )

    assert result is False

    with pytest.raises(ValueError):
        check_value(
            value="d",
            value_name="my_variable",
            allowed_values=["a", "b", "c"],
            action_on_check="other_action",
        )
