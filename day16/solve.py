from __future__ import annotations
from typing import List, Dict
from copy import copy, deepcopy
import logging
import os
import re
from dataclasses import dataclass
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


# @dataclass
# class FlowNode:
#     """Data class for the nodes in the volcano flow control system for Day 16 AoC 2022"""

#     name: str
#     rate: int
#     next_nodes: List[FlowNode]

#     def __hash__(self):
#         return hash(self.name)

#     def __repr__(self):
#         next_nodes = [n.name for n in self.next_nodes]
#         return f"{self.name}, {self.rate}, next: {[next_nodes]}"


def get_file_data(fn="input.txt"):
    """Get file data from input.txt

    Args:
        fn (str, optional): _description_. Defaults to "input.txt".

    Returns:
        _type_: raw data from the file as a str
    """
    with open(fn, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def parse_line(text_line):
    """Parse a line of text

    Args:
        text_line (_type_): _description_

    Returns:
        _type_: _description_
    """
    first_text, second_text = text_line.split(";")
    first_regex = "Valve ([A-Z]{2}) has flow rate=([0-9]+)"
    second_regex = "[A-Z]{2}"
    name, rate_text = re.findall(first_regex, first_text)[0]
    next_nodes = re.findall(second_regex, second_text)
    return name, int(rate_text), next_nodes


def parse_data(text_data):
    """Parse all the data from the input

    Args:
        text_data (_type_): _description_

    Returns:
        _type_: _description_
    """
    entries = [parse_line(line) for line in text_data.strip("\n").strip().split("\n")]
    flow_nodes = {n: {"r": r, "nn": nn} for (n, r, nn) in entries}

    return flow_nodes

TRACKER = dict()

def get_max_pressure_released(flow_nodes, cur_node='AA', opened_nodes=tuple(), min_left=30, released=0):
    """Find max possible pressure releasable from flow nodes

    Args:
        flow_nodes (list): list of flow nodes and their tunneling paths
    """
    if min_left == 0:
        if min_left >= TRACKER[(cur_node, opened_nodes)]['min_left'] and released
        return released
    #add check for memoization here
    elif 
    else:
        option1 = None
        if flow_nodes[cur_node]['r'] > 0:
            option1 = flow_nodes


def main():
    """Complete Day 16 problems"""
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    flow_nodes = parse_data(data)

    answer = 0
    print(f"Puzzle1: <SUMMARY>: {answer}")
    answer = 0
    print(f"Puzzle2: <SUMMARY>: {answer}")


if __name__ == "__main__":
    main()
