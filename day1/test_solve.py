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
    inventories = parse_data(test_data)
    assert type(inventories) == list
    assert inventories[0][0] == 1000
    assert len(inventories) == 5
    assert inventories[3][1] == 8000
      
def test_all(test_data):
    inventories = parse_data(test_data)
    assert get_max_inventory(inventories) == 24000
    assert get_top3_inventories(inventories) == 45000
