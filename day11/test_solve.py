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
    monkey_notes = parse_data(test_data)
    assert type(monkey_notes) == list
    assert monkey_notes[0].number == 0
    assert len(monkey_notes[0].items) == 2
    assert monkey_notes[3].items == [74]
  
def test_all(test_data):
    monkey_notes = parse_data(test_data)
    run_round(monkey_notes)
    assert len(monkey_notes[0].items) == 4
    assert 27 in monkey_notes[0].items
    
    # reset data/state
    monkey_notes = parse_data(test_data)
    run_round(monkey_notes)
    assert monkey_notes[0].items == [20, 23, 27, 26]
    run_rounds(monkey_notes, 19)
    assert [mn.total_inspected for mn in monkey_notes] == [101, 95, 7, 105]
    
    # reset data/state
    monkey_notes = parse_data(test_data)
    run_rounds_2(monkey_notes, 1)
    assert [mn.total_inspected for mn in monkey_notes] == [2,4,3,6]
    run_rounds_2(monkey_notes, 19)
    assert [mn.total_inspected for mn in monkey_notes] == [99, 97, 8, 103]
    monkey_notes = parse_data(test_data)
    run_rounds_2(monkey_notes, 10000)
    assert get_monkey_business(monkey_notes) == 2713310158
    