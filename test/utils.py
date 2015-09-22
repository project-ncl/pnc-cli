from mock import MagicMock

__author__ = 'thauser'

def create_mock_content_list():
    member1 = MagicMock(id=1)
    member2 = MagicMock(id=2)
    member1.name = 'testerino'
    member2.name = 'anotherone'
    content = MagicMock(content=[member1, member2])
    return content

