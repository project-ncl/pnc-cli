from mock import MagicMock

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
    mock.name = name
    return mock


