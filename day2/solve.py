import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    rounds = [line.strip().split() for line in text_data.strip('\n').strip().split('\n')]
    return rounds
    
def score_round(opponent_throw, our_throw):
    #use ASCII math to calculate throw value (1 for X, 2 for Y, etc.)
    throw_value = ord(our_throw) - ord('W')
    
    scored_value = 0
    if opponent_throw == 'A':
        if our_throw == 'X':
            scored_value = 3
        if our_throw == 'Y':
            scored_value = 6
        if our_throw == 'Z':
            scored_value = 0
    elif opponent_throw == 'B':
        if our_throw == 'X':
            scored_value = 0
        if our_throw == 'Y':
            scored_value = 3
        if our_throw == 'Z':
            scored_value = 6
    elif opponent_throw == 'C':
        if our_throw == 'X':
            scored_value = 6
        if our_throw == 'Y':
            scored_value = 0
        if our_throw == 'Z':
            scored_value = 3
    else:
        return None
    return throw_value + scored_value

def score_strategy(opponent_throw, objective):
    #use ASCII math to calculate scored value (0 for X, 3 for Y, etc.)
    scored_value = (ord(objective) - ord('X')) * 3
    
    throw_value = 'Q'
    if opponent_throw == 'A':
        if objective == 'X':
            throw_value = 3
        if objective == 'Y':
            throw_value = 1
        if objective == 'Z':
            throw_value = 2
    elif opponent_throw == 'B':
        if objective == 'X':
            throw_value = 1
        if objective == 'Y':
            throw_value = 2
        if objective == 'Z':
            throw_value = 3
    elif opponent_throw == 'C':
        if objective == 'X':
            throw_value = 2
        if objective == 'Y':
            throw_value = 3
        if objective == 'Z':
            throw_value = 1
    else:
        return None
    return scored_value + throw_value

def score_all_rounds(rounds):
    return sum([score_round(*round) for round in rounds])

def score_all_strategy(rounds):
    return sum([score_strategy(*round) for round in rounds])

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    rounds = parse_data(data)
    answer = score_all_rounds(rounds)
    logger.info(f"Puzzle1: Total Score of Rounds: {answer}")
    answer = score_all_strategy(rounds)
    logger.info(f"Puzzle2: Total Strategy Score: {answer}")
    
if __name__ == '__main__':
    main()