import sys
import os
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatusOptimal, PULP_CBC_CMD, value
from time import time
from itertools import combinations

def solve_mtz(n, distances, relax=False):
    problem = LpProblem("TSP", LpMinimize)
    cities = range(n)
    
    cat_type = 'Continuous' if relax else 'Binary'
    x = LpVariable.dicts("x", (cities, cities), lowBound=0, upBound=1, cat=cat_type)
    u = LpVariable.dicts("u", cities, lowBound=0, upBound=n-1, cat='Continuous')

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
    current = 0
    while len(tour) < n:
        tour.append(current)
        next_city = -1
        for j in cities:
            if current != j and x[current][j].varValue == 1:
                next_city = j
                break
        if next_city != -1:
            current = next_city
        else:
            break
    return value(problem.objective), tour, end_time - start_time, len(problem.variables()), len(problem.constraints)


def solve_dfj_enum(n, distances, relax=False):
    problem = LpProblem("TSP_DFJ", LpMinimize)
    cities = range(n)
    x = None
    if relax:
        x = LpVariable.dicts("x", (cities, cities), lowBound=0, upBound=1, cat='Continuous')
    else:
        x = LpVariable.dicts("x", (cities, cities), cat='Binary')
    problem += lpSum(distances[i][j] * x[i][j] for i in cities for j in cities)
    
    for i in range(n):
        problem += lpSum(x[i][j] for j in cities if j != i) == 1
        problem += lpSum(x[j][i] for j in cities if j != i) == 1

    for Q in range(2, n):
        subsets = combinations(cities, Q)
        for S in subsets:
            problem += lpSum(x[i][j] for i in S for j in S if i != j) <= len(S) - 1
    start_time = time()
    val = value(problem.objective) if problem.solve(PULP_CBC_CMD(msg=False)) == LpStatusOptimal else None
    end_time = time()
    tour = []
    current = 0
    while len(tour) < n:
        tour.append(current)
        next_city = -1
        for j in cities:
            if current != j and x[current][j].varValue > 0.9:
                next_city = j
                break
        if next_city != -1:
            current = next_city
        else:
                break
    return val, tour, end_time - start_time, len(problem.variables()), len(problem.constraints)

def solve_dfj_iter(n, distances):
    problem = LpProblem("TSP_DFJ_Iter", LpMinimize)
    cities = range(n)
    x = LpVariable.dicts("x", (cities, cities), cat='Binary')
    problem += lpSum(distances[i][j] * x[i][j] for i in cities for j in cities)
    
    for i in range(n):
        problem += lpSum(x[i][j] for j in cities if j != i) == 1
        problem += lpSum(x[j][i] for j in cities if j != i) == 1

    iters = 0
    solver_time = 0
    while True:
        iters += 1
        
        t_start = time()
        status = problem.solve(PULP_CBC_CMD(msg=False))
        solver_time += time() - t_start
        
        val = value(problem.objective) if status == LpStatusOptimal else None
        tour = [(i, j) for i in cities for j in cities if x[i][j].varValue == 1]
        
        cycles = get_subtours(x, n)
        if len(cycles) == 1 and len(cycles[0]) == n:
            val = value(problem.objective)
            tour = cycles[0]
            break
        
        for S in cycles:
            problem += lpSum(x[i][j] for i in S for j in S if i != j) <= len(S) - 1

    return val, tour, solver_time, iters, len(problem.variables()), len(problem.constraints)

def get_subtours(x, n):
    edges = {}
    for i in range(n):
        for j in range(n):
            if i != j and x[i][j].varValue == 1:
                edges[i] = j
    
    subtours = []
    visited = set()
    
    while len(visited) < n:
        current = -1
        for i in range(n):
            if i not in visited:
                current = i
                break
        
        if current == -1: 
            break
        
        cycle = []
        while current not in visited:
            visited.add(current)
            cycle.append(current)
            current = edges[current]
        
        subtours.append(cycle)
        
    return subtours


def read_instance(filename):
    if not filename.endswith(".txt"):
        filename = filename + ".txt"
    if not os.path.exists(filename):
         path = os.path.join("instances", filename)
    else:
         path = filename
         
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
        val, tour, t, vars, constr = solve_mtz(n, dists, relax=False)
        print_solution(val, tour, t, status="Optimal")  
    elif f == 1:
        val, tour, t, vars, constr = solve_mtz(n, dists, relax=True)
        print_solution(val, None, t, status="Relaxed")
    elif f == 2:
        val, tour, t, vars, constr = solve_dfj_enum(n, dists, relax=False)
        print_solution(val, tour, t, status="Optimal")
    elif f == 3:
        val, tour, t, vars, constr = solve_dfj_enum(n, dists, relax=True)
        print_solution(val, None, t, status="Relaxed")
    elif f == 4:
        val, tour, t, iters, vars, constr = solve_dfj_iter(n, dists)
        print_solution(val, tour, t, iters, status="Optimal")
    else:
        print("????")
