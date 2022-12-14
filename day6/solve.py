import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    return list(text_data.strip('\n').strip())

def find_first_x_unique(chars, num_uniq):
    for i in range(num_uniq, len(chars), 1):
        if len(set(chars[i-num_uniq+1:i+1])) == num_uniq:
            return i+1

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    chars = parse_data(data)
    answer = find_first_x_unique(chars, 4)
    logger.info(f"Puzzle1: <SUMMARY>: {answer}")
    answer = find_first_x_unique(chars, 14)
    logger.info(f"Puzzle2: <SUMMARY>: {answer}")
    
if __name__ == '__main__':
    main()