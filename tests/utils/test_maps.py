import pytest
from utils.maps import is_coordinate


@pytest.mark.parametrize('coord,expected', [
    ('-34.5850539,-58.4563165', True),
    ('34.5850539,-58.4563165', True),
    ('-34.5850539,58.4563165', True),
    ('34.5850539,58.4563165', True),
    ('foooo', False),
    ('-345850539,584563165', False),
    ('34.5850539;58.4563165', False),
    ('-34.5850539,58.4563165,16z', False),
])
def test_coordinate_validator(coord, expected):
    assert is_coordinate(coord) == expected