#
# https = //w3c.github.io/webdriver/webdriver-spec.html
# WebDriver Result
#

from .webdriverexception import WebDriverException, find_exception_by_code


class WebDriverResult(object):
    """WebDriver result object.

    Atrributes:
        session_id(str): A UDID used to uniquely identify each session.
        status(int): A status code summarizing the result of the command.
                     A non-zero value indicates that the command failed.
        value(str|list|dict): The response JSON value.
    """

    def __init__(self, session_id, status, value):
        self.session_id = session_id
        self.status = status
        self.value = value

    @classmethod
    def from_object(cls, obj):
        """The factory method to create WebDriverResult from JSON Object.

        Args:
            obj(dict): The JSON Object returned by server.
        """
        return cls(
            obj.get('sessionId', None),
            obj.get('status', 0),
            obj.get('value', None)
        )

    def raise_for_status(self):
        """Raise WebDriverException if returned status is not zero."""
        if not self.status:
            return

        error = find_exception_by_code(self.status)
        message = None
        screen = None
        stacktrace = None

        if isinstance(self.value, str):
            message = self.value
        elif isinstance(self.value, dict):
            message = self.value.get('message', None)
            screen = self.value.get('screen', None)
            stacktrace = self.value.get('stacktrace', None)

        raise WebDriverException(error, message, screen, stacktrace)
