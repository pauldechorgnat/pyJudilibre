class JudilibreDecisionNotFoundError(Exception):
    pass


class JudilibreAPIDownError(Exception):
    pass


class JudilibreWrongCredentialsError(Exception):
    pass


class JudilibreWrongURLError(Exception):
    pass


class JudilibreValueWarning(Warning):
    pass


class JudilibreValueError(ValueError):
    pass


class JudilibreResourceNotFoundError(Exception):
    pass
