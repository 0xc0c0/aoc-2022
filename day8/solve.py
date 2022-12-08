import logging
import os
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def count_visible(tree_heights):
    rows, cols = tree_heights.shape
    visible_trees = np.zeros(tree_heights.shape, dtype=bool, order='C')
    
    #handle edges
    for r in range(rows):
        #looking from the left-side
        heighest_previous_tree = -1
        for c in range(cols):
            if tree_heights[r][c] > heighest_previous_tree:
                visible_trees[r][c] = True
                heighest_previous_tree = tree_heights[r][c]
            if heighest_previous_tree == 9:
                break
        
        #looking from the right-side
        heighest_previous_tree = -1
        for c in range(cols-1, -1, -1):
            if tree_heights[r][c] > heighest_previous_tree:
                visible_trees[r][c] = True
                heighest_previous_tree = tree_heights[r][c]
            if heighest_previous_tree == 9:
                break
    
    for c in range(cols):
        #looking from the top
        heighest_previous_tree = -1
        for r in range(rows):
            if tree_heights[r][c] > heighest_previous_tree:
                visible_trees[r][c] = True
                heighest_previous_tree = tree_heights[r][c]
            if heighest_previous_tree == 9:
                break
        
        #looking from the bottom
        heighest_previous_tree = -1
        for r in range(rows-1, -1, -1):
            if tree_heights[r][c] > heighest_previous_tree:
                visible_trees[r][c] = True
                heighest_previous_tree = tree_heights[r][c]
            if heighest_previous_tree == 9:
                break
    
    
    return np.sum(visible_trees == True)

def get_max_scenic_score(tree_heights):
    rows, cols = tree_heights.shape
    scenic_scores = np.zeros(tree_heights.shape, dtype=int, order='C')
    for (row,col), _ in np.ndenumerate(scenic_scores):
        max_height = tree_heights[row][col]
        scenic_score = 1
        
        #look left
        count = 0
        tallest_seen = -1
        for c in range(col-1, -1, -1):
            count += 1
            if tree_heights[row][c] >= max_height:
                break
        scenic_score *= count

        #look right
        count = 0
        tallest_seen = -1
        for c in range(col+1, cols, 1):
            count += 1
            if tree_heights[row][c] >= max_height:
                break
        scenic_score *= count

        #look up
        count = 0
        tallest_seen = -1
        for r in range(row-1, -1, -1):
            count += 1
            if tree_heights[r][col] >= max_height:
                break
        scenic_score *= count

        #look down
        count = 0
        for r in range(row+1, rows, 1):
            count += 1
            if tree_heights[r][col] >= max_height:
                break
        scenic_score *= count
        scenic_scores[row][col] = scenic_score
    logger.debug(scenic_scores)
    return np.amax(scenic_scores)
        
def parse_data(text_data):
    heights = [[int(x) for x in list(line)] for line in text_data.strip('\n').strip().split('\n')]
    heights = np.array(heights)
    logger.debug(heights)
    return heights

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    trees = parse_data(data)
    answer = count_visible(trees)
    print(f"Puzzle1: <SUMMARY>: {answer}")
    answer = get_max_scenic_score(trees)
    print(f"Puzzle2: <SUMMARY>: {answer}")
    
if __name__ == '__main__':
    main()