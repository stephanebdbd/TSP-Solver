import sys
import os
from pulp import *
from time import time

def solve_mtz(n, distances, relax=False):
    t0 = time()
    problem = LpProblem("TSP", LpMinimize)
    cities = range(n)
    x = pulp.LpVariable.dicts("x", (cities, cities), cat='Binary')
    u = pulp.LpVariable.dicts("u", cities, lowBound=0, upBound=n-1, cat='Continuous')
    
    problem += lpSum(distances[i][j] * x[i][j] for i in cities for j in cities if i != j)
    
    for i in cities:
        for j in cities:
            if i != j and i != 0 and j != 0:
                problem += u[i] - u[j] + (n-1)*x[i][j] <= n-2
    
    cycle = problem.solve()

def solve_dfj_enum(n, distances, relax=False):
    pass


def solve_dfj_iter(n, distances):
    pass

def rid_of_cycles(x, n):
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
