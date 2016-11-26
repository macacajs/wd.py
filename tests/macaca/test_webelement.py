#
# Testcase for WebElement Object
#

import json

import pytest
import responses

from macaca.asserters import is_not_displayed
from macaca.webdriver import WebDriver
from macaca.webelement import WebElement
from macaca.webdriverexception import WebDriverException
from macaca.util import exec_


@pytest.fixture(scope="module")
def driver():
    wd = WebDriver({
        'browserName': 'chrome',
        'platformName': 'Android'
    })
    wd.attach('2345')
    return wd


@pytest.fixture(scope="module")
def element(driver):
    return WebElement('1', driver)


def test_driver(element, driver):
    assert element.driver == driver


def test_equal_element(element):
    assert element == WebElement('1', driver)


def test_not_equal_element(element):
    assert element != WebElement('2', driver)


def test_hash_element(element):
    map = {}
    map[element] = 'test'
    assert map.get(WebElement('1', driver), None) == 'test'


@responses.activate
def test_find_element(driver, element):
    import json
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/element',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': {
                'ELEMENT': '2'
            }
        })
    el = element.element('id', 'login')
    assert isinstance(el, WebElement)
    assert el.element_id == '2'
    assert el._driver == driver
    body = responses.calls[0].request.body.decode('utf-8')
    assert json.loads(body) == {
        "using": "id",
        "value": "login"
    }


@responses.activate
def test_element_if_exists(element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/element',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': {
                'ELEMENT': '2'
            }
        })
    ret = element.element_if_exists('id', 'login')
    assert ret


@responses.activate
def test_element_not_exists(element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/element',
        json={
            'status': 7,
            'sessionId': '2345',
            'value': 'no such element'
        })
    ret = element.element_if_exists('id', 'login')
    assert not ret


@responses.activate
def test_element_or_none(element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/element',
        json={
            'status': 7,
            'sessionId': '2345',
            'value': 'no such element'
        })
    ret = element.element_or_none('id', 'login')
    assert not ret


@responses.activate
def test_find_elements(element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/elements',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': [{
                'ELEMENT': '1'
            }, {
                'ELEMENT': '2'
            }]
        })
    els = element.elements('id', 'login')
    assert isinstance(els, list)
    for el in els:
        assert isinstance(el, WebElement)


def test_wait_for(element):
    from datetime import datetime
    assert element == element.wait_for()

    with pytest.raises(TypeError):
        element.wait_for(asserter='')

    before_time = datetime.now()

    with pytest.raises(WebDriverException):
        element.wait_for(2000, 500, asserter=lambda d: exec_("raise WebDriverException('test')"))

    after_time = datetime.now()
    during = after_time - before_time
    assert during.seconds == 2


@responses.activate
def test_wait_for_element(element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/element',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': {
                'ELEMENT': '2'
            }
        })

    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/2/displayed',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': True
        })

    from datetime import datetime
    element.wait_for_element('id', 'login')

    with pytest.raises(TypeError):
        element.wait_for_element('id', 'login', asserter='')

    before_time = datetime.now()

    with pytest.raises(WebDriverException) as excinfo:
        element.wait_for_element(
            'id', 'login', 2000, 500,
            asserter=is_not_displayed)
    assert excinfo.value.error == 'element is visible'

    after_time = datetime.now()
    during = after_time - before_time
    assert during.seconds == 2


@responses.activate
def test_wait_for_elements(element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/elements',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': [{
                'ELEMENT': '2'
            }, {
                'ELEMENT': '3'
            }]
        })

    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/2/displayed',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': True
        })

    from datetime import datetime
    els = element.wait_for_elements('id', 'login')

    with pytest.raises(TypeError):
        element.wait_for_elements('id', 'login', asserter='')

    before_time = datetime.now()

    with pytest.raises(WebDriverException) as excinfo:
        element.wait_for_elements(
            'id', 'login', 2000, 500,
            asserter=is_not_displayed)
    assert excinfo.value.error == 'element is visible'

    after_time = datetime.now()
    during = after_time - before_time
    assert during.seconds == 2


@responses.activate
def test_is_displayed(element):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/displayed',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': True
        })

    assert element.is_displayed() == True


@responses.activate
def test_is_selected(element):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/selected',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': False
        })

    assert element.is_selected() == False


@responses.activate
def test_is_enabled(element):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/enabled',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': False
        })

    assert element.is_enabled() == False


@responses.activate
def test_get_property(element):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/property/value',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': '123456'
        })

    assert element.get_property('value') == '123456'


@responses.activate
def test_get_computed_css(element):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/css/height',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': '200px'
        })

    assert element.get_computed_css('height') == '200px'


@responses.activate
def test_text(element):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/text',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': 'Hello, Macaca!'
        })

    assert element.text == 'Hello, Macaca!'


@responses.activate
def test_tag_name(element):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/name',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': 'input'
        })

    assert element.tag_name == 'input'


@responses.activate
def test_dimensions_and_coordinates(element):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/location',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': {
                'x': 200,
                'y': 100
            }
        })

    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/size',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': {
                'width': 400,
                'height': 400
            }
        })

    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/rect',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': {
                'x': 200,
                'y': 100,
                'width': 400,
                'height': 400
            }
        })

    assert element.location == {
        'x': 200,
        'y': 100
    }
    assert element.size == {
        'width': 400,
        'height': 400
    }
    assert element.rect == {
        'x': 200,
        'y': 100,
        'width': 400,
        'height': 400
    }


@responses.activate
def test_click(element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/click',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert element.click() == element


@responses.activate
def test_clear(element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/clear',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert element.clear() == element


@responses.activate
def test_send_keys(element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/value',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert element.send_keys('123') == element
    body = responses.calls[0].request.body.decode('utf-8')
    data = json.loads(body)
    assert data['value'] == ['1', '2', '3']


@responses.activate
def test_move_to(element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/moveto',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert element.move_to(100, 200) == element
    body = responses.calls[0].request.body.decode('utf-8')
    assert json.loads(body) == {
        'element': '1',
        'x': 100,
        'y': 200
    }


@responses.activate
def test_flick(element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/touch/flick',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert element.flick(100, 200, 100) == element
    body = responses.calls[0].request.body.decode('utf-8')
    assert json.loads(body) == {
        'element': '1',
        'x': 100,
        'y': 200,
        'speed': 100
    }


@responses.activate
def test_tap(element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/touch/click',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert element.tap() == element


@responses.activate
def test_swipe(driver, element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/swipe',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert element.swipe(0, 0, 200, 200) == element
    assert element.swipe(100, 100, 200, 200, 2000) == element
    body = responses.calls[1].request.body.decode('utf-8')
    data = json.loads(body)
    assert data == {
        'startX': 100,
        'startY': 100,
        'endX': 200,
        'endY': 200,
        'duration': 2000
    }


@responses.activate
def test_screenshot(element):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/screenshot',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': 'R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs='
        })
    assert element.take_screenshot() == 'R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs='
    assert element.save_screenshot('./test.png') == element
    from os import remove

    try:
        remove('./test.png')
    except:
        pass

    with pytest.raises(IOError):
        element.save_screenshot('/etc/test.png')

    element.save_screenshot('/etc/test.png', True)
