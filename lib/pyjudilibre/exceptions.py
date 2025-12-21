class JudilibreDecisionNotFoundError(Exception):
    pass


class JudilibreAPIDownError(Exception):
    pass


class JudilibreWrongURLError(Exception):
    pass


class JudilibreValueWarning(Warning):
    pass


class JudilibreValueError(ValueError):
    pass


class JudilibreDownloadFileError(Exception):
    pass


class JudilibreUnauthorizedError(Exception):
    pass


class JudilibreInvalidRequestError(Exception):
    pass


class JudilibreInvalidCredentialsError(Exception):
    pass


class JudilibreResourceNotFoundError(Exception):
    pass


class JudilibreSuspiciousActivityError(Exception):
    pass


class JudilibreTooManyRequestError(Exception):
    pass


class JudilibreInternalError(Exception):
    pass


ERROR_CODES_TO_EXCEPTIONS = {
    400: JudilibreInvalidRequestError,
    401: JudilibreInvalidCredentialsError,
    403: JudilibreUnauthorizedError,
    404: JudilibreResourceNotFoundError,
    423: JudilibreSuspiciousActivityError,
    429: JudilibreTooManyRequestError,
    500: JudilibreInternalError,
}

# def catch_response(response: Response) -> Response:
#     if response.status_code == 400:
#         message = response.headers.get("WWW-Authenticate", "")
#         if message == (
#             'Bearer realm="DefaultRealm",error="invalid_request"'
#             ',error_description="Unable to find token in the message"'
#         ):
#             raise JudilibreInvalidCredentialsError("Credentials are not valid.")
#     if response.status_code == 404:
#         raise JudilibreResourceNotFoundError("Resource is not found")
#     return response
