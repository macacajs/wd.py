#
# https = //w3c.github.io/webdriver/webdriver-spec.html
# WebDriver Element Implemenation
#

from base64 import b64decode

from retrying import retry

from .asserters import is_displayed
from .command import Command
from .locator import Locator
from .util import add_element_extension_method, value_to_key_strokes, value_to_single_key_strokes, fluent
from .webdriverexception import WebDriverException


class WebElement(object):
    """The WebElement Object to implement most part of WebDriver protocol.

    Attributes:
        element_id(str): A UDID used to uniquely identify an element.
    """

    def __init__(self, element_id, driver):
        """Initialize the WebElement

        Args:
            element_id(str): The UDID returned by remote servers.
            driver(WebDriver): The WebDriver Object.
        """
        self.element_id = str(element_id)
        self._driver = driver

    def __repr__(self):
        return '<{0.__name__} (session="{1}", element="{2}")>'.format(
            type(self), self._driver.session_id, self.element_id)

    def __eq__(self, el):
        return hasattr(el, 'element_id') and self.element_id == el.element_id

    def __ne__(self, el):
        return not self.__eq__(el)

    def __hash__(self):
        return hash(self.element_id)

    def _execute(self, command, data=None, unpack=True):
        """Private method to execute command with data.

        Args:
            command(Command): The defined command.
            data(dict): The uri variable and body.

        Returns:
            The unwrapped value field in the json response.
        """
        if not data:
            data = {}
        data.setdefault('element_id', self.element_id)
        return self._driver._execute(command, data, unpack)

    @property
    def driver(self):
        """Internal reference to the WebDriver instance."""
        return self._driver

    def element(self, using, value):
        """find an element in the current element.

        Support:
            Android iOS Web(WebView)

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.

        Returns:
            WebElement Object.

        Raises:
            WebDriverException.
        """
        return self._execute(Command.FIND_CHILD_ELEMENT, {
            'using': using,
            'value': value
        })

    def element_if_exists(self, using, value):
        """Check if an element in the current element.

        Support:
            Android iOS Web(WebView)

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.

        Returns:
            Return True if the element does exists and return False otherwise.

        Raises:
            WebDriverException.
        """
        try:
            self._execute(Command.FIND_CHILD_ELEMENT, {
                'using': using,
                'value': value
            })
            return True
        except:
            return False

    def element_or_none(self, using, value):
        """Check if an element in the current element.

        Support:
            Android iOS Web(WebView)

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.

        Returns:
            Return Element if the element does exists and return None otherwise.

        Raises:
            WebDriverException.
        """
        try:
            return self._execute(Command.FIND_CHILD_ELEMENT, {
                'using': using,
                'value': value
            })
        except:
            return None

    def elements(self, using, value):
        """find elements in the current element.

        Support:
            Android iOS Web(WebView)

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.

        Returns:
            Return a List<Element | None>, if no element matched, the list is empty.

        Raises:
            WebDriverException.
        """
        return self._execute(Command.FIND_CHILD_ELEMENTS, {
            'using': using,
            'value': value
        })

    def wait_for(
        self, timeout=10000, interval=1000,
        asserter=lambda x: x):
        """Wait for element till given condition

        Support:
            Android iOS Web(WebView)

        Args:
            timeout(int): How long we should be retrying stuff.
            interval(int): How long between retries.
            asserter(callable): The asserter func to determine the result.

        Returns:
            Return the Element.

        Raises:
            WebDriverException.
        """
        if not callable(asserter):
            raise TypeError('Asserter must be callable.')
        @retry(
            retry_on_exception=lambda ex: isinstance(ex, WebDriverException),
            stop_max_delay=timeout,
            wait_fixed=interval
        )
        def _wait_for(el):
            asserter(el)
            return el

        return _wait_for(self)

    def wait_for_element(
        self, using, value, timeout=10000,
        interval=1000, asserter=is_displayed):
        """Wait for element till the given condition

        Support:
            Android iOS Web(WebView)

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
        if not callable(asserter):
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
        interval=1000, asserter=is_displayed):
        """Wait for elements till the given condition

        Support:
            Android iOS Web(WebView)

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
        if not callable(asserter):
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

    def is_displayed(self):
        """Whether the element is visible.

        Support:
            Android Web(WebView)
        """
        return self._execute(Command.IS_ELEMENT_DISPLAYED)

    def is_selected(self):
        """Returns whether the element is selected.

        Support:
            Web(WebView)
        """
        return self._execute(Command.IS_ELEMENT_SELECTED)

    def is_enabled(self):
        """Returns whether the element is enabled.

        Support:
            Web(WebView)
        """
        return self._execute(Command.IS_ELEMENT_ENABLED)

    def get_property(self, name):
        """Return the result of getting a property, Support: Android iOS Web(WebView).

        Support:
            Support: Android iOS Web(WebView)

        Args:
            name(str): Name of the property to retrieve, Android iOS can only get `origin` `size`.

        Returns:
            The property of the element.
        """
        return self._execute(Command.GET_ELEMENT_PROPERTY, {'name': name})

    def get_computed_css(self, property_name):
        """The computed value of the given CSS property
           of the given web element.

        Support:
            Support: Web(WebView)

        Args:
            property_name(str): CSS property.

        Returns:
            The computed value of parameter property name
            from element's style declarations if the current
            browsing context's document type is not "xml",
            else let it be ""
        """
        return self._execute(Command.GET_ELEMENT_VALUE_OF_CSS_PROPERTY, {
            'property_name': property_name})

    @property
    def text(self):
        """Return the text of the element.
           This is equivalent to calling element.innerText.

        Support:
            Android iOS Web(WebView)
        """
        return self._execute(Command.GET_ELEMENT_TEXT)

    @property
    def tag_name(self):
        """Return the tagName of the element.

        Support:
            Web(WebView)
        """
        return self._execute(Command.GET_ELEMENT_TAG_NAME)

    @property
    def location(self):
        """The location of the element in the renderable canvas in pixels.

        Support:
            Web(WebView)

        Returns:
            A dict contains:
            x(float): X axis position of the top-left corner.
            y(float): Y axis position of the top-left corner.
        """
        return self._execute(Command.GET_ELEMENT_LOCATION)

    @property
    def rect(self):
        """The dimensions and coordinates of the given web element in pixels.

        Support:
            Android iOS Web(WebView)

        Returns:
            A dict contains:
            x(float): X axis position of the top-left corner.
            y(float): Y axis position of the top-left corner.
            height(float): Height of the web element's bounding rectangle.
            width(float): Width of the web element's bounding rectangle.
        """
        return self._execute(Command.GET_ELEMENT_RECT)

    @property
    def size(self):
        """The size of the given web element in pixels.

        Support:
            Web(WebView)

        Returns:
            A dict contains:
            height(float): Height of the web element's bounding rectangle.
            width(float): Width of the web element's bounding rectangle.
        """
        return self._execute(Command.GET_ELEMENT_SIZE)

    @fluent
    def click(self):
        """The Element Click command scrolls into view
           the element and then attempts to click the
           centre of the visible area of the first element
           of the DOMRect sequence. In case the element is
           not displayed, an element not visible error is returned.

        Support:
            Android iOS Web(WebView)
        """
        self._execute(Command.CLICK_ELEMENT)

    @fluent
    def clear(self):
        """The Element Clear command scrolls into view
           a submittable element excluding buttons or
           editable element, and then attempts to clear
           its value, checkedness, or text content.

        Support:
            Android iOS Web(WebView)
        """
        self._execute(Command.CLEAR_ELEMENT)

    @fluent
    def keys(self, value):
        """Send a sequence of key strokes to an element.

        Support:
            Android iOS Web(WebView)

        Args:
            value(str|int|list): value can be a string,
              int or a list contains defined Keys.
        """
        self._execute(Command.SEND_KEYS_TO_ELEMENT, {
            'value': value_to_single_key_strokes(value)})

    @fluent
    def send_keys(self, value):
        """Send a sequence of key strokes to an element.

        Support:
            Android iOS Web(WebView)

        Args:
            value(str|int|list): value can be a string,
              int or a list contains defined Keys.
        """
        self._execute(Command.SEND_KEYS_TO_ELEMENT, {
            'value': value_to_key_strokes(value)})

    @fluent
    def move_to(self, x=0, y=0):
        """Deprecated use element.touch('drag', { toX, toY, duration(s) }) instead.
            Move the mouse by an offset of the specificed element.

        Support:
            Android

        Args:
            x(float): X offset to move to, relative to the
                      top-left corner of the element.
            y(float): Y offset to move to, relative to the
                      top-left corner of the element.

        Returns:
            WebElement object.
        """
        self._driver.move_to(self, x, y)

    @fluent
    def flick(self, x, y, speed):
        """Deprecated use touch('drag', { fromX, fromY, toX, toY, duration(s) }) instead.
            Flick on the touch screen using finger motion events.
            This flickcommand starts at a particulat screen location.

        Support:
            iOS

        Args:
            x(float}: The x offset in pixels to flick by.
            y(float): The y offset in pixels to flick by.
            speed(float) The speed in pixels per seconds.

        Returns:
            WebElement object.
        """
        self._driver.flick(self, x, y, speed)

    @fluent
    def tap(self):
        """Deprecated use touch('tap') instead.
            Single tap on the touch enabled device.

        Support:
            Android iOS

        Args:
            element(WebElement): WebElement Object to single tap on.

        Returns:
            WebElement object.
        """
        self._driver.tap(self)

    @fluent
    def swipe(self, startX, startY, endX, endY, duration = 1000):
        """Deprecated use touch('drag', { fromX, fromY, toX, toY, duration(s) }) instead.
            Swipe on the touch screen using finger motion events.

        Support:
            Android iOS

        Args:
            startX(Float): The x-coordinate of start point.
            startY(Float): The y-coordinate of start point.
            endX(Float): The x-coordinate of end point.
            endY(Float): The y-coordinate of end point.
            duration(Float): The duration in ms.

        Returns:
            WebElement object.
        """
        self._execute(Command.SWIPE_ELEMENT, {
            'startX': startX,
            'startY': startY,
            'endX': endX,
            'endY': endY,
            'duration': duration
        })

    def take_screenshot(self):
        """Gets the screenshot of the current element
           as a base64 encoded string.

        Support:
            Android iOS Web(WebView)

        Returns:
            Base64 encoded string of the screenshot.
        """
        return self._execute(Command.ELEMENT_SCREENSHOT)

    @fluent
    def save_screenshot(self, filename, quietly = False):
        """Save the screenshot to local.

        Support:
            Android iOS Web(WebView)

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
                f.write(b64decode(imgData.encode('ascii')))
        except IOError as err:
            if not quietly:
                raise err

    @fluent
    def touch(self, name, args=None):
        """Apply touch actions on devices. Such as, tap/doubleTap/press/pinch/rotate/drag.
            See more on https://github.com/alibaba/macaca/issues/366.

        Support:
            Android iOS

        Args:
            name(str): Name of the action
            args(dict): Arguments of the action

        Returns:
            WebDriver Object.

        Raises:
            WebDriverException.
        """
        if isinstance(name, list) and not isinstance(name, str):
            for obj in name:
                obj['element'] = self.element_id
            actions = name
        elif isinstance(name, str):
            if not args:
                args = {}
            args['type'] = name
            args['element'] = self.element_id
            actions = [args]
        else:
            raise TypeError('Invalid parameters.')
        self._driver._execute(Command.PERFORM_ACTIONS, {
            'actions': actions
        })


add_element_extension_method(WebElement)
