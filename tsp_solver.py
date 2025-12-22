import sys
import os
from pulp import *
from time import time

def solve_mtz(n, distances, relax=False):
    pass

def solve_dfj_enum(n, distances, relax=False):
    pass


def solve_dfj_iter(n, distances):
    pass
    






def read_instance(filename):
    dir = "instances"
    if not filename.endswith(".txt"):
        filename = filename + ".txt"
    path = os.path.join(dir, filename)
    with open(path, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]
    
    try:
        n = int(lines[0])
        
        coords = []
        for i in range(n):
            parts = lines[1+i].split()
            coords.append((float(parts[0]), float(parts[1])))
            
        distances = []
        for i in range(n):
            parts = lines[1+n+i].split()
            distances.append([float(x) for x in parts])
            
        return n, coords, distances
    except Exception as e:
        print(f"Error reading instance: {e}")
        sys.exit(1)

def print_solution():
    pass



if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    
    filename = sys.argv[1]
    f = int(sys.argv[2])

    n, coords, dists = read_instance(filename)
    
    if f == 0:
        val, tour, t = solve_mtz(n, dists, relax=False)
        print_solution()
    elif f == 1:
        val, tour, t = solve_mtz(n, dists, relax=True)
        print_solution()
    elif f == 2:
        val, tour, t = solve_dfj_enum(n, dists, relax=False)
        print_solution()
    elif f == 3:
        val, tour, t = solve_dfj_enum(n, dists, relax=True)
        print_solution()
    elif f == 4:
        val, tour, t, iters = solve_dfj_iter(n, dists)
        print_solution()
    else:
        print("????")
