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
    assert len(pairs) == 8
    assert len(pairs[3]) == 2
    assert pairs[1][1] == [[1],4]

def test_all(test_data):
    pairs = parse_data(test_data)
    assert sum(get_ordered_pairs_indices(pairs)) == 13
    ordered_packets = get_ordered_packets(pairs)
    assert get_decoder_key(ordered_packets) == 140