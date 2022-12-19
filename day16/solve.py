from __future__ import annotations
from typing import List, Dict
from copy import copy,deepcopy
import logging
import os
import re
from dataclasses import dataclass
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

@dataclass
class FlowNode:
    name: str
    rate: int
    next_nodes: List[FlowNode]
    
    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        return f"name: {self.name}, rate: {self.rate}, next_nodes: {[n.name for n in self.next_nodes]}"
    
def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_line(text_line):
    first_text, second_text = text_line.split(';')
    first_regex = 'Valve ([A-Z]{2}) has flow rate=([0-9]+)'
    second_regex = '[A-Z]{2}'
    name, rate_text = re.findall(first_regex, first_text)[0]
    next_nodes = re.findall(second_regex, second_text)
    return name, int(rate_text), next_nodes

def parse_data(text_data):
    entries = [parse_line(line) for line in text_data.strip('\n').strip().split('\n')]
    all_nodes = dict()
    for name, rate, _ in entries:
        all_nodes[name] = FlowNode(name, rate, list())
    for name, _, next_nodes in entries:
        for n in next_nodes:
            all_nodes[name].next_nodes.append(all_nodes[n])
    return all_nodes

def get_useful_remaining_valves(states):
    return [n for n,v in states.items() if n.rate > 0 and v == False]

def init_states(all_nodes:Dict[str]):
    return {v:False for (k,v) in all_nodes.items() if v.rate != 0}

def get_states_node_tracker_index(states, node:FlowNode):
    return [1 if v else 0 for _,v in states.items()] + [node.name]

def get_states_node_tracker(states_node_tracker, states, node:FlowNode):
    i = get_states_node_tracker_index(states, node)
    if i in states_node_tracker:
        return states_node_tracker[i]
    else:
        return None

def update_states_node_tracker(states_node_tracker, states, node, time_left, value):
    i = get_states_node_tracker_index(states, node)
    states_node_tracker[i] = value

def get_optimal_pressure(node:FlowNode, states, states_node_tracker, released_pressure:int=0, time_left:int=30):
    # initialize states tracker
    # [states + value_found]
    preexisting_value = get_states_node_tracker(states, node, time_left)
    if preexisting_value:
        return preexisting_value
    
    # check if all useful valves are already open
    logger.debug(f"node: {node.name}, time left: {time_left}")
    states_check = get_useful_remaining_valves(states)
    if len(states_check) == 0:  #nothing left to do
        return 0
    elif time_left <= 1:  #nothing can be value added with 1 minutes left (opening a valve still results in 0 * rate)
        return 0
    else:
        # need to compare stopping and opening, then moving on
        # to moving to each next value and calculating their downstream optimals
        comparisons = list()
        
        #account for turning this state on
        if node in states_check:
            next_states = copy(states)
            next_states[node] = True
            released_pressure = node.rate * (time_left - 1)
            comparisons.append(released_pressure + get_optimal_pressure(node, next_states, time_left - 1))
        
        #now account for moving to any next node
        for nn in node.next_nodes:
            comparisons.append(get_optimal_pressure(nn, states, time_left - 1))
        if states_node_tracker[(states,node)] < max(comparisons):
            states_node_tracker[(states,node)] = max(comparisons)
        
        return states_node_tracker[states]



def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    model = parse_data(data)
    answer = 0
    print(f"Puzzle1: <SUMMARY>: {answer}")
    answer = 0
    print(f"Puzzle2: <SUMMARY>: {answer}")
    
if __name__ == '__main__':
    main()