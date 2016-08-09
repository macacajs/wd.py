#
# https = //w3c.github.io/webdriver/webdriver-spec.html
# WebDriver Protocol Implemenation
#

from base64 import decodebytes

from retrying import retry

from .asserters import is_displayed
from .command import Command
from .locator import Locator
from .remote_invoker import RemoteInvoker
from .util import add_element_extension_method, value_to_key_strokes, fluent
from .webdriverresult import WebDriverResult
from .webdriverexception import WebDriverException
from .webelement import WebElement


class WebDriver:
    """The WebDriver Object to implement most part of WebDriver protocol.

    Attributes:
        session_id(str): A UDID used to uniquely identify each session.
        capabilities(dict): The capabilities of the driver/browserreturned by
            remote server.
        desired_capabilities(dict): The desired capabilities requested by the
            local end.
        remote_invoker(RemoteInvoker): The remote invoker responsible for send
            request.
    """

    def __init__(self, desired_capabilities, url='http://127.0.0.1:3456/wd/hub'):
        """Initialize the WebDriver

        Args:
            desired_capabilities(dict): The desired capabilities requested by
                the local end.
            url(str): The url of remote server, default: localhost:3456/wd/hub.
        """
        self.session_id = None
        self.capabilities = None
        self.desired_capabilities = desired_capabilities
        self.remote_invoker = RemoteInvoker(url)

    def __repr__(self):
        return '<{0.__name__} (session="{1}")>'.format(
            type(self), self.session_id)

    def _execute(self, command, data=None, unpack=True):
        """ Private method to execute command.

        Args:
            command(Command): The defined command.
            data(dict): The uri variable and body.
            uppack(bool): If unpack value from result.

        Returns:
            The unwrapped value field in the json response.
        """
        if not data:
            data = {}
        if self.session_id is not None:
            data.setdefault('session_id', self.session_id)
        data = self._wrap_el(data)
        res = self.remote_invoker.execute(command, data)
        ret = WebDriverResult.from_object(res)
        ret.raise_for_status()
        if self.session_id and self.session_id != ret.session_id:
            raise WebDriverException('invalid session id')
        ret.value = self._unwrap_el(ret.value)
        if not unpack:
            return ret
        return ret.value

    def _unwrap_el(self, value):
        """Convert {'Element': 1234} to WebElement Object

        Args:
            value(str|list|dict): The value field in the json response.

        Returns:
            The unwrapped value.
        """
        if isinstance(value, dict) and 'ELEMENT' in value:
            element_id = value.get('ELEMENT')
            return WebElement(element_id, self)
        elif isinstance(value, list):
            return [self._unwrap_el(item) for item in value]
        else:
            return value

    def _wrap_el(self, value):
        """Convert WebElement Object to {'Element': 1234}

        Args:
            value(str|list|dict): The local value.

        Returns:
            The wrapped value.
        """
        if isinstance(value, dict):
            return {k: self._wrap_el(v) for k, v in value.items()}
        elif isinstance(value, WebElement):
            return {'ELEMENT': value.element_id}
        elif isinstance(value, list):
            return [self._wrap_el(item) for item in value]
        else:
            return value

    @fluent
    def attach(self, session_id):
        """Attach to given Session.

        Args:
            session_id(str): The given session ID

        Returns:
            WebDriver Object.
        """
        self.session_id = session_id

    @fluent
    def init(self):
        """Create Session by desiredCapabilities

        Returns:
            WebDriver Object.
        """
        resp = self._execute(Command.NEW_SESSION, {
            'desiredCapabilities': self.desired_capabilities
        }, False)
        resp.raise_for_status()
        self.session_id = str(resp.session_id)
        self.capabilities = resp.value

    @fluent
    def quit(self):
        """Quit the driver.

        Returns:
            WebDriver Object.
        """
        self._execute(Command.QUIT)

    @fluent
    def get(self, url):
        """
        Loads a web page in the current browser session.

        Args:
            url(str): The URL to navigate to.

        Returns:
            WebDriver Object.

        Raises:
            WebDriverException.
        """
        self._execute(Command.GET, {'url': url})

    @property
    def current_url(self):
        """Gets the URL of the current page.

        Returns:
            Return the URL of the current page.
        """
        return self._execute(Command.GET_CURRENT_URL)

    @fluent
    def back(self):
        """Back.

        Returns:
            WebDriver Object.
        """
        self._execute(Command.GO_BACK)

    @fluent
    def forward(self):
        """Forward.

        Returns:
            WebDriver Object.
        """
        self._execute(Command.GO_FORWARD)

    @fluent
    def refresh(self):
        """Refresh.

        Returns:
            WebDriver Object.
        """
        self._execute(Command.REFRESH)

    @property
    def title(self):
        """Get the current page title.
        """
        return self._execute(Command.GET_TITLE)

    @property
    def current_window_handle(self):
        """Returns the handle of the current window.
        """
        return self._execute(Command.GET_CURRENT_WINDOW_HANDLE)

    @fluent
    def close(self):
        """Closes the current window.

        Returns:
            WebDriver Object.
        """
        self._execute(Command.CLOSE)

    @fluent
    def switch_to_window(self, window_name):
        """Switch to the given window.

        Args:
            window_name(str): The window to change focus to.

        Returns:
            WebDriver Object.
        """
        data = {
            'name': window_name
        }
        self._execute(Command.SWITCH_TO_WINDOW, data)

    @property
    def window_handles(self):
        """Returns the handles of all windows within the current session.
        """
        return self._execute(Command.GET_WINDOW_HANDLES)

    @fluent
    def maximize_window(self):
        """Maximizes the current window.

        Returns:
            WebDriver Object.
        """
        self._execute(Command.MAXIMIZE_WINDOW,
            {"window_handle": "current"})

    @fluent
    def set_window_size(self, width, height, window_handle='current'):
        """Sets the width and height of the current window.

        Args:
            width(int): the width in pixels
            height(int): the height in pixels

        Returns:
            WebDriver Object.
        """
        self._execute(Command.SET_WINDOW_SIZE, {
            'width': int(width),
            'height': int(height),
            'window_handle': window_handle})

    def get_window_size(self, window_handle='current'):
        """Gets the width and height of the current window.

        Returns:
            A dict contains width and height
        """
        return self._execute(Command.GET_WINDOW_SIZE,
            {'window_handle': window_handle})

    @fluent
    def set_window_position(self, x, y, window_handle='current'):
        """Sets the x,y position of the current window.

        Args:
            x(int): the x-coordinate in pixels.
            y(int): the y-coordinate in pixels.

        Returns:
            WebDriver Object.
        """
        self._execute(Command.SET_WINDOW_POSITION, {
            'x': int(x),
            'y': int(y),
            'window_handle': window_handle})

    def get_window_position(self, window_handle='current'):
        """
        Gets the x,y position of the current window.
        :Usage:
            driver.get_window_position()
        """
        return self._execute(Command.GET_WINDOW_POSITION, {
            'window_handle': window_handle})

    @property
    def context(self):
        """returns the current context (Native or WebView)."""
        return self._execute(Command.CURRENT_CONTEXT_HANDLE)

    @property
    def contexts(self):
        """returns a list of available contexts"""
        return self._execute(Command.CONTEXT_HANDLES)

    @context.setter
    def context(self, new_context):
        """sets the current context"""
        self._execute(Command.SWITCH_TO_CONTEXT, {"name": new_context})

    @fluent
    def move_to(self, element, x=0, y=0):
        """Move the mouse by an offset of the specificed element.

        Args:
            element(WebElement): WebElement Object.
            x(float): X offset to move to, relative to the
                      top-left corner of the element.
            y(float): Y offset to move to, relative to the
                      top-left corner of the element.

        Returns:
            WebDriver object.
        """
        self._execute(Command.MOVE_TO, {
            'element': element.element_id,
            'x': x,
            'y': y
        })

    @fluent
    def flick(self, element, x, y, speed):
        """Flick on the touch screen using finger motion events.
           This flickcommand starts at a particulat screen location.

        Args:
            element(WebElement): WebElement Object where the flick starts.
            x(float}: The x offset in pixels to flick by.
            y(float): The y offset in pixels to flick by.
            speed(float) The speed in pixels per seconds.

        Returns:
            WebDriver object.
        """
        self._execute(Command.FLICK, {
            'element': element.element_id,
            'x': x,
            'y': y,
            'speed': speed
        })

    @fluent
    def tap(self, element):
        """Single tap on the touch enabled device..

        Args:
            element(WebElement): WebElement Object to single tap on.

        Returns:
            WebDriver object.
        """
        self._execute(Command.SINGLE_TAP, {
            'element': element.element_id,
        })

    @fluent
    def keys(self, value):
        """Send a sequence of key strokes.

        Args:
            value(str|int|list): value can be a string,
              int or a list contains defined Keys.
        """
        self._execute(Command.SEND_KEYS_TO_ACTIVE_ELEMENT, {
            'value': value_to_key_strokes(value)
        })

    @fluent
    def switch_to_frame(self, frame_reference=None):
        """Switches focus to the specified frame, by index, name, or webelement.

        Args:
            frame_reference(None|int|WebElement):
                The identifier of the frame to switch to.
                None means to set to the default context.
                An integer representing the index.
                A webelement means that is an (i)frame to switch to.
                Otherwise throw an error.

        Returns:
            WebDriver Object.
        """
        if frame_reference is not None and type(frame_reference) not in [int, WebElement]:
            raise TypeError('Type of frame_reference must be None or int or WebElement')
        self._execute(Command.SWITCH_TO_FRAME,
            {'id': frame_reference})

    @fluent
    def switch_to_parent_frame(self):
        """Switches focus to the parent context."""
        self._execute(Command.SWITCH_TO_PARENT_FRAME)


    def get_active_element(self):
        """Returns the active element in current context."""
        return self._execute(Command.GET_ACTIVE_ELEMENT)

    @property
    def source(self):
        """Gets the source of the current page.

        Returns:
            Return the source of the current page.
        """
        return self._execute(Command.GET_PAGE_SOURCE)


    def execute_script(self, script, *args):
        """Execute JavaScript Synchronously in current context.

        Args:
            script: The JavaScript to execute.
            *args: Arguments for your JavaScript.

        Returns:
            Returns the return value of the function.
        """
        return self._execute(Command.EXECUTE_SCRIPT, {
            'script': script,
            'args': list(args)})

    @fluent
    def execute_async_script(self, script, *args):
        """Execute JavaScript Asynchronously in current context.

        Args:
            script: The JavaScript to execute.
            *args: Arguments for your JavaScript.

        Returns:
            Returns the return value of the function.
        """
        return self._execute(Command.EXECUTE_ASYNC_SCRIPT, {
            'script': script,
            'args': list(args)})

    @property
    def cookies(self):
        """Returns  all cookies associated with the address of the current context.
        """
        return self._execute(Command.GET_ALL_COOKIES)

    def get_cookie(self, name):
        """Get a single cookie by name.

        Returns:
            Returns the cookie if found, None if not.
        """
        for cookie in self.cookies:
            if cookie['name'] == name:
                return cookie
        return None

    @fluent
    def delete_cookie(self, name):
        """Delete a single cookie by name.

        Args:
            name: The cookie name.
        """
        self._execute(Command.DELETE_COOKIE, {'name': name})

    @fluent
    def delete_all_cookies(self):
        """Delete all cookies at once."""
        self._execute(Command.DELETE_ALL_COOKIES)

    @fluent
    def add_cookie(self, cookie_dict):
        """Set a cookie.

        Args:
            cookie_dict: A dictionary object.
                keys:
                    "name",
                    "value",
                    ["path"],
                    ["domain"],
                    ["secure"],
                    ['httpOnly'],
                    ["expiry]"

        Returns:
            WebElement Object.
        """
        if not isinstance(cookie_dict, dict):
            raise TypeError('Type of the cookie must be a dict.')
        if not cookie_dict.get(
            'name', None
        ) or not cookie_dict.get(
            'value', None):
            raise KeyError('Missing required keys, \'name\' and \'value\' must be provided.')
        self._execute(Command.ADD_COOKIE, {'cookie': cookie_dict})

    @fluent
    def set_implicitly_wait(self, time_to_wait):
        """Implicit wait timeout that specifies a time to
           wait for the implicit element location strategy
           hen locating elements using Find Element and Find Elements.

        Args:
            time_to_wait(int): Amount of time to wait (in seconds)

        Returns:
            WebElement Object.
        """
        self._execute(Command.IMPLICIT_WAIT, {
            'ms': float(time_to_wait) * 1000})

    @fluent
    def set_script_timeout(self, time_to_wait):
        """Script timeout that specifies a time to wait for scripts to run.

        Args:
            time_to_wait(int): Amount of time to wait (in seconds)

        Returns:
            WebElement Object.
        """
        self._execute(Command.SET_SCRIPT_TIMEOUT, {
            'ms': float(time_to_wait) * 1000})

    @fluent
    def set_page_load_timeout(self, time_to_wait):
        """Page load timeout that specifies a time to
           wait for the page loading to complete.

        Args:
            time_to_wait(int): Amount of time to wait

        Returns:
            WebElement Object.
        """
        self._execute(Command.SET_TIMEOUTS, {
            'ms': float(time_to_wait) * 1000,
            'type': 'page load'})

    @fluent
    def accept_alert(self):
        """Accepts the alert available."""
        self._execute(Command.ACCEPT_ALERT)

    @fluent
    def dismiss_alert(self):
        """Dismisses the alert available."""
        self._execute(Command.DISMISS_ALERT)

    @property
    def alert_text(self):
        """Gets the text of the Alert."""
        return self._execute(Command.GET_ALERT_TEXT)

    @fluent
    def alert_keys(self, keys):
        """Sends keystrokes to a JavaScript prompt() dialog.

        Args:
            keys(str): The keys send to.
        """
        self._execute(Command.SET_ALERT_VALUE, {
            'text': keys
        })

    def take_screenshot(self):
        """Gets the screenshot of the current window
           as a base64 encoded string.

        Returns:
            Base64 encoded string of the screenshot.
        """
        return self._execute(Command.SCREENSHOT)

    @fluent
    def save_screenshot(self, filename, quietly = False):
        """Save the screenshot to local.

        Args:
            filename(str): The path to save the image.
            quietly(bool): If True, omit the IOError when
                failed to save the image.

        Returns:
            WebElement Object.

        Raises:
            WebDriverException.
            IOError.
        """
        imgData = self.take_screenshot()
        try:
            with open(filename, "wb") as f:
                f.write(decodebytes(imgData.encode('ascii')))
        except IOError as err:
            if not quietly:
                raise err

    def element(self, using, value):
        """Find an element in the current context.

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.

        Returns:
            WebElement Object.

        Raises:
            WebDriverException.
        """
        return self._execute(Command.FIND_ELEMENT, {
            'using': using,
            'value': value
        })

    def element_if_exists(self, using, value):
        """Check if an element in the current context.

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.

        Returns:
            Return True if the element does exists and return False otherwise.

        Raises:
            WebDriverException.
        """
        try:
            self._execute(Command.FIND_ELEMENT, {
                'using': using,
                'value': value
            })
            return True
        except:
            return False

    def element_or_none(self, using, value):
        """Check if an element in the current context.

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.

        Returns:
            Return Element if the element does exists and return None otherwise.

        Raises:
            WebDriverException.
        """
        try:
            return self._execute(Command.FIND_ELEMENT, {
                'using': using,
                'value': value
            })
        except:
            return None

    def elements(self, using, value):
        """Find elements in the current context.

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.

        Returns:
            Return a List<Element | None>, if no element matched, the list is empty.

        Raises:
            WebDriverException.
        """
        return self._execute(Command.FIND_ELEMENTS, {
            'using': using,
            'value': value
        })

    def wait_for(
        self, timeout=10000, interval=1000,
        *, asserter=lambda x: x):
        """Wait for driver till satisfy the given condition

        Args:
            timeout(int): How long we should be retrying stuff.
            interval(int): How long between retries.
            asserter(callable): The asserter func to determine the result.

        Returns:
            Return the driver.

        Raises:
            WebDriverException.
        """
        if not hasattr(asserter, '__call__'):
            raise TypeError('Asserter must be callable.')
        @retry(
            retry_on_exception=lambda ex: isinstance(ex, WebDriverException),
            stop_max_delay=timeout,
            wait_fixed=interval
        )
        def _wait_for(driver):
            asserter(driver)
            return driver

        return _wait_for(self)

    def wait_for_element(
        self, using, value, timeout=10000,
        interval=1000, *, asserter=is_displayed):
        """Wait for element till satisfy the given condition

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.
            timeout(int): How long we should be retrying stuff.
            interval(int): How long between retries.
            asserter(callable): The asserter func to determine the result.

        Returns:
            Return the Element.

        Raises:
            WebDriverException.
        """
        if not hasattr(asserter, '__call__'):
            raise TypeError('Asserter must be callable.')
        @retry(
            retry_on_exception=lambda ex: isinstance(ex, WebDriverException),
            stop_max_delay=timeout,
            wait_fixed=interval
        )
        def _wait_for_element(ctx, using, value):
            el = ctx.element(using, value)
            asserter(el)
            return el

        return _wait_for_element(self, using, value)

    def wait_for_elements(
        self, using, value, timeout=10000,
        interval=1000, *, asserter=is_displayed):
        """Wait for elements till satisfy the given condition

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.
            timeout(int): How long we should be retrying stuff.
            interval(int): How long between retries.
            asserter(callable): The asserter func to determine the result.

        Returns:
            Return the list of Element if any of them satisfy the condition.

        Raises:
            WebDriverException.
        """
        if not hasattr(asserter, '__call__'):
            raise TypeError('Asserter must be callable.')
        @retry(
            retry_on_exception=lambda ex: isinstance(ex, WebDriverException),
            stop_max_delay=timeout,
            wait_fixed=interval
        )
        def _wait_for_elements(ctx, using, value):
            els = ctx.elements(using, value)
            if not len(els):
                raise WebDriverException('no such element')
            else:
                el = els[0]
                asserter(el)
                return els

        return _wait_for_elements(self, using, value)


add_element_extension_method(WebDriver)
