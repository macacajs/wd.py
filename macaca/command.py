#
# https = //w3c.github.io/webdriver/webdriver-spec.html#list-of-endpoints
# Commands according to WebDriver Endpoints
#

from collections import namedtuple

Endpoint = namedtuple('Endpoint', ['method', 'uri'])


class Command(object):
    """Commands for WebDriver Defined Endpoints."""
    STATUS = Endpoint(
        'GET',
        '/status'
    )
    NEW_SESSION = Endpoint(
        'POST',
        '/session'
    )
    GET_ALL_SESSIONS = Endpoint(
        'GET',
        '/sessions'
    )
    QUIT = Endpoint(
        'DELETE',
        '/session/{session_id}'
    )
    GET_CURRENT_WINDOW_HANDLE = Endpoint(
        'GET',
        '/session/{session_id}/window_handle'
    )
    GET_WINDOW_HANDLES = Endpoint(
        'GET',
        '/session/{session_id}/window_handles'
    )
    GET = Endpoint(
        'POST',
        '/session/{session_id}/url'
    )
    GO_FORWARD = Endpoint(
        'POST',
        '/session/{session_id}/forward'
    )
    GO_BACK = Endpoint(
        'POST',
        '/session/{session_id}/back'
    )
    REFRESH = Endpoint(
        'POST',
        '/session/{session_id}/refresh'
    )
    EXECUTE_SCRIPT = Endpoint(
        'POST',
        '/session/{session_id}/execute'
    )
    GET_CURRENT_URL = Endpoint(
        'GET',
        '/session/{session_id}/url'
    )
    GET_TITLE = Endpoint(
        'GET',
        '/session/{session_id}/title'
    )
    GET_PAGE_SOURCE = Endpoint(
        'GET',
        '/session/{session_id}/source'
    )
    SCREENSHOT = Endpoint(
        'GET',
        '/session/{session_id}/screenshot'
    )
    ELEMENT_SCREENSHOT = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/screenshot'
    )
    FIND_ELEMENT = Endpoint(
        'POST',
        '/session/{session_id}/element'
    )
    FIND_ELEMENTS = Endpoint(
        'POST',
        '/session/{session_id}/elements'
    )
    GET_ACTIVE_ELEMENT = Endpoint(
        'POST',
        '/session/{session_id}/element/active'
    )
    FIND_CHILD_ELEMENT = Endpoint(
        'POST',
        '/session/{session_id}/element/{element_id}/element'
    )
    FIND_CHILD_ELEMENTS = Endpoint(
        'POST',
        '/session/{session_id}/element/{element_id}/elements'
    )
    CLICK_ELEMENT = Endpoint(
        'POST',
        '/session/{session_id}/element/{element_id}/click'
    )
    CLEAR_ELEMENT = Endpoint(
        'POST',
        '/session/{session_id}/element/{element_id}/clear'
    )
    SWIPE_ELEMENT = Endpoint(
        'POST',
        '/session/{session_id}/element/{element_id}/swipe'
    )
    SUBMIT_ELEMENT = Endpoint(
        'POST',
        '/session/{session_id}/element/{element_id}/submit'
    )
    GET_ELEMENT_TEXT = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/text'
    )
    SEND_KEYS_TO_ELEMENT = Endpoint(
        'POST',
        '/session/{session_id}/element/{element_id}/value'
    )
    SEND_KEYS_TO_ACTIVE_ELEMENT = Endpoint(
        'POST',
        '/session/{session_id}/keys'
    )
    UPLOAD_FILE = Endpoint(
        'POST',
        "/session/{session_id}/file"
    )
    GET_ELEMENT_VALUE = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/value'
    )
    GET_ELEMENT_TAG_NAME = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/name'
    )
    IS_ELEMENT_SELECTED = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/selected'
    )
    SET_ELEMENT_SELECTED = Endpoint(
        'POST',
        '/session/{session_id}/element/{element_id}/selected'
    )
    IS_ELEMENT_ENABLED = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/enabled'
    )
    IS_ELEMENT_DISPLAYED = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/displayed'
    )
    GET_ELEMENT_LOCATION = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/location'
    )
    GET_ELEMENT_LOCATION_ONCE_SCROLLED_INTO_VIEW = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/location_in_view'
    )
    GET_ELEMENT_SIZE = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/size'
    )
    GET_ELEMENT_RECT = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/rect'
    )
    GET_ELEMENT_PROPERTY = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/property/{name}'
    )
    GET_ELEMENT_ATTRIBUTE = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/attribute/{name}'
    )
    ELEMENT_EQUALS = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/equals/{other}'
    )
    GET_ALL_COOKIES = Endpoint(
        'GET',
        '/session/{session_id}/cookie'
    )
    ADD_COOKIE = Endpoint(
        'POST',
        '/session/{session_id}/cookie'
    )
    DELETE_ALL_COOKIES = Endpoint(
        'DELETE',
        '/session/{session_id}/cookie'
    )
    DELETE_COOKIE = Endpoint(
        'DELETE',
        '/session/{session_id}/cookie/{name}'
    )
    SWITCH_TO_FRAME = Endpoint(
        'POST',
        '/session/{session_id}/frame'
    )
    SWITCH_TO_PARENT_FRAME = Endpoint(
        'POST',
        '/session/{session_id}/frame/parent'
    )
    SWITCH_TO_WINDOW = Endpoint(
        'POST',
        '/session/{session_id}/window'
    )
    CLOSE = Endpoint(
        'DELETE',
        '/session/{session_id}/window'
    )
    GET_ELEMENT_VALUE_OF_CSS_PROPERTY = Endpoint(
        'GET',
        '/session/{session_id}/element/{element_id}/css/{property_name}'
    )
    IMPLICIT_WAIT = Endpoint(
        'POST',
        '/session/{session_id}/timeouts/implicit_wait'
    )
    EXECUTE_ASYNC_SCRIPT = Endpoint(
        'POST',
        '/session/{session_id}/execute_async'
    )
    SET_SCRIPT_TIMEOUT = Endpoint(
        'POST',
        '/session/{session_id}/timeouts/async_script'
    )
    SET_TIMEOUTS = Endpoint(
        'POST',
        '/session/{session_id}/timeouts'
    )
    DISMISS_ALERT = Endpoint(
        'POST',
        '/session/{session_id}/dismiss_alert'
    )
    ACCEPT_ALERT = Endpoint(
        'POST',
        '/session/{session_id}/accept_alert'
    )
    SET_ALERT_VALUE = Endpoint(
        'POST',
        '/session/{session_id}/alert_text'
    )
    GET_ALERT_TEXT = Endpoint(
        'GET',
        '/session/{session_id}/alert_text'
    )
    SET_ALERT_CREDENTIALS = Endpoint(
        'POST',
        '/session/{session_id}/alert/credentials'
    )
    CLICK = Endpoint(
        'POST',
        '/session/{session_id}/click'
    )
    DOUBLE_CLICK = Endpoint(
        'POST',
        '/session/{session_id}/doubleclick'
    )
    MOUSE_DOWN = Endpoint(
        'POST',
        '/session/{session_id}/buttondown'
    )
    MOUSE_UP = Endpoint(
        'POST',
        '/session/{session_id}/buttonup'
    )
    MOVE_TO = Endpoint(
        'POST',
        '/session/{session_id}/moveto'
    )
    GET_WINDOW_SIZE = Endpoint(
        'GET',
        '/session/{session_id}/window/{window_handle}/size'
    )
    W3C_GET_WINDOW_SIZE = Endpoint(
        'GET',
        '/session/{session_id}/window/size'
    )
    SET_WINDOW_SIZE = Endpoint(
        'POST',
        '/session/{session_id}/window/{window_handle}/size'
    )
    W3C_SET_WINDOW_SIZE = Endpoint(
        'POST',
        '/session/{session_id}/window/size'
    )
    GET_WINDOW_POSITION = Endpoint(
        'GET',
        '/session/{session_id}/window/{window_handle}/position'
    )
    SET_WINDOW_POSITION = Endpoint(
        'POST',
        '/session/{session_id}/window/{window_handle}/position'
    )
    MAXIMIZE_WINDOW = Endpoint(
        'POST',
        '/session/{session_id}/window/{window_handle}/maximize'
    )
    W3C_MAXIMIZE_WINDOW = Endpoint(
        'POST',
        '/session/{session_id}/window/maximize'
    )
    SET_SCREEN_ORIENTATION = Endpoint(
        'POST',
        '/session/{session_id}/orientation'
    )
    GET_SCREEN_ORIENTATION = Endpoint(
        'GET',
        '/session/{session_id}/orientation'
    )
    SINGLE_TAP = Endpoint(
        'POST',
        '/session/{session_id}/touch/click'
    )
    TOUCH_DOWN = Endpoint(
        'POST',
        '/session/{session_id}/touch/down'
    )
    TOUCH_UP = Endpoint(
        'POST',
        '/session/{session_id}/touch/up'
    )
    TOUCH_MOVE = Endpoint(
        'POST',
        '/session/{session_id}/touch/move'
    )
    TOUCH_SCROLL = Endpoint(
        'POST',
        '/session/{session_id}/touch/scroll'
    )
    DOUBLE_TAP = Endpoint(
        'POST',
        '/session/{session_id}/touch/doubleclick'
    )
    LONG_PRESS = Endpoint(
        'POST',
        '/session/{session_id}/touch/longclick'
    )
    FLICK = Endpoint(
        'POST',
        '/session/{session_id}/touch/flick'
    )
    EXECUTE_SQL = Endpoint(
        'POST',
        '/session/{session_id}/execute_sql'
    )
    GET_LOCATION = Endpoint(
        'GET',
        '/session/{session_id}/location'
    )
    SET_LOCATION = Endpoint(
        'POST',
        '/session/{session_id}/location'
    )
    GET_APP_CACHE = Endpoint(
        'GET',
        '/session/{session_id}/application_cache'
    )
    GET_APP_CACHE_STATUS = Endpoint(
        'GET',
        '/session/{session_id}/application_cache/status'
    )
    CLEAR_APP_CACHE = Endpoint(
        'DELETE',
        '/session/{session_id}/application_cache/clear'
    )
    GET_NETWORK_CONNECTION = Endpoint(
        'GET',
        '/session/{session_id}/network_connection'
    )
    SET_NETWORK_CONNECTION = Endpoint(
        'POST',
        '/session/{session_id}/network_connection'
    )
    GET_LOCAL_STORAGE_ITEM = Endpoint(
        'GET',
        '/session/{session_id}/local_storage/key/{key}'
    )
    REMOVE_LOCAL_STORAGE_ITEM = Endpoint(
        'DELETE',
        '/session/{session_id}/local_storage/key/{key}'
    )
    GET_LOCAL_STORAGE_KEYS = Endpoint(
        'GET',
        '/session/{session_id}/local_storage'
    )
    SET_LOCAL_STORAGE_ITEM = Endpoint(
        'POST',
        '/session/{session_id}/local_storage'
    )
    CLEAR_LOCAL_STORAGE = Endpoint(
        'DELETE',
        '/session/{session_id}/local_storage'
    )
    GET_LOCAL_STORAGE_SIZE = Endpoint(
        'GET',
        '/session/{session_id}/local_storage/size'
    )
    GET_SESSION_STORAGE_ITEM = Endpoint(
        'GET',
        '/session/{session_id}/session_storage/key/{key}'
    )
    REMOVE_SESSION_STORAGE_ITEM = Endpoint(
        'DELETE',
        '/session/{session_id}/session_storage/key/{key}'
    )
    GET_SESSION_STORAGE_KEYS = Endpoint(
        'GET',
        '/session/{session_id}/session_storage'
    )
    SET_SESSION_STORAGE_ITEM = Endpoint(
        'POST',
        '/session/{session_id}/session_storage'
    )
    CLEAR_SESSION_STORAGE = Endpoint(
        'DELETE',
        '/session/{session_id}/session_storage'
    )
    GET_SESSION_STORAGE_SIZE = Endpoint(
        'GET',
        '/session/{session_id}/session_storage/size'
    )
    GET_LOG = Endpoint(
        'POST',
        '/session/{session_id}/log'
    )
    GET_AVAILABLE_LOG_TYPES = Endpoint(
        'GET',
        '/session/{session_id}/log/types'
    )
    CURRENT_CONTEXT_HANDLE = Endpoint(
        'GET',
        '/session/{session_id}/context'
    )
    CONTEXT_HANDLES = Endpoint(
        'GET',
        '/session/{session_id}/contexts'
    )
    SWITCH_TO_CONTEXT = Endpoint(
        'POST',
        '/session/{session_id}/context'
    )
    PERFORM_ACTIONS = Endpoint(
        'POST',
        '/session/{session_id}/actions'
    )
