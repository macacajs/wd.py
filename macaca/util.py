#
# Util for WebDriver
#

from string import Formatter
from functools import wraps

from .locator import Locator
from .keys import Keys


class MemorizeFormatter(Formatter):
    """Customize the Formatter to record used and unused kwargs."""

    def __init__(self):
        """Initialize the MemorizeFormatter."""
        Formatter.__init__(self)
        self._used_kwargs = {}
        self._unused_kwargs = {}

    def check_unused_args(self, used_args, args, kwargs):
        """Implement the check_unused_args in superclass."""
        for k, v in kwargs.items():
            if k in used_args:
                self._used_kwargs.update({k: v})
            else:
                self._unused_kwargs.update({k: v})

    def vformat(self, format_string, args, kwargs):
        """Clear used and unused dicts before each formatting."""
        self._used_kwargs = {}
        self._unused_kwargs = {}
        return super().vformat(format_string, args, kwargs)

    def format_map(self, format_string, mapping):
        """format a string by a map

        Args:
            format_string(str): A format string
            mapping(dict): A map to format the string

        Returns:
            A formatted string.

        Raises:
            KeyError: if key is not provided by the given map.
        """
        return self.vformat(format_string, args=None, kwargs=mapping)

    def get_used_kwargs(self):
        """Get used kwargs after formatting."""
        return self._used_kwargs

    def get_unused_kwargs(self):
        """Get unused kwargs after formatting."""
        return self._unused_kwargs


def add_element_extension_method(Klass):
    """Add element_by alias and extension' methods(if_exists/or_none)."""
    def add_element_method(Klass, using):
        locator = using.name.lower()
        find_element_name = "element_by_" + locator
        find_element_if_exists_name = "element_by_" + locator + "_if_exists"
        find_element_or_none_name = "element_by_" + locator + "_or_none"
        wait_for_element_name = "wait_for_element_by_" + locator

        find_elements_name = "elements_by_" + locator
        wait_for_elements_name = "wait_for_elements_by_" + locator

        def find_element(self, value):
            return self.element(using.value, value)

        find_element.__name__ = find_element_name
        find_element.__doc__ = (
            "Set parameter 'using' to '{0}'.\n".format(using.value) +
            str(Klass.__dict__['element'].__doc__)
        )

        def find_element_if_exists(self, value):
            return self.element_if_exists(using.value, value)

        find_element_if_exists.__name__ = find_element_if_exists_name
        find_element_if_exists.__doc__ = (
            "Set parameter 'using' to '{0}'.\n".format(using.value) +
            str(Klass.__dict__['element_if_exists'].__doc__)
        )

        def find_element_or_none(self, value):
            return self.element_or_none(using.value, value)

        find_element_or_none.__name__ = find_element_or_none_name
        find_element_or_none.__doc__ = (
            "Set parameter 'using' to '{0}'.\n".format(using.value) +
            str(Klass.__dict__['element_or_none'].__doc__)
        )

        def wait_for_element_by(self, *args, **kwargs):
            return self.wait_for_element(using.value, *args, **kwargs)

        wait_for_element_by.__name__ = wait_for_element_name
        wait_for_element_by.__doc__ = (
            "Set parameter 'using' to '{0}'.\n".format(using.value) +
            str(Klass.__dict__['wait_for_element'].__doc__)
        )

        def find_elements(self, value):
            return self.elements(using.value, value)

        find_elements.__name__ = find_elements_name
        find_elements.__doc__ = (
            "Set parameter 'using' to '{0}'.\n".format(using.value) +
            str(Klass.__dict__['elements'].__doc__)
        )

        def wait_for_elements_available(self, *args, **kwargs):
            return self.wait_for_elements(using.value, *args, **kwargs)

        wait_for_elements_available.__name__ = wait_for_elements_name
        wait_for_elements_available.__doc__ = (
            "Set parameter 'using' to '{0}'.\n".format(using.value) +
            str(Klass.__dict__['wait_for_elements'].__doc__)
        )

        setattr(Klass, find_element_name, find_element)
        setattr(Klass, find_element_if_exists_name, find_element_if_exists)
        setattr(Klass, find_element_or_none_name, find_element_or_none)
        setattr(Klass, wait_for_element_name, wait_for_element_by)
        setattr(Klass, find_elements_name, find_elements)
        setattr(Klass, wait_for_elements_name, wait_for_elements_available)

    for locator in iter(Locator):
        add_element_method(Klass, locator)


def fluent(func):
    """Fluent interface decorator to return self if method return None."""
    @wraps(func)
    def fluent_interface(instance, *args, **kwargs):
        ret = func(instance, *args, **kwargs)
        if ret is not None:
            return ret
        return instance
    return fluent_interface


def value_to_key_strokes(value):
    """Convert value to a list of key strokes
    >>> value_to_key_strokes(123)
    ['1', '2', '3']
    >>> value_to_key_strokes('123')
    ['1', '2', '3']
    >>> value_to_key_strokes([1, 2, 3])
    ['1', '2', '3']
    >>> value_to_key_strokes(['1', '2', '3'])
    ['1', '2', '3']

    Args:
        value(int|str|list)

    Returns:
        A list of string.
    """
    result = []
    if isinstance(value, int):
        value = str(value)

    for v in value:
        if isinstance(v, Keys):
            result.append(v.value)
        elif isinstance(v, int):
            result.append(str(v))
        else:
            result.append(v)
    return result
