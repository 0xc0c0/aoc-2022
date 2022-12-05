import logging
import os
import re

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_stacks(text_stacks):
    lines = text_stacks.rstrip().split('\n')
    stack_labels = [int(x) for x in lines[-1].strip().split()]
    num_rows = (len(lines) - 1)
    row_entries = [[lines[i][j:j+4].strip() for j in range(0,len(lines[i]),4)] for i in range(num_rows-1, -1, -1)]
    
    box_stacks = {k:[] for k in stack_labels}
    for row in row_entries:
        for i,box in enumerate(row):
            if len(box) >= 3:
                letter = box.rstrip(']').lstrip('[')
                box_stacks[stack_labels[i]].append(letter)
    return box_stacks

def parse_moves(text_moves):
    regex = 'move ([0-9]+) from ([0-9]+) to ([0-9]+)'
    results = re.findall(regex, text_moves)
    return [[int(x) for x in result] for result in results]

def parse_data(text_data):
    text_stacks, text_moves = text_data.strip('\n').rstrip().split('\n\n')
    return parse_stacks(text_stacks), parse_moves(text_moves)

def move(stacks, num, src, dst):
    for n in range(num):
        letter = stacks[src].pop()
        stacks[dst].append(letter)

def move_part2(stacks, num, src, dst):
    tmp_stack = []
    for n in range(num):
        letter = stacks[src].pop()
        tmp_stack.append(letter)
    
    for n in range(num):
        letter = tmp_stack.pop()
        stacks[dst].append(letter)

def complete_moves(stacks, moves):
    for (num,src,dst) in moves:
        move(stacks, num, src, dst)
    return stacks

def complete_moves_part2(stacks, moves):
    for (num,src,dst) in moves:
        move_part2(stacks, num, src, dst)
    return stacks

def get_tops(stacks):
    return ''.join([stacks[k][-1] for k in stacks.keys()])

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    stacks, moves = parse_data(data)
    complete_moves(stacks, moves)
    answer = get_tops(stacks)
    logger.info(f"Puzzle1: Complete all moves one box at a time, tops of stacks are: {answer}")
    stacks, moves = parse_data(data)
    complete_moves_part2(stacks, moves)
    answer = get_tops(stacks)
    logger.info(f"Puzzle2: Complete all moves multiple boxes at a time, tops of stacks are: {answer}")
    
if __name__ == '__main__':
    main()