import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    pairs = [[[int(y) for y in x.split('-')] for x in line.strip().split(',')]
             for line in text_data.strip('\n').strip().split('\n')]
    return pairs

def check_full_containment(range1, range2):
    lower1, upper1 = range1
    lower2, upper2 = range2
    if (upper1 - lower1) >= (upper2 - lower2):
        #test range1 for outer boundedness
        if lower2 >= lower1 and upper2 <= upper1:
            return True
    else:
        #test range1 for outer boundedness
        if lower1 >= lower2 and upper1 <= upper2:
            return True
    return False

def check_overlapping(range1, range2):
    lower1, upper1 = range1
    lower2, upper2 = range2
    if lower1 <= lower2:
        # we use lower1 as outer edge
        if lower2 <= upper1:
            return True
    else:
        # we use lower2 as outer edge
        if lower1 <= upper2:
            return True
    return False

def count_contained_pairs(pairs):
    return sum([check_full_containment(*p) for p in pairs])

def count_overlapping_pairs(pairs):
    return sum([check_overlapping(*p) for p in pairs])

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    pairs = parse_data(data)
    answer = count_contained_pairs(pairs)
    logger.info(f"Puzzle1: Contained Pairs: {answer}")
    answer = count_overlapping_pairs(pairs)
    logger.info(f"Puzzle2: Overlapping Pairs: {answer}")
    
if __name__ == '__main__':
    main()