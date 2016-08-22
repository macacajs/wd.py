#
# Default Asserts for element
#


from .webdriverexception import WebDriverException


def is_displayed(target):
    """Assert whether the target is displayed

    Args:
        target(WebElement): WebElement Object.

    Returns:
        Return True if the element is displayed or return False otherwise.
    """
    is_displayed = getattr(target, 'is_displayed', None)
    if not is_displayed or not callable(is_displayed):
        raise TypeError('Target has no attribute \'is_displayed\' or not callable')
    if not is_displayed():
        raise WebDriverException('element not visible')


def is_not_displayed(target):
    """Assert whether the target is not displayed

    Args:
        target(WebElement): WebElement Object.

    Returns:
        Return True if the element is not displayed or return False otherwise.
    """
    is_displayed = getattr(target, 'is_displayed', None)
    if not is_displayed or not callable(is_displayed):
        raise TypeError('Target has no attribute \'is_displayed\' or not callable')
    if is_displayed():
        raise WebDriverException('element is visible')
