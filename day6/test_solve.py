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
    text_stream = parse_data(test_data)
  
def test_all(test_data):
    text_stream = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'
    assert find_first_x_unique(text_stream, 4) == 10
    assert find_first_x_unique(text_stream, 14) == 29
    
