import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import random

# Adjusted dynamic parameters for better accuracy and performance
ALPHA_INITIAL = 0.5  # Lower initial pheromone influence for exploration
BETA = 5  # Heuristic importance for distance
EVAPORATION_INITIAL = 0.8  # Higher initial evaporation rate for exploration
EVAPORATION_FINAL = 0.3  # Final evaporation rate to reinforce good paths
PHEROMONE_MIN = 0.1  # Minimum pheromone level to avoid complete evaporation
PHEROMONE_MAX = 10.0  # Maximum pheromone level to avoid too strong attraction
ITERATIONS = 100  # Number of iterations for the algorithm
ANT_COUNT_INITIAL = 100  # Start with more ants for early exploration
ANT_COUNT_FINAL = 50  # Reduce the number of ants as the algorithm converges
Q = 100  # Pheromone deposit factor
INITIAL_PHEROMONE = 1.0  # Initial pheromone level
EPSILON = 1e-10  # Small constant to avoid divide by zero


def read_kml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    placemark_elements = root.findall(".//{http://www.opengis.net/kml/2.2}Placemark")
    coordinates = []
    for placemark in placemark_elements:
        coordinates_element = placemark.find(".//{http://www.opengis.net/kml/2.2}coordinates")
        if coordinates_element is not None:
            coordinate = coordinates_element.text.strip().split(",")
            coordinates.append((float(coordinate[0]), float(coordinate[1])))
    return coordinates


def calculate_distance(coord1, coord2):
    return np.linalg.norm(coord1 - coord2)


def initialize_pheromone_matrix(size):
    return np.full((size, size), INITIAL_PHEROMONE)


def calculate_total_distance(order, coordinates):
    total_distance = 0
    for i in range(len(order) - 1):
        coord1 = coordinates[order[i]]
        coord2 = coordinates[order[i + 1]]
        total_distance += calculate_distance(coord1, coord2)
    return total_distance


def select_next_city(ant, visited, pheromone, coordinates):
    current_city = ant[-1]
    probabilities = []

    for next_city in range(len(coordinates)):
        if next_city not in visited:
            distance = calculate_distance(coordinates[current_city], coordinates[next_city])
            if distance == 0:
                distance = EPSILON
            pheromone_level = pheromone[current_city, next_city] ** ALPHA_INITIAL
            heuristic_value = (1.0 / distance) ** BETA
            probabilities.append(pheromone_level * heuristic_value)
        else:
            probabilities.append(0)

    probabilities = np.array(probabilities)
    if probabilities.sum() == 0:
        probabilities = np.ones(len(probabilities))  # Avoid NaN issue by setting uniform probabilities if all are zero
    probabilities = probabilities / probabilities.sum()

    return np.random.choice(len(coordinates), p=probabilities)


def update_pheromone(pheromone, all_ants, best_order, best_distance, iteration, max_iterations):
    # Dynamically adjust the evaporation rate
    evaporation_rate = EVAPORATION_INITIAL - (EVAPORATION_INITIAL - EVAPORATION_FINAL) * (iteration / max_iterations)
    pheromone *= (1 - evaporation_rate)

    for ant in all_ants:
        distance = calculate_total_distance(ant, coordinates_array)
        for i in range(len(ant) - 1):
            from_city = ant[i]
            to_city = ant[i + 1]
            pheromone[from_city, to_city] += Q / distance
            pheromone[to_city, from_city] += Q / distance

    # Best path pheromone update
    for i in range(len(best_order) - 1):
        from_city = best_order[i]
        to_city = best_order[i + 1]
        pheromone[from_city, to_city] += Q / best_distance
        pheromone[to_city, from_city] += Q / best_distance

    # Apply pheromone clamping to prevent too high or too low levels
    pheromone = np.clip(pheromone, PHEROMONE_MIN, PHEROMONE_MAX)

    return pheromone


def ant_colony_optimization(coordinates):
    size = len(coordinates)
    pheromone = initialize_pheromone_matrix(size)
    best_order = None
    best_distance = float('inf')

    for iteration in range(ITERATIONS):
        print(f"Starting iteration {iteration + 1}/{ITERATIONS}")

        # Dynamically adjust the number of ants based on the iteration
        current_ant_count = ANT_COUNT_INITIAL - (ANT_COUNT_INITIAL - ANT_COUNT_FINAL) * (iteration / ITERATIONS)
        current_ant_count = int(current_ant_count)

        all_ants = []
        for ant_index in range(current_ant_count):
            ant = [random.randint(0, size - 1)]
            visited = set(ant)

            while len(ant) < size:
                next_city = select_next_city(ant, visited, pheromone, coordinates)
                ant.append(next_city)
                visited.add(next_city)

            all_ants.append(ant)
            distance = calculate_total_distance(ant, coordinates)
            if distance < best_distance:
                best_distance = distance
                best_order = ant

        print(f"Iteration {iteration + 1}: Best distance so far = {best_distance}")

        # Update pheromone dynamically based on iteration
        pheromone = update_pheromone(pheromone, all_ants, best_order, best_distance, iteration, ITERATIONS)

    return best_order, best_distance


# Path to the KML file
file_path = r"/Users/georgem./PycharmProjects/GarbageTruck/venv/ΔΕΠΟΣ.kml"

# Read the KML file
coordinates = read_kml_file(file_path)
coordinates_array = np.array(coordinates)

# Solve using Ant Colony Optimization
best_order, best_distance = ant_colony_optimization(coordinates_array)

# Check if a solution was found
if best_order is None:
    print("No valid solution found.")
else:
    # Get optimized coordinates
    optimized_coordinates = coordinates_array[best_order]

    # Display optimized path coordinates
    print("Optimized Path Coordinates:")
    for index in best_order:
        print(coordinates[index])

    # Plot the optimized route
    plt.plot(optimized_coordinates[:, 0], optimized_coordinates[:, 1], 'g--')
    plt.scatter(optimized_coordinates[:, 0], optimized_coordinates[:, 1], color='k')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Optimized Garbage Truck Route with ACO')
    plt.grid()
    plt.show(block=True)  # Ensure the plot blocks until closed
