import pytest
import os
from .solve import *

@pytest.fixture
def test_data():
    #dynamically obtain full path of 'test.txt'
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.txt')
    with open(test_file, 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    sensors, beacons = parse_data(test_data)
    assert len(sensors) == len(beacons)
    assert sensors[0]['loc'][0] == 0
  
def test_all(test_data):
    sensors, beacons = parse_data(test_data)
    min_dist = min(sensors, key=lambda s:s['dist'])['dist']
    assert min_dist == 1
    all_ranges = get_all_impossible_x_ranges_y_intercept(sensors, y_0=10)
    all_points = get_all_impossible_points_y_intercept(all_ranges, beacons, y_0=10)
    assert len(all_points) == 26
    x = get_unaccounted_point(sensors, 20)
    assert x == (14,11)
    assert get_tuning_freq(sensors, axis_lim=20) == 56000011