Macaca Python Client
=====================

.. image:: https://img.shields.io/coveralls/macacajs/wd.py/master.svg
    :target: https://coveralls.io/github/macacajs/wd.py

.. image:: https://img.shields.io/travis/macacajs/wd.py/master.svg
    :target: https://travis-ci.org/macacajs/wd.py

.. image:: https://img.shields.io/pypi/v/wd.svg
    :target: https://pypi.python.org/pypi/wd

.. image:: https://img.shields.io/pypi/pyversions/wd.svg
    :target: https://pypi.python.org/pypi/wd/

.. image:: https://img.shields.io/pypi/dd/wd.svg
    :target: https://pypi.python.org/pypi/wd/

Intro
------
WD.py is a Python WebDriver client implemented most of the APIs in the `WebDriver Protocol <https://www.w3.org/TR/webdriver/>`_.
It was originally designed for `Macaca <http://macacajs.github.io/macaca/>`_ (A Node.js powered WebDriver server), but also available for any other implementation of WebDriver server
such as Selenium, Appium and etc.

Homepage
---------
`WD.py’s documentation. <https://macacajs.github.io/wd.py/>`_

Examples
---------
.. code-block:: python

    >>> from macaca import WebDriver, WebElement

    # Configure the desired capabilities.
    >>> desired_caps = {
        'autoAcceptAlerts': True,
        'browserName': 'Chrome',
        'platformName': 'desktop'
    }

    >>> driver = WebDriver(desired_caps)

    # Start the WebDriver session
    >>> driver.init()

    # Support fluent API
    >>> driver.set_window_size(1280, 800).get("https://www.google.com")

    # Get WebElement instance through element_by_* APIs.
    >>> web_element = driver.element_by_id("lst-ib")
    >>> print(type(web_element))
    macaca.webelement.WebElement

    # WebElement include methods such as send_keys, click, get_attribute and etc.
    >>> web_element.send_keys("macaca")
    >>> web_element = driver.element_by_name("btnK")
    >>> web_element.click()

    # WebDriver also has some properties like source, title and current_url.
    >>> html = driver.source
    >>> print('Does Macaca exist: ', 'macaca' in html)
    True
    >>> title = driver.title
    >>> print(title)
    macaca - Google Search

Changelog
----------
Details changes for each release are documented in the `HISTORY.rst <HISTORY.rst>`_.

License
--------
`MIT <http://opensource.org/licenses/MIT>`_
