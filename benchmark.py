import os
import csv
import time
from tsp_solver import read_instance, solve_mtz, solve_dfj_enum, solve_dfj_iter

INSTANCES_DIR = "instances"
OUTPUT_FILE = "results.csv"

def run_benchmark():
    header = ["instance", "formulation", "obj_int", "time_int", "obj_relax", "time_relax", "gap", "vars", "constr"]
    
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        
        files = sorted([f for f in os.listdir(INSTANCES_DIR) if f.endswith(".txt")])
        
        for filename in files:
            instance_name = filename.replace(".txt", "")
            print(f"Processing {instance_name}...")
            
            try:
                n, coords, dists = read_instance(os.path.join(INSTANCES_DIR, filename))
            except:
                print(f"Skipping {filename} (read error)")
                continue

            print(f"  - MTZ...")
            obj_relax, _, time_relax, _, _ = solve_mtz(n, dists, relax=True)
            obj_int, _, time_int, n_vars, n_constr = solve_mtz(n, dists, relax=False)
            
            gap = (obj_int - obj_relax) / obj_int if obj_int else 0
            writer.writerow([instance_name, "MTZ", rounded(obj_int), rounded(time_int), rounded(obj_relax), rounded(time_relax), rounded(gap, 4), n_vars, n_constr])
            csvfile.flush()

            if n <= 15:
                print(f"  - DFJ Enum...")
                obj_relax, _, time_relax, _, _ = solve_dfj_enum(n, dists, relax=True)
                obj_int, _, time_int, n_vars, n_constr = solve_dfj_enum(n, dists, relax=False)
                
                gap = (obj_int - obj_relax) / obj_int if obj_int else 0
                writer.writerow([instance_name, "DFJ_enum", rounded(obj_int), rounded(time_int), rounded(obj_relax), rounded(time_relax), rounded(gap, 4), n_vars, n_constr])
                csvfile.flush()
            
            print(f"  - DFJ Iter...")
            obj_relax = "None"
            time_relax = "None"
            gap = "None"
            
            obj_int, _, time_int, _, n_vars, n_constr = solve_dfj_iter(n, dists)
            
            writer.writerow([instance_name, "DFJ_iter", rounded(obj_int), rounded(time_int), obj_relax, time_relax, gap, n_vars, n_constr])
            csvfile.flush()
            
    print(f"Benchmark completed. Results saved to {OUTPUT_FILE}")

def rounded(val, digits=4):
    if val is None: return ""
    return round(val, digits)

if __name__ == "__main__":
    run_benchmark()
