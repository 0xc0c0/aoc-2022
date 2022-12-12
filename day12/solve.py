import logging
import os
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def translate(c):
    if c == 'S':
        return 0
    if c == 'E':
        return 27
    else:
        return ord(c) - 96

def init(heights):
    start_pt = np.where(heights == 0)
    heights[start_pt] = 0
    end_pt = np.where(heights == 27)
    heights[end_pt] = 26
    return heights, start_pt, end_pt

def parse_data(text_data):
    heights = [[translate(c) for c in list(line.strip())] for line in text_data.strip('\n').strip().split('\n')]
    heights = np.array(heights)
    return init(heights)

def move(heights:np.ndarray, best_paths:np.ndarray, cur_pt, end_pt, cur_steps):
    next_tasks = list()
    if cur_pt == end_pt:
        return next_tasks
    x0, y0 = cur_pt
    xmax, ymax = heights.shape
    attempts = [(0,-1),(0,1),(-1,0),(1,0)]
    if x0 == 0:
        attempts.remove((-1,0))
    if x0 == xmax - 1:
        attempts.remove((1,0))
    if y0 == 0:
        attempts.remove((0,-1))
    if y0 == ymax - 1:
        attempts.remove((0,1))
        
    for attempt in attempts:
        new_pt = tuple(map(sum, zip(cur_pt, attempt)))
        if heights[new_pt] <= heights[cur_pt] + 1:
            if best_paths[new_pt] == -1 or best_paths[new_pt] > cur_steps + 1:
                best_paths[new_pt] = cur_steps + 1
                next_tasks.append((new_pt, cur_steps + 1))
                # move(heights, best_paths, new_pt, end_pt, cur_steps + 1)
    return next_tasks

def run_moves(heights, start, end):
    best = np.zeros(heights.shape, dtype=int)
    best[best == 0] = -1
    
    deferred_moves = [(start,0)]
    while deferred_moves:
        cur_pt, cur_steps = deferred_moves.pop(0)
        next_tasks = move(heights, best, cur_pt, end, cur_steps)
        logger.debug(f"next_tasks: {next_tasks}")
        for nt in next_tasks:
            deferred_moves.append(nt)
    return best

def find_fastest_starting_point(heights, end):
    starting_points = list(zip(*np.where(heights == 1)))
    logger.debug(f"there are {len(starting_points)} possible starting points")
    fewest_steps = 0
    for i,s in enumerate(starting_points):
        logger.debug(f"running {i+1} out of {len(starting_points)}")
        best = run_moves(heights, s, end)
        if best[end] != -1 and (fewest_steps == 0 or (best[end] < fewest_steps)):
            fewest_steps = best[end]
    return fewest_steps

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    heights, start, end = parse_data(data)
    best = run_moves(heights, start, end)
    answer = best[end]
    print(f"Puzzle1: Shortest Path from Starting Point to End/Peak: {answer}")
    answer = find_fastest_starting_point(heights, end)
    print(f"Puzzle2: Shortest Path from Any 'a' point to End/Peak: {answer}")
    
if __name__ == '__main__':
    main()