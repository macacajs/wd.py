#
# Testcase for WebDriver Object
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


@responses.activate
def test_init(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': {
                'browserName': 'chrome'
            }
        })
    assert driver.desired_capabilities == {
        'browserName': 'chrome',
        'platformName': 'Android'
    }
    assert driver == driver.init()
    assert driver.session_id == '2345'
    assert driver.capabilities == {'browserName': 'chrome'}


@responses.activate
def test_attach(driver):
    assert driver.session_id == '2345'
    driver.attach('1234')
    assert driver.session_id == '1234'
    driver.attach('2345')

@responses.activate
def test_get_url(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/url',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver == driver.get('www.taobao.com')


@responses.activate
def test_get_current_url(driver):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/url',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': 'www.taobao.com'
        })
    assert driver.current_url == 'www.taobao.com'


@responses.activate
def test_find_element(driver):
    import json
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': {
                'ELEMENT': '1'
            }
        })
    el = driver.element('id', 'login')
    assert isinstance(el, WebElement)
    assert el.element_id == '1'
    assert el._driver == driver
    body = responses.calls[0].request.body.decode('utf-8')
    assert json.loads(body) == {
        "using": "id",
        "value": "login"
    }


@responses.activate
def test_element_if_exists(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': {
                'ELEMENT': '1'
            }
        })
    ret = driver.element_if_exists('id', 'login')
    assert ret


@responses.activate
def test_element_not_exists(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element',
        json={
            'status': 7,
            'sessionId': '2345',
            'value': 'no such element'
        })
    ret = driver.element_if_exists('id', 'login')
    assert not ret


@responses.activate
def test_element_or_none(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element',
        json={
            'status': 7,
            'sessionId': '2345',
            'value': 'no such element'
        })
    ret = driver.element_or_none('id', 'login')
    assert not ret


@responses.activate
def test_find_elements(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/elements',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': [{
                'ELEMENT': '1'
            }, {
                'ELEMENT': '2'
            }]
        })
    els = driver.elements('id', 'login')
    assert isinstance(els, list)
    for el in els:
        assert isinstance(el, WebElement)


def test_wait_for(driver):
    from datetime import datetime
    assert driver == driver.wait_for()

    with pytest.raises(TypeError):
        driver.wait_for(asserter='')

    before_time = datetime.now()

    with pytest.raises(WebDriverException):
        driver.wait_for(2000, 500, asserter=lambda d: exec_("raise WebDriverException('test')"))

    after_time = datetime.now()
    during = after_time - before_time
    assert during.seconds == 2


@responses.activate
def test_wait_for_element(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': {
                'ELEMENT': '1'
            }
        })

    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/displayed',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': True
        })

    from datetime import datetime
    el = driver.wait_for_element('id', 'login')

    with pytest.raises(TypeError):
        driver.wait_for_element('id', 'login', asserter='')

    before_time = datetime.now()

    with pytest.raises(WebDriverException) as excinfo:
        driver.wait_for_element(
            'id', 'login', 2000, 500,
            asserter=is_not_displayed)
    assert excinfo.value.error == 'element is visible'

    after_time = datetime.now()
    during = after_time - before_time
    assert during.seconds == 2


@responses.activate
def test_wait_for_elements(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/elements',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': [{
                'ELEMENT': '1'
            }, {
                'ELEMENT': '2'
            }]
        })

    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/1/displayed',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': True
        })

    from datetime import datetime
    els = driver.wait_for_elements('id', 'login')

    with pytest.raises(TypeError):
        driver.wait_for_elements('id', 'login', asserter='')

    before_time = datetime.now()

    with pytest.raises(WebDriverException) as excinfo:
        driver.wait_for_elements(
            'id', 'login', 2000, 500,
            asserter=is_not_displayed)
    assert excinfo.value.error == 'element is visible'

    after_time = datetime.now()
    during = after_time - before_time
    assert during.seconds == 2


@responses.activate
def test_quit(driver):
    responses.add(
        responses.DELETE,
        'http://127.0.0.1:3456/wd/hub/session/2345',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver == driver.quit()


@responses.activate
def test_back(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/back',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver == driver.back()


@responses.activate
def test_forward(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/forward',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver == driver.forward()


@responses.activate
def test_refresh(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/refresh',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver == driver.refresh()


@responses.activate
def test_title(driver):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/title',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': 'Hello, Macaca!'
        })
    assert driver.title == 'Hello, Macaca!'


@responses.activate
def test_current_window_handle(driver):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/window_handle',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': 'WINDOWS_1'
        })
    assert driver.current_window_handle == 'WINDOWS_1'


@responses.activate
def test_close_window(driver):
    responses.add(
        responses.DELETE,
        'http://127.0.0.1:3456/wd/hub/session/2345/window',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver.close() == driver


@responses.activate
def test_switch_to_window(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/window',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver.switch_to_window('WINDOWS_2') == driver


@responses.activate
def test_window_handles(driver):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/window_handles',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ['WINDOWS_1', 'WINDOWS_2']
        })
    assert driver.window_handles == ['WINDOWS_1', 'WINDOWS_2']


@responses.activate
def test_maximize_window(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/window/current/maximize',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver.maximize_window() == driver


@responses.activate
def test_set_window_size(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/window/current/size',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver.set_window_size(1280, 800) == driver


@responses.activate
def test_get_window_size(driver):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/window/current/size',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': {
                'width': 1280,
                'height': 800
            }
        })
    assert driver.get_window_size() == {
        'width': 1280,
        'height': 800
    }


@responses.activate
def test_set_window_position(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/window/current/position',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver.set_window_position(100, 200) == driver


@responses.activate
def test_get_window_position(driver):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/window/current/position',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': {
                'x': 100,
                'y': 200
            }
        })
    assert driver.get_window_position() == {
        'x': 100,
        'y': 200
    }



@responses.activate
def test_get_context(driver):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/context',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': 'NATIVE'
        })
    assert driver.context == 'NATIVE'


@responses.activate
def test_set_context(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/context',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    driver.context = 'WEBVIEW_1'
    assert responses.calls[0].request.body.decode('utf-8') == '{"name": "WEBVIEW_1"}'


@responses.activate
def test_get_contexts(driver):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/contexts',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ['NATIVE', 'WEBVIEW_1', 'WEBVIEW_2']
        })
    assert driver.contexts == ['NATIVE', 'WEBVIEW_1', 'WEBVIEW_2']


@responses.activate
def test_move_to(driver, element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/moveto',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver.move_to(element, 100, 200) == driver


@responses.activate
def test_flick(driver, element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/touch/flick',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver.flick(element, 100, 200, 100) == driver


@responses.activate
def test_tap(driver, element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/touch/click',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver.tap(element) == driver


@responses.activate
def test_swipe(driver, element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/temp/swipe',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver.swipe(0, 0, 200, 200) == driver
    assert driver.swipe(100, 100, 200, 200, 2000) == driver
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
def test_keys(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/keys',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver.send_keys(123) == driver
    body = responses.calls[0].request.body.decode('utf-8')
    data = json.loads(body)
    assert data['value'] == ['1', '2', '3']


@responses.activate
def test_switch_to_frame(driver, element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/frame',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    with pytest.raises(TypeError):
        driver.switch_to_frame('2')
    with pytest.raises(TypeError):
        driver.switch_to_frame([1])

    assert driver.switch_to_frame(element) == driver
    body = responses.calls[0].request.body.decode('utf-8')
    assert json.loads(body) == {
        "id": {
            "ELEMENT": "1"
        }
    }


@responses.activate
def test_switch_to_parent_frame(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/frame/parent',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver.switch_to_parent_frame() == driver


@responses.activate
def test_get_active_element(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/element/active',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': {
                'ELEMENT': '3'
            }
        })
    el = driver.get_active_element()
    assert isinstance(el, WebElement)
    assert el.element_id == '3'


@responses.activate
def test_get_page_source(driver):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/source',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': 'Hello, Macaca!'
        })
    assert driver.source == 'Hello, Macaca!'


@responses.activate
def test_execute_script(driver, element):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/execute',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': 'input'
        })
    assert driver.execute_script(
        'return arguments[0].tagName', element) == 'input'
    body = responses.calls[0].request.body.decode('utf-8')
    assert json.loads(body) == {
        'script': 'return arguments[0].tagName',
        'args': [{"ELEMENT": "1"}]
    }


@responses.activate
def test_execute_async_script(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/execute_async',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver.execute_async_script('document.title') == ''


@responses.activate
def test_cookies(driver):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/cookie',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': [
            {
                'name': '_ga',
                'value': 3213123
            }, {
                'name': 'first',
                'value': False
            }]
        })
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/cookie',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    responses.add(
        responses.DELETE,
        'http://127.0.0.1:3456/wd/hub/session/2345/cookie',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    responses.add(
        responses.DELETE,
        'http://127.0.0.1:3456/wd/hub/session/2345/cookie/first',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver.cookies == [
        {
            'name': '_ga',
            'value': 3213123
        }, {
            'name': 'first',
            'value': False
        }]
    assert driver.get_cookie('first')['value'] == False
    assert driver.get_cookie('last') == None
    assert driver.delete_cookie('first') == driver
    assert driver.delete_all_cookies() == driver
    assert driver.add_cookie({'name': 'first', 'value': True}) == driver

    with pytest.raises(TypeError):
        driver.add_cookie('error')

    with pytest.raises(KeyError):
        driver.add_cookie({'name': 'first'})


@responses.activate
def test_timeouts(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/timeouts/implicit_wait',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/timeouts/async_script',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/timeouts',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })

    assert driver.set_implicitly_wait(5000) == driver
    assert driver.set_script_timeout(5000) == driver
    assert driver.set_page_load_timeout(5000) == driver


@responses.activate
def test_alert(driver):
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/accept_alert',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/dismiss_alert',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/alert_text',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': 'Hello, Macaca!'
        })
    responses.add(
        responses.POST,
        'http://127.0.0.1:3456/wd/hub/session/2345/alert_text',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': ''
        })
    assert driver.accept_alert() == driver
    assert driver.dismiss_alert() == driver
    assert driver.alert_text == 'Hello, Macaca!'
    assert driver.alert_keys(123) == driver


@responses.activate
def test_screenshot(driver):
    responses.add(
        responses.GET,
        'http://127.0.0.1:3456/wd/hub/session/2345/screenshot',
        json={
            'status': 0,
            'sessionId': '2345',
            'value': 'R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs='
        })
    assert driver.take_screenshot() == 'R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs='
    assert driver.save_screenshot('./test.png') == driver
    from os import remove

    try:
        remove('./test.png')
    except:
        pass

    with pytest.raises(IOError):
        driver.save_screenshot('/etc/test.png')

    driver.save_screenshot('/etc/test.png', True)
