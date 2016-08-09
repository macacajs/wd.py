#
# Testcase for Asserters
#


import pytest

from macaca.asserters import is_displayed, is_not_displayed
from macaca.webelement import WebElement
from macaca.webdriverexception import WebDriverException


class DisplayedWebElement:
    def is_displayed(self):
        return True


class NotDisplayedWebElement:
    def is_displayed(self):
        return False


@pytest.fixture(scope="module")
def displayed_element():
    return DisplayedWebElement()


@pytest.fixture(scope="module")
def not_displayed_element():
    return NotDisplayedWebElement()


@pytest.fixture(scope="module")
def wrong_element():
    return []


def test_is_displayed(displayed_element, not_displayed_element):
    is_displayed(displayed_element)
    with pytest.raises(WebDriverException):
        is_displayed(not_displayed_element)


def test_is_not_displayed(displayed_element, not_displayed_element):
    is_not_displayed(not_displayed_element)
    with pytest.raises(WebDriverException):
        is_not_displayed(displayed_element)


def test_wrong_element(wrong_element):
    with pytest.raises(TypeError):
        is_displayed(wrong_element)
    with pytest.raises(TypeError):
        is_not_displayed(wrong_element)
