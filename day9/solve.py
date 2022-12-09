import logging
import os
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

COL_I = 1
ROW_I = 0

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    motions = [line.strip().split() for line in text_data.strip('\n').strip().split('\n')]
    motions = [[entry[0], int(entry[1])] for entry in motions]
    return motions

def is_far_distance(head_loc, tail_loc):
    d2 = (head_loc[ROW_I] - tail_loc[ROW_I]) ** 2 + (head_loc[COL_I] - tail_loc[COL_I]) ** 2
    return d2 > 2

def get_distance_sq(loc1, loc2):
    d2 = (loc1[ROW_I] - loc2[ROW_I]) ** 2 + (loc1[COL_I] - loc2[COL_I]) ** 2
    return d2

def move(dir, head_loc, tail_loc):
    if dir == 'R':
        head_loc[COL_I] += 1
        if is_far_distance(head_loc, tail_loc):
            tail_loc[COL_I] += 1
            tail_loc[ROW_I] = head_loc[ROW_I]
    elif dir == 'L':
        head_loc[COL_I] -= 1
        if is_far_distance(head_loc, tail_loc):
            tail_loc[COL_I] -= 1
            tail_loc[ROW_I] = head_loc[ROW_I]
    elif dir == 'U':
        head_loc[ROW_I] += 1
        if is_far_distance(head_loc, tail_loc):
            tail_loc[ROW_I] += 1
            tail_loc[COL_I] = head_loc[COL_I]
    elif dir == 'D':
        head_loc[ROW_I] -= 1
        if is_far_distance(head_loc, tail_loc):
            tail_loc[ROW_I] -= 1
            tail_loc[COL_I] = head_loc[COL_I]
    else:
        return None
    return head_loc, tail_loc

def get_vector(loc1, loc2):
    loc1 - loc2

def move_bigger(dir, knots_loc):
    knots_loc = np.array(knots_loc)
    if dir == 'R':
        knots_loc[0][COL_I] += 1
    elif dir == 'L':
        knots_loc[0][COL_I] -= 1
    elif dir == 'U':
        knots_loc[0][ROW_I] += 1
    elif dir == 'D':
        knots_loc[0][ROW_I] -= 1
        
    for i in range(1,10):
        if is_far_distance(knots_loc[i-1], knots_loc[i]):
            if get_distance_sq(knots_loc[i-1], knots_loc[i]) == 4:
                # in line, follow vector, no change in vector to follow.
                # move 1 unit (not 2) toward lead knot.
                knots_loc[i] += (knots_loc[i-1] - knots_loc[i])//2
                
            else:
                #diagonal, need to work from the bigger part of the distance
                total_d = knots_loc[i-1] - knots_loc[i]
                knots_loc[i] += np.sign(total_d)

    return knots_loc

def count_tail_motions(motions):
    head_loc = [0,0]
    tail_loc = [0,0]
    all_tail_visits = set()
    all_tail_visits.add(tuple(tail_loc))
    for dir, distance in motions:
        for i in range(distance):
            head_loc, tail_loc = move(dir, head_loc, tail_loc)
            all_tail_visits.add(tuple(tail_loc))
    # print(all_tail_visits)
    return len(all_tail_visits)

def count_bigger_tail_motions(motions):
    knots_loc = np.array([[0,0]]*10)
    all_9_visits = set()
    all_9_visits.add(tuple(knots_loc[-1]))
    for dir, distance in motions:
        for i in range(distance):
            # print(knots_loc)
            knots_loc = move_bigger(dir, knots_loc)
            all_9_visits.add(tuple(knots_loc[-1]))
    # print(all_9_visits)
    return len(all_9_visits)
    

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    motions = parse_data(data)
    answer = count_tail_motions(motions)
    print(f"Puzzle1: Unique Spots Visited by Tail (2 knots): {answer}")
    answer = count_bigger_tail_motions(motions)
    print(f"Puzzle2: Unique Spots Visited by Tail (10 knots): {answer}")
    
if __name__ == '__main__':
    main()