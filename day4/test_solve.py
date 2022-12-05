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
    pairs = parse_data(test_data)
    assert type(pairs) == list
    assert tuple(pairs[0][1]) == (6,8)
    assert tuple(pairs[0][0]) == (2,4)
    assert len(pairs) == 6
  
def test_all(test_data):
    pairs = parse_data(test_data)
    assert check_full_containment(*pairs[0]) == False
    assert check_full_containment(*pairs[3]) == True
    assert count_contained_pairs(pairs) == 2
    assert count_overlapping_pairs(pairs) == 4
