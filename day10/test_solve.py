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
    instructions = parse_data(test_data)
  
def test_all(test_data):
    instructions = parse_data(test_data)
    cycle_values = run_instructions(instructions)
    test_total = get_signal_strengths(cycle_values, [20,60,100,140,180,220])
    assert test_total == 13140
