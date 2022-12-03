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
    rucksacks = parse_data(test_data)
    assert type(rucksacks) == list
    assert len(rucksacks[0]) == 2
    assert len(rucksacks[0][0]) == len(rucksacks[0][1])
  
def test_all(test_data):
    rucksacks = parse_data(test_data)
    assert find_rucksack_shared_item(*rucksacks[0]) == 'p'
    assert get_item_priority('a') == 1
    assert get_item_priority('z') == 26
    assert get_item_priority('A') == 27
    assert get_item_priority('Z') == 52
    assert get_priority_sum(rucksacks) == 157
    
    rucksacks = parse_data_no_breakup(test_data)
    elf_groups = get_elf_groups(rucksacks)
    assert len(elf_groups) == 2
    assert find_common_badge(*elf_groups[0]) == 'r'
    assert find_common_badge(*elf_groups[1]) == 'Z'
    assert get_priority_sum_elf_groups(rucksacks) == 70