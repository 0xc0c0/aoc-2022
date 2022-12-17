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
    rock_lines = parse_data(test_data)
    assert type(rock_lines) == list
    assert len(rock_lines) == 2
    assert len(rock_lines[0]) == 3
    assert len(rock_lines[0][0]) == 2
    assert rock_lines[0][1][1] == 6
    rp = get_all_rock_points(rock_lines)
    assert len(rp) == 20
  
def test_all(test_data):
    rock_lines = parse_data(test_data)
    rp = get_all_rock_points(rock_lines)
    sp = get_all_sand_points(rp)
    assert len(sp) == 24
    rp2 = add_floor(rp)
    sp2 = get_all_sand_points(rp2, check_infinity=False)
    assert len(sp2) == 93
