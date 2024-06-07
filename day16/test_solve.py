"""Test program using pytest for AoC solver"""
import os
import pytest
from .solve import parse_data, init_states, get_optimal_pressure


@pytest.fixture(name="test_data")
def get_test_data():
    """Data fixture for AoC test data

    Returns:
        str: raw test data as a string
    """
    # dynamically obtain full path of 'test.txt'
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test.txt")
    with open(test_file, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def test_parse_input(test_data):
    """Tests parsing functions for test data

    Returns:
        str: raw test data as a string
    """
    flow_nodes = parse_data(test_data)
    assert len(flow_nodes) == 10
    assert flow_nodes["BB"]["r"] == 13
    assert flow_nodes["GG"]["r"] == 0
    assert "FF" in flow_nodes["GG"]["nn"]


def test_all(test_data):
    """Test cases for actual problem

    Returns:
        str: raw test data as a string
    """
    pass
    # nodes = parse_data(test_data)
    # states = init_states(nodes)
    # pressure = get_optimal_pressure(nodes["AA"], states, 30)
    # assert pressure == 1651
