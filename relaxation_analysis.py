import os
import csv
from tsp_solver import read_instance, solve_mtz, solve_dfj_enum

INSTANCES_DIR = "instances"
OUTPUT_FILE = "relaxation_results.csv"

def run_relaxation_analysis():
    # En-tête du CSV simplifié pour l'analyse
    header = ["instance", "formulation", "obj_int", "obj_relax", "gap"]
    
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        
        files = sorted([f for f in os.listdir(INSTANCES_DIR) if f.endswith(".txt")])
        
        for filename in files:
            instance_name = filename.replace(".txt", "")
            print(f"Analyzing {instance_name}...")
            
            try:
                n, coords, dists = read_instance(filename)
            except Exception as e:
                print(f"Skipping {filename}: {e}")
                continue

            # --- 1. MTZ (Toutes les instances) ---
            print("  -> MTZ")
            val_relax, _, _, _, _ = solve_mtz(n, dists, relax=True)
            val_int, _, _, _, _ = solve_mtz(n, dists, relax=False)
            
            gap_mtz = (val_int - val_relax) / val_int if val_int else 0
            writer.writerow([instance_name, "MTZ", rounded(val_int), rounded(val_relax), rounded(gap_mtz, 5)])
            csvfile.flush()

            # --- 2. DFJ (Seulement pour n <= 15 via Enum) ---
            if n <= 15:
                print("  -> DFJ (Enum)")
                # La relaxation DFJ est obtenue via solve_dfj_enum(relax=True)
                val_relax_dfj, _, _, _, _ = solve_dfj_enum(n, dists, relax=True)
                # L'entier est le même (val_int), mais on peut le recalculer pour être sûr ou réutiliser val_int
                # Pour la cohérence "par formulation", recalculons ou utilisons solve_dfj_enum(relax=False)
                # (Mathématiquement val_int est identique pour les deux formulations si résolu à l'optimal)
                val_int_dfj, _, _, _, _ = solve_dfj_enum(n, dists, relax=False)
                
                gap_dfj = (val_int_dfj - val_relax_dfj) / val_int_dfj if val_int_dfj else 0
                writer.writerow([instance_name, "DFJ", rounded(val_int_dfj), rounded(val_relax_dfj), rounded(gap_dfj, 5)])
                csvfile.flush()

    print(f"Analysis completed. Results in {OUTPUT_FILE}")

def rounded(val, digits=4):
    if val is None: return "None"
    return round(val, digits)

if __name__ == "__main__":
    run_relaxation_analysis()
