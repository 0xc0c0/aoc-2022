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
    stacks, moves = parse_data(test_data)
    assert len(moves) == 4
    assert stacks[2][1] == 'C'
  
def test_all(test_data):
    stacks, moves = parse_data(test_data)
    complete_moves(stacks, moves)
    assert get_tops(stacks) == 'CMZ'
    stacks, moves = parse_data(test_data)
    complete_moves_part2(stacks, moves)
    assert get_tops(stacks) == 'MCD'
