#
# Remote Invoker to execute command & handle HTTP communication
#

import logging
try:
    from urllib.parse import urlparse, urlunparse
except ImportError:
    from urlparse import urlparse, urlunparse

from requests import Request, Session

from .util import MemorizeFormatter

LOGGER = logging.getLogger(__name__)


class RemoteInvoker(object):
    """Remote Invoker to execute WebDriver command."""

    def __init__(self, url='http://127.0.0.1:3456/wd/hub'):
        """Init the RemoteInvoker by remote url

        Args:
            url(str|dict): The url of remote server.
        Defaults:
            if url is str:
                url = http://127.0.0.1:3456/wd/hub
            if url is dict:
                url = {
                    'protocol': 'http',
                    'hostname': '127.0.0.1',
                    'port': 3456,
                    'path': '/wd/hub'
                }
        Examples:
            r = RemoteInvoker('http://127.0.0.1:3456/wd/hub')
            r = RemoteInvoker({
                'protocol': 'https',
                'hostname': '127.0.0.1',
                'port': 5678,
                'username': 'macaca',
                'password': '123456',
                'path': '/how/r/u'
            }) => "https://macaca:123456@127.0.0.1:5678/how/r/u"
        """
        self._timeout = None
        if isinstance(url, str):
            parsed_url = urlparse(url)
            scheme = parsed_url.scheme
            netloc = parsed_url.netloc
            if not scheme or not netloc:
                raise ValueError(
                    'Invalid URL \'{0}\': No schema or '
                    'hostname supplied'.format(url))
            elif scheme not in ('http', 'https'):
                raise ValueError(
                    'Invalid URL \'{0}\': Unknown schema \'{1}\', '
                    'only \'http\' and \'https\' '
                    'are supported'.format(url, scheme))
            else:
                self._url = url
        elif isinstance(url, dict):
            scheme = url.get('scheme', None) \
                or url.get('protocol', None) \
                or 'http'
            if scheme not in ('http', 'https'):
                raise ValueError(
                    'Invalid URL Dict: Unknown schema \'{0}\', '
                    'only \'http\' and \'https\' are supported'.format(scheme))
            hostname = url.get('hostname', '127.0.0.1')
            port = url.get('port', 3456)
            path = url.get('path', '/wd/hub')
            username = url.get('username', None)
            password = url.get('password', None)
            if username and password:
                netloc = '{0}:{1}@{2}:{3}'.format(
                    username, password, hostname, port)
            else:
                netloc = '{0}:{1}'.format(hostname, port)
            self._url = urlunparse((scheme, netloc, path, '', '', ''))
        else:
            raise TypeError(
                'URL \'{0}\' should be a string or a dict.'.format(url))

        self._formatter = MemorizeFormatter()

    def execute(self, command, data={}):
        """Format the endpoint url by data and then request the remote server.

        Args:
            command(Command): WebDriver command to be executed.
            data(dict): Data fulfill the uri template and json body.

        Returns:
            A dict represent the json body from server response.

        Raises:
            KeyError: Data cannot fulfill the variable which command needed.
            ConnectionError: Meet network problem (e.g. DNS failure,
                refused connection, etc).
            Timeout: A request times out.
            HTTPError: HTTP request returned an unsuccessful status code.
        """
        method, uri = command
        try:
            path = self._formatter.format_map(uri, data)
            body = self._formatter.get_unused_kwargs()
            url = "{0}{1}".format(self._url, path)
            return self._request(method, url, body)
        except KeyError as err:
            LOGGER.debug(
                'Endpoint {0} is missing argument {1}'.format(uri, err))
            raise

    def _request(self, method, url, body):
        """Internal method to send request to the remote server.

        Args:
            method(str): HTTP Method(GET/POST/PUT/DELET/HEAD).
            url(str): The request url.
            body(dict): The JSON object to be sent.

        Returns:
            A dict represent the json body from server response.

        Raises:
            ConnectionError: Meet network problem (e.g. DNS failure,
                refused connection, etc).
            Timeout: A request times out.
            HTTPError: HTTP request returned an unsuccessful status code.
        """
        if method != 'POST' and method != 'PUT':
            body = None

        s = Session()

        LOGGER.debug(
            'Method: {0}, Url: {1}, Body: {2}.'.format(method, url, body))

        req = Request(method, url, json=body)
        prepped = s.prepare_request(req)

        res = s.send(prepped, timeout=self._timeout or None)
        res.raise_for_status()
        # TODO try catch
        return res.json()
