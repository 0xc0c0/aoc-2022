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
    nodes = parse_data(test_data)
    assert len(nodes) == 10
    assert nodes['BB'].rate == 13
    assert nodes['GG'].rate == 0
    ff = nodes['FF']
    assert ff in nodes['GG'].next_nodes
    states = init_states(nodes)
    assert states[ff] == False
  
def test_all(test_data):
    nodes = parse_data(test_data)
    states = init_states(nodes)
    pressure = get_optimal_pressure(nodes['AA'], states, 30)
    assert pressure == 1651
