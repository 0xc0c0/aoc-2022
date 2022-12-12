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
    heights, start, end = parse_data(test_data)
    assert type(heights) == np.ndarray
    assert heights[1,3] == 18
    assert heights.ndim == 2
    assert heights.shape == (5,8)
    assert start == (0,0)
    assert end == (2,5)
  
def test_all(test_data):
    heights, start, end = parse_data(test_data)
    best = run_moves(heights, start, end)
    assert best[end] == 31
    fewest = find_fastest_starting_point(heights, end)
    assert fewest == 29
