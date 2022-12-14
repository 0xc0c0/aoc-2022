import pytest
import os
import numpy as np
from .solve import *

@pytest.fixture
def test_data():
    #dynamically obtain full path of 'test.txt'
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.txt')
    with open(test_file, 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    heights = parse_data(test_data)
    assert heights.ndim == 2
    assert heights.shape == (5,5)
    assert heights[2][0] == 6
    assert heights[4,4] == 0
  
def test_all(test_data):
    trees = parse_data(test_data)
    assert count_visible(trees) == 21
    assert get_max_scenic_score(trees) == 8