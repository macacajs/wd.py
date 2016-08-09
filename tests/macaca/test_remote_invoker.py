#
# Testcase for RemoteInvoker
#


import pytest
import responses

from macaca.remote_invoker import RemoteInvoker
from macaca.command import Command


@pytest.fixture(scope="function",
                params=['https://macaca:123456@192.168.3.1:5678/test/hub',
                        {
                            'protocol': 'https',
                            'hostname': '192.168.3.1',
                            'username': 'macaca',
                            'password': '123456',
                            'port': 5678,
                            'path': 'test/hub'
                        }])
def remote_invoker(request):
    return RemoteInvoker(request.param)


def test_init(remote_invoker):
    assert remote_invoker._url == "https://macaca:123456@192.168.3.1:5678/test/hub"


def test_init_default():
    r = RemoteInvoker()
    assert r._url == "http://127.0.0.1:3456/wd/hub"


def test_init_scheme():
    r = RemoteInvoker({
        'protocol': 'https'
    })
    assert r._url == "https://127.0.0.1:3456/wd/hub"


def test_wrong_init_missing_scheme():
    with pytest.raises(ValueError):
        r = RemoteInvoker('www.error.com')


def test_wrong_init_wrong_scheme():
    with pytest.raises(ValueError):
        r = RemoteInvoker('xxx://www.error.com')


def test_wrong_init_protocol():
    with pytest.raises(ValueError):
        r = RemoteInvoker({
            'protocol': 'xxx',
            'hostname': '192.168.3.1',
            'username': 'macaca',
            'password': '123456',
            'port': 5678,
            'path': 'test/hub'
        })


def test_wrong_init_type():
    with pytest.raises(TypeError):
        r = RemoteInvoker(['wwww.error.com'])


@responses.activate
def test_request_server(remote_invoker):
    responses.add(responses.GET, 'https://macaca:123456@192.168.3.1:5678/test/hub/status',
                  json={'status': 0})
    resp = remote_invoker.execute(Command.STATUS)


def test_missing_uri_params(remote_invoker):
    with pytest.raises(KeyError):
        resp = remote_invoker.execute(Command.CLICK_ELEMENT)


@responses.activate
def test_correct_uri_and_data(remote_invoker):
    url = 'https://macaca:123456@192.168.3.1:5678/test/hub/session/1234/element/1/click'
    responses.add(responses.POST,
                  url,
                  json={'status': 0})
    resp = remote_invoker.execute(Command.CLICK_ELEMENT, {
        'session_id': '1234',
        'element_id': 1,
        'data': 'test'
    })
    assert responses.calls[0].request.url == url
    assert responses.calls[0].request.body == '{"data": "test"}'


@responses.activate
def test_request(remote_invoker):
    body = {
        'data': 'macaca'
    }
    responses.add(responses.POST, 'https://httpbin.org/post',
                  json=body)
    resp = remote_invoker._request('POST', 'https://httpbin.org/post', body)
    assert resp == body
