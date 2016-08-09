#
# https://w3c.github.io/webdriver/webdriver-spec.html#locator-strategies
# Locator according to WebDriver Protocol
#

from enum import Enum


class Locator(Enum):
    """Locator Enum defined by WebDriver Protocol."""
    ID = "id"
    XPATH = "xpath"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    NAME = "name"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector"
