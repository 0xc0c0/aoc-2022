import logging
import os
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def get_rock_points(rock_line):
    rock_points = set()
    for i in range(len(rock_line)-1):
        x0,y0 = rock_line[i]
        x1,y1 = rock_line[i+1]
        if x0 == x1:
            direction = np.sign(y1-y0)
            for y in range(y0,y1 + direction,direction):
                rock_points.add((x0,y))
        elif y0 == y1:
            direction = np.sign(x1-x0)
            for x in range(x0,x1 + direction,direction):
                rock_points.add((x,y0))
        else:
            return None
    return rock_points

def get_all_rock_points(rock_lines):
    rock_points = set()
    for rock_line in rock_lines:
        rp = get_rock_points(rock_line)
        rock_points = rock_points.union(rp)
    return rock_points

def parse_data(text_data):
    rock_lines = [[[int(y) for y in x.split(',')] for x in line.strip().split(' -> ')] for line in text_data.strip('\n').strip().split('\n')]
    return rock_lines

def add_points(a,b):
    return tuple(map(lambda i, j: i + j, a, b))

def sand_fall_step(all_points, cur_point):
    checks = ((0,1),(-1,1),(1,1))
    for check_diff in checks:       
        check_point = add_points(cur_point, check_diff)
        if not check_point in all_points:
            return check_point
    return cur_point

def sand_fall(rock_points, sand_points, check_infinity):
    cur_point = (500, 0)
    all_points = rock_points.union(sand_points)
    last_point = None
    while last_point != cur_point:
        last_point = cur_point
        # logger.debug(f"cur_point: {cur_point}, last_point: {last_point}")
        if check_infinity:
            points_underneath = set([p for p in all_points if p[0] == cur_point[0] and p[1] >= cur_point[1]])
            # logger.debug(f"check_infinite == {points_underneath}")
            if points_underneath == set():
                raise ValueError(f"Infinity has been identified at point {cur_point}")
        cur_point = sand_fall_step(all_points, cur_point)
    return cur_point

def get_all_sand_points(rock_points, check_infinity=True):
    sand_points = set()
    while (500,0) not in sand_points:
        try:
            new_sand_point = sand_fall(rock_points, sand_points, check_infinity)
            logger.debug(f"sand point added at: {new_sand_point}")
            sand_points.add(new_sand_point)
            # if len(sand_points) % 100 == 0:
                # logger.info(f"total sand points at {len(sand_points)}")
        except ValueError as e:
            logger.info(e)
            break
    return sand_points

def add_floor(rock_points):
    floor_depth = max([p[1] for p in rock_points]) + 2
    needed_floor_min = 500 - (floor_depth + 10)
    needed_floor_max = 500 + (floor_depth + 10)
    # logger.info(f"floor depth is: {floor_depth}")
    floor_rock_points = set([(x,floor_depth) for x in range(needed_floor_min,needed_floor_max + 1)])
    # logger.info(f"floor is: [{min(floor_rock_points)}, {max(floor_rock_points)}]")
    return rock_points.union(floor_rock_points)

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    rock_lines = parse_data(data)
    rp = get_all_rock_points(rock_lines)
    sp = get_all_sand_points(rp)
    answer = len(sp)
    print(f"Puzzle1: <SUMMARY>: {answer}")
    rp2 = add_floor(rp)
    sp2 = get_all_sand_points(rp2, check_infinity=False)
    answer = len(sp2)
    print(f"Puzzle2: <SUMMARY>: {answer}")
    
if __name__ == '__main__':
    main()