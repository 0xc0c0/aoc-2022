import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
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
