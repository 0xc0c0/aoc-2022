import logging
import os
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    lines = text_data.strip('\n').strip().split('\n')
    instructions = list()
    for line in lines:
        # print(line)
        line = line.strip().split()
        instruction = {'op': line[0]}
        if len(line) == 2:
            instruction['arg'] = int(line[1])
        instructions.append(instruction)
        
    return instructions

def run_instruction(instruction, cycle_values):
    if len(cycle_values) == 0:
        cur_value = 1
    else:
        cur_value = cycle_values[-1]

    cycle_values.append(cur_value)  #in any case, one cycle gets the same value
    if instruction['op'] == 'noop':
        pass
    elif instruction['op'] == 'addx':
        cycle_values.append(cur_value + instruction['arg'])
    return cycle_values

def run_instructions(instructions):
    cycle_values = [1]
    for instruction in instructions:
        cycle_values = run_instruction(instruction, cycle_values)
    return cycle_values

def get_signal_strengths(cycle_values, signal_indices):
    # print(cycle_values)
    total = 0
    for i in signal_indices:
        total += (i) * (cycle_values[i-1])
    return total

def render_sprite(cycle_values):
    CRT = ['.'] * 240
    for i in range(240):
        # note: nth cycle means i + 1
        if (cycle_values[i] - 1) <= (i % 40) <= (cycle_values[i] + 1):
            CRT[i] = '#'
    for i in range(0,240, 40):
        print(f"{''.join(CRT[i:i+40])}")

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    instructions = parse_data(data)
    cycle_values = run_instructions(instructions)
    answer = get_signal_strengths(cycle_values, [20,60,100,140,180,220])
    print(f"Puzzle1: Strengths: {answer}")
    print(f"Puzzle2: Rendered Image Shown Below (8 capital letters):")
    render_sprite(cycle_values)
    
if __name__ == '__main__':
    main()