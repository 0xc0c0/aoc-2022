import logging
import os
import re
import numpy as np
import math

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def get_mhd(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

def parse_data(text_data):
    regex_expr = "Sensor at x=([-,0-9]+), y=([-,0-9]+): closest beacon is at x=([-,0-9]+), y=([-,0-9]+)"
    data = re.findall(regex_expr, text_data)
    sensors = list()
    beacons = list()
    for b_x, b_y, s_x, s_y in data:
        b = (int(b_x), int(b_y))
        s = (int(s_x), int(s_y))
        d = get_mhd(b,s)
        sensors.append({'loc': b, 'dist': d})
        beacons.append(s)
    sensors = sorted(sensors, key=lambda s:s['loc'][0])
    beacons = sorted(beacons)
    return sensors, beacons

def get_impossible_x_ranges_y_intercept(sensor, y_0):
    line_dist = abs(sensor['loc'][1] - y_0)
    horizon_residual_mhd = sensor['dist'] - line_dist
    if horizon_residual_mhd >= 0:
        return (sensor['loc'][0] - horizon_residual_mhd, sensor['loc'][0] + horizon_residual_mhd)
    else:
        return None        

def get_all_impossible_x_ranges_y_intercept(sensors, y_0):
    all_ranges = list()
    for sensor in sensors:
        new_range = get_impossible_x_ranges_y_intercept(sensor, y_0)
        if new_range:
            logger.debug(f"for sensor at {sensor['loc']}, added range: {new_range}")
            all_ranges.append(new_range)
    all_ranges = reduce_ranges(all_ranges)
    return all_ranges

def get_all_impossible_points_y_intercept(all_ranges, beacons, y_0):
    all_points = set()
    for r in all_ranges:
        for x in range(min(r), max(r) + 1):
            p = (x, y_0)
            if p not in beacons:
                all_points.add((x,y_0))
    return all_points

def reduce_ranges(all_ranges):
    ranges = sorted(all_ranges)
    i = 0
    while i < (len(ranges) - 1):
        #if ranges i overlaps with next range
        if ranges[i][1] > ranges[i+1][0]:
            #combine two entries
            larger_end = max(ranges[i][1],ranges[i+1][1])
            ranges[i] = (ranges[i][0], larger_end)
            ranges.pop(i+1)
        else:
            i += 1
    return ranges

def get_uncovered_x(ranges, xlim):
    x_covered = -1
    for r in ranges:
        # update the covered low end of check
        if min(r) <= x_covered and max(r) > x_covered:
            x_covered = max(r)
        if x_covered > xlim:
            return None
    return x_covered + 1

def get_unaccounted_point(sensors, axis_lim):
    for y in range(0,axis_lim + 1):
        all_ranges = get_all_impossible_x_ranges_y_intercept(sensors, y)
        uncovered_x = get_uncovered_x(all_ranges, axis_lim)
        if uncovered_x:
            return (uncovered_x, y)
    return None
       
def get_tuning_freq(sensors, axis_lim):
    x = get_unaccounted_point(sensors, axis_lim)
    return x[0] * 4000000 + x[1]

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    sensors, beacons = parse_data(data)
    all_ranges = get_all_impossible_x_ranges_y_intercept(sensors, y_0=2000000)
    all_points = get_all_impossible_points_y_intercept(all_ranges, beacons, y_0=2000000)
    answer = len(all_points)
    print(f"Puzzle1: <SUMMARY>: {answer}")
    answer = get_tuning_freq(sensors, 4000000)
    print(f"Puzzle2: <SUMMARY>: {answer}")
    
if __name__ == '__main__':
    main()