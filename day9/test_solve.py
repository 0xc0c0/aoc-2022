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

@pytest.fixture
def test_data2():
    #dynamically obtain full path of 'test.txt'
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test2.txt')
    with open(test_file, 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    motions = parse_data(test_data)
    assert len(motions) == 8
    assert motions[0] == ['R', 4]
    assert motions[-1] == ['R', 2]
  
def test_all(test_data, test_data2):
    motions = parse_data(test_data)
    assert count_tail_motions(motions) == 13
    motions = parse_data(test_data2)
    assert count_bigger_tail_motions(motions) == 36