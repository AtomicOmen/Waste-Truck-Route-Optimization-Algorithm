# Garbage Truck Route Optimization with Ant Colony Algorithm

This project implements an Ant Colony Optimization (ACO) algorithm to find the best route for a garbage truck to collect bins in the most efficient way. The algorithm reads geographical coordinates from a KML file and optimizes the order of locations to minimize the total distance traveled.

## Features
- **Ant Colony Optimization (ACO)**: Solves the Traveling Salesman Problem (TSP) for garbage truck route optimization.
- **Dynamic Parameters**: Includes dynamic evaporation rates, pheromone clamping, and variable ant count to balance exploration and exploitation.
- **Interactive Plotting**: Visualizes the optimized route using `matplotlib`.
- **KML Input**: Reads geographical coordinates from a KML file to determine garbage bin locations.

## Installation

### Requirements
- Python 3.x
- Required Libraries:
  - `matplotlib`: for plotting the optimized routes.
  - `numpy`: for numerical operations.
  - `xml.etree.ElementTree`: for reading KML files (included in Python).

To install the required dependencies, run:

```bash
pip install numpy matplotlib
```

## Project Structure

```
.
├── main.py          # Main Python script with the ACO algorithm implementation
├── README.md        # Project documentation
└── ΔΕΠΟΣ.kml        # Sample KML file with bin coordinates
```

## How It Works
The Ant Colony Optimization (ACO) algorithm simulates the behavior of ants finding paths in a graph. Each ant constructs a solution based on pheromone trails and heuristics (such as distance). Over multiple iterations, the algorithm balances exploration (trying new routes) and exploitation (refining the best routes).

### Algorithm Overview
**Pheromone Trails:** Guide ants in selecting paths. Higher pheromone levels on paths indicate better solutions.
**Evaporation:** Pheromone levels decay over time to avoid premature convergence to suboptimal solutions.
**Dynamic Ant Count:** More ants explore in early iterations, while fewer ants refine the solution later on.
**Pheromone Clamping:** Limits the pheromone levels to prevent stagnation or excessive dominance of any one path.
### Steps:
- **Load Coordinates:** The script reads coordinates from a KML file.

- **Optimize with ACO:** Ant Colony Optimization is used to determine the best route.

- **Plot Results:** The optimized route is displayed on a 2D plot using matplotlib.

## Running the Code

### 1. Clone the Repository
```
git clone https://github.com/your-username/garbage-truck-aco.git
cd garbage-truck-aco
```
### 2. Ensure the Required Libraries are Installed
```
pip install numpy matplotlib
```
### 3. Run the Script
```
python main.py
```
Make sure the KML file (e.g., ΔΕΠΟΣ.kml) is located in the same directory as main.py.
## Sample Output
The program will print the optimized path coordinates and show a plot of the garbage truck's route:
```
Optimized Path Coordinates:
(24.3830459867467, 40.9263259808839)
(24.3830599867475, 40.9258319808848)
...
```
The plot will display the garbage truck's optimized route.

## Parameter Tuning
You can adjust the following ACO parameters in the code to balance between exploration and exploitation:

- **ALPHA_INITIAL:** Initial influence of pheromones (default: 0.5).
- **BETA:** Importance of distance (default: 5).
- **EVAPORATION_INITIAL:** Initial pheromone evaporation rate (default: 0.8).
- **ANT_COUNT_INITIAL:** Number of ants used in the initial iterations (default: 100).
- **ITERATIONS:** Number of iterations to run the algorithm (default: 100).

### Example of Parameter Adjustment:
If you want to explore faster convergence, you can decrease the number of ants or iterations:
```
ANT_COUNT_INITIAL = 50
ITERATIONS = 50
```

## Notes
- Make sure the KML file is valid and contains well-formed coordinates for all garbage bin locations.
- You can add more geographic data points to the KML file to extend the route optimization.




