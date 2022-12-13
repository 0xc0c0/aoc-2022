import logging
import os
import numpy as np
import copy

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    pairs = [[eval(x) for x in pair.split('\n')] for pair in text_data.strip('\n').strip().split('\n\n')]
    return pairs

def is_ordered(left_packet, right_packet):
    logger.debug(f"comparing {left_packet} to {right_packet}")
    left_packet = copy.deepcopy(left_packet)
    right_packet = copy.deepcopy(right_packet)
    if type(left_packet) == int and type(right_packet) == int:
        if left_packet < right_packet:
            return True
        if left_packet == right_packet:
            return None
        if left_packet > right_packet:
            return False
    
    # not both ints, process next level deep
    
    # first adjust for mismatched types (int vs. list)
    if type(left_packet) == int:
        left_packet = [left_packet]
    if type(right_packet) == int:
        right_packet = [right_packet]

    # now guaranteed to be lists of something:
    while left_packet and right_packet:
        l = left_packet.pop(0)
        r = right_packet.pop(0)
        status = is_ordered(l,r)
        if status == True:
            return True
        if status == False:
            return False
    
    # check whether we continue processing or stop now due to items still remaining in left or right packet
    if len(left_packet) == len(right_packet):
        return None
    if left_packet:
        return False
    if right_packet:
        return True

def get_ordered_pairs_indices(pairs):
    ordered = list()
    pairs = copy.deepcopy(pairs)
    for i, pair in enumerate(pairs):
        status = is_ordered(*pair)
        if status == True or status == None:
            logger.debug(f"Pair {i+1} is ordered")
            ordered.append(i+1)
    return ordered

def insert_ordered(ol_packets,candidate_packet):
    if len(ol_packets) == 0:
        logger.debug(f"appending {candidate_packet}")
        ol_packets.append(candidate_packet)
    else:
        for i,list_packet in enumerate(ol_packets):
            status = is_ordered(candidate_packet, list_packet)
            status = True if None else status
            if status == True:
                logger.debug(f"inserting {candidate_packet} at index {i}")
                ol_packets.insert(i, candidate_packet)
                return
        logger.debug(f"appending {candidate_packet}")
        ol_packets.append(candidate_packet)
        return

def get_ordered_packets(pairs):
    ordered_packets = list()
    all_packets = [p for pair in copy.deepcopy(pairs) for p in pair]
    all_packets.append([[2]])
    all_packets.append([[6]])
    logger.debug(f"all packets: {all_packets}")
    while all_packets:
        p = all_packets.pop(0)
        insert_ordered(ordered_packets, p)
    logger.debug(f"ordered packets: {ordered_packets}")
    return ordered_packets    

def get_decoder_key(ordered_packets):
    i1 = ordered_packets.index([[2]])
    i2 = ordered_packets.index([[6]])
    return (i1 + 1) * (i2 + 1)

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    pairs = parse_data(data)
    answer = sum(get_ordered_pairs_indices(pairs))
    print(f"Puzzle1: Find All Ordered Pairs: {answer}")
    ordered_packets = get_ordered_packets(pairs)
    answer = get_decoder_key(ordered_packets)
    print(f"Puzzle2: Obtain Decoder Key: {answer}")
    
if __name__ == '__main__':
    main()