import pytest
from utils.maps import is_coordinate, distance_between


@pytest.mark.parametrize('coord,valid', [
    ('-55.44,34.55', True),
    ('Fooo', False)
])
def test_coordinate_validator(coord, valid):
    assert is_coordinate(coord) == valid

def test_distance(mocker):
    dummy_data = {
        "rows": [
      {
         "elements" : [
            {
               "distance": {
                  "text": "225 mi",
                  "value": 361715
               },
               "duration": {
                  "text": "3 hours 49 mins",
                  "value": 13725
               },
               "status": "OK"
            }
         ]
      }
    ],
    }
    distance_mock = mocker.Mock()
    mocker.patch('utils.maps.Client', return_value=distance_mock)
    distance_mock.distance_matrix.return_value=dummy_data
    dist = distance_between(['fooo'], 'bar')

    assert dist == [{'status': True, 'distance': 361715, 'duration': 13725}]