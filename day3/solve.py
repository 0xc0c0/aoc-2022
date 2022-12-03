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
    rucksacks = [(list(line[:len(line)//2]),list(line[len(line)//2:])) for line in text_data.strip('\n').strip().split('\n')]
    return rucksacks

def parse_data_no_breakup(text_data):
    return text_data.strip('\n').strip().split('\n')

def get_item_priority(item):
    if item.islower():
        return ord(item) - 96
    if item.isupper():
        return ord(item) - 38

def find_rucksack_shared_item(left, right):
    for leftitem in left:
        if leftitem in right:
            return leftitem
    return None

def get_priority_sum(rucksacks):
    sum = 0
    for rucksack in rucksacks:
        shared_item = find_rucksack_shared_item(*rucksack)
        sum += get_item_priority(shared_item)
    return sum

def get_elf_groups(rucksacks):
    elf_groups = [[list(y) for y in rucksacks[x:x+3]] for x in range(0, len(rucksacks), 3)]
    return elf_groups

def find_common_badge(elf1, elf2, elf3):
    for item in elf1:
        if item in elf2 and item in elf3:
            return item
    return None

def get_priority_sum_elf_groups(rucksacks):
    elf_groups = get_elf_groups(rucksacks)
    sum = 0
    for elf_group in elf_groups:
        badge = find_common_badge(*elf_group)
        sum += get_item_priority(badge)
    return sum

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    rucksacks = parse_data(data)
    answer = get_priority_sum(rucksacks)
    logger.info(f"Puzzle1: Rucksack Common Item on Each Side: {answer}")
    rucksacks = parse_data_no_breakup(data)
    answer = get_priority_sum_elf_groups(rucksacks)
    logger.info(f"Puzzle2: Badges Among Elf Groups: {answer}")
    
if __name__ == '__main__':
    main()