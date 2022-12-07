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
    lines = parse_data(test_data)
    assert len(lines) == 23
  
def test_all(test_data):
    lines = parse_data(test_data)
    root = process_lines(lines)
    a = root.getChildDir('a')
    e = a.getChildDir('e')
    assert e.getTotalSize() == 584
    assert a.getTotalSize() == 94853
    d = root.getChildDir('d')
    assert d.getTotalSize() == 24933642
    assert root.getTotalSize() == 48381165
    
    assert len(root.getAllDirs()) == 4
    assert find_best_dir_to_free_up_space(root) == 24933642
    
