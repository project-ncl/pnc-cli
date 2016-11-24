import random
import string
from mock import MagicMock
import pytest

__author__ = 'thauser'


def create_mock_list_with_name_attribute():
    member1 = MagicMock(id=1)
    member2 = MagicMock(id=2)
    member1.name = 'testerino'
    member2.name = 'anotherone'
    content = MagicMock(content=[member1, member2])
    return content



def create_mock_object_with_name_attribute(name):
    mock = MagicMock()
    mock.id = 1
    mock.name = name
    return mock


def gen_random_name():
    return "cli-test-" + ''.join(random.choice(string.ascii_uppercase + string.digits)
                            for _ in range(10))


def gen_random_version():
    return ''.join(random.choice(string.digits)for _ in range(10)) + '.' + ''.join(random.choice(string.digits) for _ in range(10))


def assert_raises_valueerror(api, function, **kwargs):
    with pytest.raises(ValueError):
        getattr(api, function)(**kwargs)


def assert_raises_typeerror(api, function, **kwargs):
    with pytest.raises(TypeError):
        getattr(api, function)(invalid_param=1, **kwargs)
