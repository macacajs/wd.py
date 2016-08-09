#
# Testcase for WebDriverException
#


import pytest

from macaca.webdriverexception import WebDriverError, find_exception_by_code, WebDriverException


def test_find_exception():
    error = find_exception_by_code(7)
    assert error == WebDriverError.NO_SUCH_ELEMENT


def test_find_exception_does_not_exists():
    error = find_exception_by_code(100)
    assert error == None

def test_init_exception():
    wd_ex = WebDriverException(
        'no such element', 'Element is not found', 'xxxxxx', ['a', 'b']
    )
    assert wd_ex.error == 'no such element'
    assert wd_ex.message == 'Element is not found'
    assert wd_ex.screen == 'xxxxxx'
    assert wd_ex.stacktrace == ['a', 'b']
    assert str(wd_ex) == (
        '\nError: no such element\n'
        'Message: Element is not found\n'
        'Screenshot: available via screen\n'
        'Stacktrace:\na\nb')
