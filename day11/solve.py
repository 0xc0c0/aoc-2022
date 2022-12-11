import logging
import os
import re
from dataclasses import dataclass
from typing import List
import operator

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

class MonkeyNote():
    items: List[int] = list()
    total_inspected: int = 0
    number: int = -1
    test_modulo: int = -1
    true_monkey: int = -1
    false_monkey: int = -1
    monkey_op = None
    
    def __init__(self, monkey_note_text):
        self.parse_monkey_note(monkey_note_text)

    def __str__(self):
        s = list()
        s.append(f"items: {self.items}")
        s.append(f"number: {self.number}")
        s.append(f"total_inspected: {self.total_inspected}")
        s.append(f"test_modulo: {self.test_modulo}")
        s.append(f"true_monkey: {self.true_monkey}")
        s.append(f"false_monkey: {self.false_monkey}")
        s.append(f"monkey_op: {self.monkey_op}")
        return '\n'.join(s)
    
    def __repr__(self):
        return self.__str__()
    
    def parse_monkey_note(self, monkey_note_text):
        lines = monkey_note_text.strip().split('\n')
        self.number = int(re.findall('Monkey ([0-9]+)', lines[0].strip())[0])
        if lines[1].strip().startswith('Starting items'):
            self.items = [int(x) for x in re.findall('[0-9]+', lines[1])]
        else:
            raise ValueError(f"Problem with Starting Items")

        self.parse_operation_fn(lines[2].strip())

        if lines[3].strip().startswith('Test: divisible'):
            self.test_modulo = int(re.findall('[0-9]+', lines[3])[0])
        else:
            raise ValueError(f"Problem with Test statement")
        if lines[4].strip().startswith('If true'):
            v = int(re.findall('[0-9]+', lines[4])[0])
            logger.debug(f"Monkey {self.number} has true Monkey toss set to monkey {v}")
            self.true_monkey = v
        else:
            raise ValueError(f"Problem with If True statement")
        if lines[5].strip().startswith('If false'):
            v = int(re.findall('[0-9]+', lines[5])[0])
            logger.debug(f"Monkey {self.number} has false Monkey toss set to monkey {v}")
            self.false_monkey = v
        else:
            raise ValueError(f"Problem with If False statement")

    def parse_operation_fn(self, operation_text):
        op_text, arg_text = re.findall('Operation: new = old (.) ([0-9]+|old)', operation_text)[0]
        if op_text == '*':
            op_fn = operator.mul
        elif op_text == '+':
            op_fn = operator.add
        
        if arg_text == 'old': 
            def monkey_op(item_value: int):
                new_value = op_fn(item_value, item_value)
                return new_value
            self.monkey_op = monkey_op
        else:
            arg = int(arg_text)
            def monkey_op(item_value: int):
                new_value = op_fn(item_value, arg)
                return new_value
            self.monkey_op = monkey_op
        
    def inspect_item(self, item_value):
        logger.debug(f"Monkey {self.number} old inspection count: {self.total_inspected}")
        logger.debug(f"Monkey {self.number} old value: {item_value}")
        if not self.monkey_op:
            logger.warning(f"Problem with monkey_op")
            return None
        if item_value not in self.items:
            logger.warning(f"Problem with item_value during inspection")
            return None
        self.total_inspected += 1
        logger.debug(f"Monkey {self.number} new inspection count: {self.total_inspected}")
        new_value = self.monkey_op(item_value)
        return new_value
    
    def check_divisible(self, item_value):
        return item_value % self.test_modulo == 0

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    monkey_notes = [MonkeyNote(block) for block in text_data.strip('\n').strip().split('\n\n')]
    for i,mn in enumerate(monkey_notes):
        if i != mn.number:
            print(f"Problem with Monkey number ordering:  {i} {mn.number}") 
    return monkey_notes

def run_round(monkey_notes: List[MonkeyNote]):
    for mn in monkey_notes:
        logger.debug(f"running round on monkey {mn.number}")
        logger.debug(mn)
        for old_value in mn.items:
            new_value = mn.inspect_item(old_value)
            new_value = new_value // 3
            if mn.check_divisible(new_value):
                logger.debug(f"appending {new_value} to Monkey {mn.true_monkey}")
                monkey_notes[mn.true_monkey].items.append(new_value)
            else:
                logger.debug(f"appending {new_value} to Monkey {mn.false_monkey}")
                monkey_notes[mn.false_monkey].items.append(new_value)
        mn.items = list()

def run_round_2(monkey_notes: List[MonkeyNote], divisor_check = 1):
    for mn in monkey_notes:
        logger.debug(f"running round on monkey {mn.number}")
        logger.debug(mn)
        for old_value in mn.items:
            new_value = mn.inspect_item(old_value)
            new_value = new_value % divisor_check
            if mn.check_divisible(new_value):
                logger.debug(f"appending {new_value} to Monkey {mn.true_monkey}")
                monkey_notes[mn.true_monkey].items.append(new_value)
            else:
                logger.debug(f"appending {new_value} to Monkey {mn.false_monkey}")
                monkey_notes[mn.false_monkey].items.append(new_value)
        mn.items = list()

def run_rounds(monkey_notes: List[MonkeyNote], count: int = 20):
    for r in range(count):
        logger.debug(f"running round {r}")
        run_round(monkey_notes)

def get_gcm(monkey_notes):
    gcm = 1
    for mn in monkey_notes:
        gcm *= mn.test_modulo
    return gcm

def run_rounds_2(monkey_notes: List[MonkeyNote], count: int):
    for r in range(count):
        logger.debug(f"running round {r}")
        run_round_2(monkey_notes, divisor_check=get_gcm(monkey_notes))



def get_monkey_business(monkey_notes: List[MonkeyNote]):
    all_counts = [mn.total_inspected for mn in monkey_notes]
    all_counts.sort(reverse=True)
    return all_counts[0] * all_counts[1]

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    monkey_notes = parse_data(data)
    run_rounds(monkey_notes)
    answer = get_monkey_business(monkey_notes)
    print(f"Puzzle1: Monkey Business after 20 rounds with worry reduction: {answer}")
    monkey_notes = parse_data(data)
    run_rounds_2(monkey_notes, 10000)
    answer = get_monkey_business(monkey_notes)
    print(f"Puzzle2: Monkey Business after 20 rounds without worry reduction: {answer}")

if __name__ == '__main__':
    main()