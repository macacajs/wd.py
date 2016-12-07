Quick Start
==============

What is WD.py?
---------------

WD.py is a Python WebDriver client implemented most of the APIs in the `WebDriver Protocol <https://www.w3.org/TR/webdriver/>`_.
It was originally designed for `Macaca <http://macacajs.github.io>`_ (A Node.js powered WebDriver server), but also available for any other implementation of WebDriver server
such as Selenium, Appium and etc.

Installation
-------------

To install WD.py, simply:

.. code-block:: python

    pip install wd

To get latest code from source via `GitHub <https://github.com/macacajs/wd.py>`_.

.. code-block:: shell

    git clone https://github.com/macacajs/wd.py.git


Prerequisite
-------------

WD.py does not start the WebDriver server automaticalliy, you may use `Macaca <http://macacajs.github.io>`_ to start a WebDriver server and run the tests after.

Usage
------

**Configure the WebDriver**

Firstly, you need to configure the WebDriver with desired capabilities and server url.

.. code-block:: python

    from macaca import WebDriver

    desired_caps = {
        'browserName': 'Chrome', # Electon, Safari(iOS).
        'platformName': 'desktop', # iOS, Android.
        'platformVersion': '*',
        'autoAcceptAlerts': True # Accept the Alerts in page automaticalliy.
    }

    server_url = 'http://127.0.0.1:3456/wd/hub/'

    # You can omit the server_url if you use the default url above.
    driver = WebDriver(desired_caps, server_url)

    # You can also use a dict to represent the url.
    driver = WebDriver(desired_caps, {
        'protocol': 'https',
        'hostname': '127.0.0.1',
        'port': 5678,
        'username': 'macaca',
        'password': '123456',
        'path': '/hub'
    })

    # Defaults
    {
        'protocol': 'http',
        'hostname': '127.0.0.1',
        'port': 3456,
        'path': '/wd/hub'
    }

    # Which equals to
    driver = WebDriver(desired_caps, 'https://macaca:123456@127.0.0.1:5678/hub')

**Init the WebDriver**

.. code-block:: python

    # Create a new session towards WebDriver server.
    driver.init()

**Stop the WebDriver**

.. code-block:: python

    # Delete current session.
    driver.quit()

**Attach to an existing session**

.. code-block:: python

    # Attach to a given session.
    driver.attach('012-345-678-9')

**WebDriver methods**

The instance methods of WebDriver mostly related to the global action of driver.
For example, switch to a new url, refresh and get title.

.. code-block:: python

    # Navigate to a url.
    driver.get('https://www.google.com')

    # Refresh current page.
    driver.refresh()

    # Get title of current page
    title = driver.title

**Find element(s)**

The Find Element and Find Elements commands allow look up of individual elements and collections of elements, respectively.
Locator strategies are listed below:

- "id"
- "xpath"
- "link text"
- "partial link text"
- "tag name"
- "class name"
- "css selector"

The basic method of finding element(s) is `element`:

.. code-block:: python

    # Finding the element which its `id` matches `login`
    driver.element('id', 'login')

But in most cases, you don't need to use this basic method, there are a lot of extension methods for convenience.

.. code-block:: python

    # Finding the element which its `id` matches `login`
    driver.element_by_id('login')

    # Similarly, all the strategies can be append after `element` using snake case.
    driver.element_by_id('login')

    driver.element_by_xpath('//*[@id="finding-elements-to-interact"]/table[4]')

    driver.element_by_link_text('macaca')

    driver.element_by_partial_link_text('maca')

    driver.element_by_tag_name('input')

    driver.element_by_class_name('btn')

    driver.element_by_css_selector('.btn')

    # And we have element_if_exists and element_or_none to avoid
    # raise WebDriverException of ` no such element` when element not found.

    # Return True if the element does exists and return False otherwise.
    driver.element_by_id_if_exists('login')

    # Return Element if the element does exists and return None otherwise.
    driver.element_by_id_or_none('login')

    # More over, there are `wait for` method to wait for element
    # till satisfy the given condition

    # Default to wait 10s, each interval 1s.
    # The asserter function defaults to asserters.is_displayed.

    # See more at API section.
    driver.wait_for_element_by_id('login')

**WebElement methods**

The instance methods of WebElement mostly related to the action element such as
click the element, get the tag name or get the innerText of the element.

The WebElement instance is returned by finding element command.

.. code-block:: python

    from macaca import WebElement

    # Retrieve the element by id
    web_element = driver.element_by_id('login')
    print(type(web_element) == WebElement) # True

    # Click the element
    web_element.click()

    # Get the tag name of the element
    tag_name = web_element.tag_name

    # Get the innerText of the element
    text = web_element.text

Futhermore, all the `element` methods on WebDriver can be used on WebElement, it means to
find element from the current Web Element.

.. code-block:: python

    web_element.element_by_id('ss')

**Keys**

We can send a sequence of key strokes to an element when need to fulfill a input field.

.. code-block:: python

    web_element.send_keys('123456')

    # or
    driver.send_keys(web_element, '123456')

    # `send_keys` also accept an array, it's very useful when sending special keys.
    driver.send_keys(web_element, [1, 2, 3, 4, 5, 6])

*Special keys* means the pressable keys that aren't text, learn more at `Character Types`_.

.. _`Character Types`: https://w3c.github.io/webdriver/webdriver-spec.html#dfn-character-types

For easily use, the *keys* defined in above protocol can import from `Keys` module directly.

.. code-block:: python

    >>> from macaca import keys

    >>> print(keys.ENTER)
    \uE007

    >>> print(keys.DELETE)
    \uE017

It is convenient to send special keys using array.

.. code-block:: python

    from macaca.keys import ENTER, DELETE

    web_element.send_keys([1, DELETE, 1, 2, 3, 4, 5, 6])


**Screenshot**

There are two methods to use when taking screenshot.

.. code-block:: python

    # Return the base64 encoded string of the screenshot.
    base64_str = driver.take_screenshot()

    # Save screenshot to the given path.
    driver.save_screenshot('./screen.png')

    # `save_screenshot` has the optional second parameter
    # to decide whether to ignore the IOError when failed to
    # save to file system for some reason.
    # For example, no permission to write.

    >>> driver.save_screenshot('/etc/screen.png')
    IOError: [Errno 13] Permission denied: '/etc/screen.png'

    # Nothing happened.
    >>> driver.save_screenshot('/etc/screen.png', True)

**Switch context**

For mobile testing, we will need to switch context between *Native* and *Webview*.

.. code-block:: python

    # Get existing contexts
    ctxs = driver.contexts

    print(ctxs) # ['NATIVE', 'WEBVIEW_1', 'WEBVIEW_2']

    # Switch to `WEBVIEW_1`
    driver.context = 'WEBVIEW_1'

    print(driver.context) # WEBVIEW_1

**Execute JavaScript Snippets**

In some complex situation, we may need to inject a snippet of JavaScript into the page
and get whatever we want.

.. code-block:: python

    # You can use `arguments` in the script to represent the
    # indexed parameter after the `script`.

    script = 'return document.querySelector(".btn").tagName === arguments[0]'
    args = ['div']

    result = driver.execute_script(script, *args)

    # The script above equals to a IIFE in JavaScript.
    # function () {
    #   return document.querySelector(".btn").tagName === "div"
    # }()

**Fluent Interface**

All the APIs in *WebDriver* and *WebElement* support fluent interface,
which means we can chain the method if the method returns None.

.. code-block:: python

    >>> driver.get('https://www.google.com').element_by_id('login').click()

    # For method that returns something, it's not working.
    >>> driver.element_by_id('login').get_attribute('class').click()
    AttributeError: 'str' object has no attribute 'click'

Due to the nature of Python, it is illegal to write method chaining like JavaScript below:

.. code-block:: javascript

    driver
      .get('https://www.google.com')
      .element_by_id('login')
      .click()

For Pythoner, we recommend two coding style for you to choose.

.. code-block:: python

    # Use additional parenthesis
    (
        driver
            .get('https://www.google.com')
            .element_by_id('login')
            .click()
    )

    # Use backslashes
    driver                             \
        .get('https://www.google.com') \
        .element_by_id('login')        \
        .click()

Next Step
---------------
TODO
