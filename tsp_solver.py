import sys
import os
from pulp import *
from time import time
from itertools import combinations

def solve_mtz(n, distances, relax=False):
    problem = LpProblem("TSP", LpMinimize)
    cities = range(n)
    
    cat_type = 'Continuous' if relax else 'Binary'
    x = pulp.LpVariable.dicts("x", (cities, cities), lowBound=0, upBound=1, cat=cat_type)
    u = pulp.LpVariable.dicts("u", cities, lowBound=0, upBound=n-1, cat='Continuous')

    problem += lpSum(distances[i][j] * x[i][j] for i in cities for j in cities if i != j)

    for i in cities:
        #garde fou
        problem += lpSum(x[i][j] for j in cities if i != j) == 1
        problem += lpSum(x[j][i] for j in cities if i != j) == 1

    for i in cities:
        for j in cities:
            if i != j and i != 0 and j != 0:
                problem += u[i] - u[j] + n * x[i][j] <= n - 1
                
    start_time = time()
    problem.solve(PULP_CBC_CMD(msg=False))
    end_time = time()

    tour = []
    for i in cities:
        for j in cities:
            if x[i][j].varValue == 1:
                tour.append((i, j))
    return problem.objective.value(), tour, end_time - start_time


def solve_dfj_enum(n, distances, relax=False):
    t0 = time()
    problem = LpProblem("TSP_DFJ", LpMinimize)
    cities = range(n)
    x = pulp.LpVariable.dicts("x", (cities, cities), cat='Binary')
    problem += lpSum(distances[i][j] * x[i][j] for i in cities for j in cities)
    
    for i in range(n):
        problem += lpSum(x[i][j] for j in cities if j != i) == 1
        problem += lpSum(x[j][i] for j in cities if j != i) == 1

    for Qx in range(2, n):
        subsets = combinations(cities, Qx)
        for S in subsets:
            problem += lpSum(x[i][j] for i in S for j in S if i != j) <= len(S) - 1

    val = value(problem.objective) if problem.solve(pulp.PULP_CBC_CMD(msg=False)) == LpStatusOptimal else None
    tour = [(i, j) for i in cities for j in cities if x[i][j].varValue == 1]
    t = time() - t0
    return val, tour, t

def solve_dfj_iter(n, distances):
    pass

def rid_of_cycles(x, n):
    return []






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

def print_solution(value_obj, tour, solve_time, iterations=None, status="Optimal"):
    print(f"Status: {status}")
    print(f"Objective: {value_obj}")
    if tour:
        tour_str = " -> ".join(str(i) for i in tour + [tour[0]])
        print(f"Tour: {tour_str}")
    print(f"Time: {solve_time:.4f} sec")
    if iterations is not None:
        print(f"Iterations: {iterations}")

    return tour



if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    
    filename = sys.argv[1]
    f = int(sys.argv[2])

    n, coords, dists = read_instance(filename)
    
    if f == 0:
        val, tour, t = solve_mtz(n, dists, relax=False)
        print_solution(val, tour, t, status="Optimal")
    elif f == 1:
        val, tour, t = solve_mtz(n, dists, relax=True)
        print_solution(val, None, t, status="Relaxed")
    elif f == 2:
        val, tour, t = solve_dfj_enum(n, dists, relax=False)
        print_solution(val, tour, t, status="Optimal")
    elif f == 3:
        val, tour, t = solve_dfj_enum(n, dists, relax=True)
        print_solution(val, None, t, status="Relaxed")
    elif f == 4:
        val, tour, t, iters = solve_dfj_iter(n, dists)
        print_solution(val, tour, t, iters, status="Optimal")
    else:
        print("????")
