#
# Testcase for Util
#


import pytest

from macaca.util import (
    add_element_extension_method,
    fluent,
    value_to_key_strokes,
    MemorizeFormatter
)
from macaca.locator import Locator
from macaca.keys import Keys


@pytest.fixture(scope="module")
def formatter():
    return MemorizeFormatter()


@pytest.fixture(scope="module")
def before_format_url():
    return '/session/{session_id}/element/{element_id}/value'


def test_format_url(formatter, before_format_url):
    data = {
        'session_id': 123,
        'element_id': 456
    }

    after_format_url = formatter.format_map(before_format_url, data)
    assert after_format_url == '/session/123/element/456/value'


def test_missing_data_url(formatter, before_format_url):
    data = {
        'session_id': 123
    }
    with pytest.raises(KeyError) as excinfo:
        formatter.format_map(before_format_url, data)
    assert excinfo.value.args[0]  == 'element_id'


def test_data_after_use(formatter, before_format_url):
    data = {
        'session_id': 123,
        'element_id': 456,
        'not use': 789
    }
    after_format_url = formatter.format_map(before_format_url, data)
    assert after_format_url == '/session/123/element/456/value'
    used_kwargs = formatter.get_used_kwargs()
    unused_kwargs = formatter.get_unused_kwargs()
    assert used_kwargs == {
        'session_id': 123,
        'element_id': 456
    }
    assert unused_kwargs == {
        'not use': 789
    }


class FakeWebElement:
    def element(self, using=Locator.ID.value, value=None):
        return (using, value)

    def element_if_exists(self, using=Locator.ID.value, value=None):
        return (using, value)

    def element_or_none(self, using=Locator.ID.value, value=None):
        return (using, value)

    def elements(self, using=Locator.ID.value, value=None):
        return (using, value)

    def wait_for_element(self, using=Locator.ID.value, value=None):
        return (using, value)

    def wait_for_elements(self, using=Locator.ID.value, value=None):
        return (using, value)


def test_add_element_extension_method():
    add_element_extension_method(FakeWebElement)
    wb_el = FakeWebElement()

    for locator in iter(Locator):
        locator_name = locator.name.lower()
        locator_value = locator.value
        find_element_name = "element_by_" + locator_name
        find_element_if_exists_name = "element_by_" + locator_name + \
            "_if_exists"
        find_element_or_none_name = "element_by_" + locator_name + "_or_none"
        wait_for_element_name = "wait_for_element_by_" + locator_name
        find_elements_name = "elements_by_" + locator_name
        wait_for_elements_name = "wait_for_elements_by_" + locator_name
        assert getattr(wb_el, find_element_name)('test') == \
            wb_el.element(locator_value, 'test')
        assert getattr(wb_el, find_element_if_exists_name)('test') == \
            wb_el.element_if_exists(locator_value, 'test')
        assert getattr(wb_el, find_element_or_none_name)('test') == \
            wb_el.element_or_none(locator_value, 'test')
        assert getattr(wb_el, wait_for_element_name)('test') == \
            wb_el.wait_for_element(locator_value, 'test')
        assert getattr(wb_el, find_elements_name)('test') == \
            wb_el.elements(locator_value, 'test')
        assert getattr(wb_el, wait_for_elements_name)('test') == \
            wb_el.wait_for_elements(locator_value, 'test')


class FakeDriver:
    @fluent
    def returnSomething(self):
        return "ok"

    @fluent
    def returnNone(self):
        pass


@pytest.fixture(scope="module")
def driver():
    return FakeDriver()


def test_fluent_decorator(driver):
    assert driver.returnSomething() == 'ok'
    assert driver.returnNone() == driver


def test_value_to_key_strokes():
    assert value_to_key_strokes(123) == ['123']
    assert value_to_key_strokes('123') == ['123']
    assert value_to_key_strokes([1, 2, 3]) == ['123']
    assert value_to_key_strokes(['123']) == ['123']
