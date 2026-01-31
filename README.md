# TSP Solver & Analysis 🚚

This repository contains a **Python** implementation designed to solve the **Traveling Salesman Problem (TSP)** using Integer Linear Programming (ILP).

It was developed by a team of two for the **Algorithmics and Operations Research** (*Algorithmique et Recherche Opérationnelle*) course at the **Université Libre de Bruxelles (ULB)** during the third year of the Bachelor's degree (Academic Year 2025-2026).

## 🎯 Objectives

The main goal of this project is to analyze and compare different ILP formulations for the TSP:

1. **Miller-Tucker-Zemlin (MTZ)** formulation.
2. **Dantzig-Fulkerson-Johnson (DFJ)** formulation.
* **Enumerative:** Generating all subtour elimination constraints a priori.
* **Iterative:** Using a "Constraint Generation" approach to add subtour elimination constraints on the fly.

The project also involves analyzing the **Linear Relaxation** of these models and comparing their performance (execution time, number of variables/constraints, and integrality gap).

## 🛠️ Technologies

* **Language:** Python 3
* **Solver Library:** [PuLP](https://pypi.org/project/PuLP/) 
* **Visualization:** Matplotlib (optional, for result plotting)

## 📂 Project Structure

* `tsp_solver.py`: Main script handling the model creation, solving, and constraint generation.
* `instances/`: Folder containing TSP instances (Euclidean, Random, Circle, etc.).
* `results.csv`: Generated file containing performance metrics for each run.
* `Rapport.pdf`: Scientific report detailing the comparative analysis of MTZ vs. DFJ.

## 🚀 Usage

To run the solver, use the following command format in your terminal:

```bash
python3 tsp_solver.py <instance_file> <method_id>

```

Arguments 

* `<instance_file>`: Path to the instance file (e.g., `instances/instance_10_random_sym_1.txt`).
* `<method_id>`: Integer indicating the formulation to use:
* `0`: **MTZ** (Integer Solution) 
* `1`: **MTZ** (Linear Relaxation) 
* `2`: **DFJ Enumerative** (Integer Solution - *Warning: Slow for n > 15*) 
* `3`: **DFJ Enumerative** (Linear Relaxation) 
* `4`: **DFJ Iterative** (Constraint Generation) 

### Example

To solve an instance using the **DFJ Iterative** method:

```bash
python3 tsp_solver.py instances/instance_10_euclidean_1.txt 4

```

## 👥 Authors

* **Stéphane Badi Budu** - [stephanebdbd](https://www.google.com/search?q=https://github.com/stephanebdbd)
* **Pietro NARCISI**

---

*Project realized for the Faculty of Sciences, ULB.*
