#
# Testcase for WebDriverResult
#


import pytest

from macaca.webdriverresult import WebDriverResult
from macaca.webdriverexception import WebDriverException


@pytest.fixture(scope="module")
def right_result():
    obj = {
        'sessionId': '1234',
        'status': 0,
        'value': 'ok'
    }
    return obj


@pytest.fixture(scope="module",
    params=[
        {
            'sessionId': '1234',
            'status': 1,
            'value': 'ok'
        },
        {
            'sessionId': '1234',
            'status': 1,
            'value': {
                'message': 'no such element',
                'screen': 'xxx',
                'stacktrace': ['a', 'b']
            }
        }])
def wrong_result(request):
    return request.param


def test_result_from_obj(right_result):
    wd_result = WebDriverResult.from_object(right_result)
    assert wd_result.session_id == right_result['sessionId']
    assert wd_result.status == right_result['status']
    assert wd_result.value == right_result['value']


def test_right_result(right_result):
    wd_result = WebDriverResult.from_object(right_result)
    assert wd_result.raise_for_status() == None


def test_wrong_result(wrong_result):
    wd_result = WebDriverResult.from_object(wrong_result)
    with pytest.raises(WebDriverException) as excinfo:
        wd_result.raise_for_status()
    ex = excinfo.value
    assert ex.message is not None
