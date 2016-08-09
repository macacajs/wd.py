#
# https = //w3c.github.io/webdriver/webdriver-spec.html
# WebDriver Exception
#

from collections import namedtuple
from enum import Enum

ErrorCode = namedtuple('ErrorCode', 'code error_code')


class WebDriverError(Enum):
    """
    Error codes defined in the WebDriver wire protocol.
    """
    NO_SUCH_ELEMENT = ErrorCode(7, 'no such element')
    NO_SUCH_FRAME = ErrorCode(8, 'no such frame')
    UNKNOWN_COMMAND = ErrorCode(9, 'unknown command')
    STALE_ELEMENT_REFERENCE = ErrorCode(10, 'stale element reference')
    ELEMENT_NOT_VISIBLE = ErrorCode(11, 'element not visible')
    INVALID_ELEMENT_STATE = ErrorCode(12, 'invalid element state')
    UNKNOWN_ERROR = ErrorCode(13, 'unknown error')
    ELEMENT_IS_NOT_SELECTABLE = ErrorCode(15, 'element not selectable')
    JAVASCRIPT_ERROR = ErrorCode(17, 'javascript error')
    XPATH_LOOKUP_ERROR = ErrorCode(19, 'invalid selector')
    TIMEOUT = ErrorCode(21, 'timeout')
    NO_SUCH_WINDOW = ErrorCode(23, 'no such window')
    INVALID_COOKIE_DOMAIN = ErrorCode(24, 'invalid cookie domain')
    UNABLE_TO_SET_COOKIE = ErrorCode(25, 'unable to set cookie')
    UNEXPECTED_ALERT_OPEN = ErrorCode(26, 'unexpected alert open')
    NO_ALERT_OPEN = ErrorCode(27, 'no such alert')
    SCRIPT_TIMEOUT = ErrorCode(28, 'script timeout')
    INVALID_ELEMENT_COORDINATES = ErrorCode(29, 'invalid element coordinates')
    IME_NOT_AVAILABLE = ErrorCode(30, 'ime not available')
    IME_ENGINE_ACTIVATION_FAILED = ErrorCode(
        31, 'ime engine activation failed')
    INVALID_SELECTOR = ErrorCode(32, 'invalid selector')
    MOVE_TARGET_OUT_OF_BOUNDS = ErrorCode(34, 'move target out of bounds')


def find_exception_by_code(code):
    """Find name of exception by WebDriver defined error code.

    Args:
        code(str): Error code defined in protocol.

    Returns:
        The error name defined in protocol.
    """
    errorName = None
    for error in WebDriverError:
        if error.value.code == code:
            errorName = error
            break
    return errorName


class WebDriverException(Exception):
    """WebDriver exception.

    Attributes:
        error(str): Error type defined in WebDriver Protocol.
        message(str): A description of the kind of error that occurred.
        screen(str):  If included, a screenshot of the current page as
            a base64 encoded string.
        stacktrace(str): A stack trace report of the error occurred.
    """

    def __init__(self, error=None, message=None, screen=None, stacktrace=None):
        """Initialize the WebDriverException"""
        self.error = error
        self.message = message
        self.screen = screen
        self.stacktrace = stacktrace

    def __str__(self):
        exception_msg = (
            "\nError: {0}\nMessage: {1}\n").format(self.error, self.message)
        if self.screen is not None:
            exception_msg += "Screenshot: available via screen\n"
        if self.stacktrace is not None:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += "Stacktrace:\n%s" % stacktrace
        return exception_msg
