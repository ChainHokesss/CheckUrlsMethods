import pytest
import asyncio

from .main import check_methods, get_available_methods, url_methods, url_validator


@pytest.mark.parametrize(
    'url, method, valid',
    (
        ('https://google.com', 'GET', True),
        ('https://www.facebook.com', 'DELETE', True),
        ('https://google.com', 'not', False),
        ('https://www.python-httpx.org/quickstart/', 'GET', True)
    )
)
def test_check_method_func(url, method, valid):
    res = asyncio.run(check_methods(method, url))
    if valid:
        assert res[0] == method
        assert res[1] != 405
    else:
        assert res is None


@pytest.mark.parametrize(
    'url, valid',
    (
        ("https://ca-manager-api.herokuapp.com/api/user", True),
        ("hello World", False),
        ("https://google.com", True),
        ("facebook.com", False),
        ("https://www.facebook.com", True),
        ("https://esp8266.ru/forum/threads/ehnergopotreblenie-esp-novoe.2591/", True),
        ("https://www.python-httpx.org/quickstart/", True),
        ("jlad;asmdl;as.com", False),
    )
)
def test_url_validation_func(url, valid):
    res = url_validator(url)
    if valid:
        assert res == url
    else:
        assert res is None


@pytest.mark.parametrize(
    'url, valid',
    (
        ('https://google.com', True),
        ('facebook.com', False),
        ('https://www.python-httpx.org/async/', True),
        ('https://docs.pytest.org/en/7.2.x/#id1', True),
    )
)
def test_get_available_methods_func(url, valid):
    res = asyncio.run(get_available_methods(url, url_methods))
    if valid:
        assert res[0] == url
        assert False if 405 in res[1].values() else True
    else:
        assert res is None
