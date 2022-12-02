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
    rounds = parse_data(test_data)
    assert type(rounds) == list
    assert rounds[0] == ['A', 'Y']
  
def test_all(test_data):
    rounds = parse_data(test_data)
    assert score_round(*rounds[0]) == 8
    assert score_round(*rounds[1]) == 1
    assert score_all_rounds(rounds) == 15
    assert score_all_strategy(rounds) == 12