import math
from collections import deque, defaultdict
from queue import PriorityQueue

# Function to parse adjacencies from the text file
def parse_adjacencies(file_path):
    graph = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file:
            city_a, city_b = line.strip().split()
            graph[city_a].append(city_b)
            graph[city_b].append(city_a)  # Ensure bidirectional connectivity
    return graph

# Function to parse city coordinates from the CSV file
def parse_coordinates(file_path):
    coordinates = {}
    with open(file_path, 'r') as file:
        next(file)  # Skip header line
        for line in file:
            city, lat, lon = line.strip().split(',')
            coordinates[city] = (float(lat), float(lon))
    return coordinates

# Haversine formula to calculate the distance between two points on the earth
def calculate_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    r = 3956  # Radius of Earth in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = r * c
    return distance

# Implementations for BFS, DFS, ID-DFS, BestFirst, and A* algorithms go here
# Due to space, including only corrected execute_search function as an example
def bfs_search(graph, coordinates, start, goal):
    queue = deque([(start, [start], 0)])  # (current_city, path, total_distance)
    visited = set()

    while queue:
        current_city, path, total_distance = queue.popleft()
        if current_city == goal:
            return path, total_distance

        for neighbor in graph[current_city]:
            if neighbor not in visited:
                visited.add(neighbor)
                new_distance = total_distance + calculate_distance(coordinates[current_city], coordinates[neighbor])
                queue.append((neighbor, path + [neighbor], new_distance))
    
    return None, 0

# Depth-First Search Algorithm
def dfs_search(graph, coordinates, start, goal, path=None, total_distance=0, visited=set()):
    if path is None:
        path = [start]
        visited.add(start)
    
    if start == goal:
        return path, total_distance

    for neighbor in graph[start]:
        if neighbor not in visited:
            visited.add(neighbor)
            new_distance = total_distance + calculate_distance(coordinates[start], coordinates[neighbor])
            new_path, new_total_distance = dfs_search(graph, coordinates, neighbor, goal, path + [neighbor], new_distance, visited)
            if new_path:
                return new_path, new_total_distance

    return None, 0

# Iterative Deepening Depth-First Search Algorithm
def iddfs_search(graph, coordinates, start, goal):
    def dls(node, depth, path, total_distance):
        if node == goal:
            return path, total_distance
        if depth <= 0:
            return None, 0
        for neighbor in graph[node]:
            if neighbor not in path:  # Avoid cycles
                new_distance = total_distance + calculate_distance(coordinates[node], coordinates[neighbor])
                found_path, found_distance = dls(neighbor, depth - 1, path + [neighbor], new_distance)
                if found_path:
                    return found_path, found_distance
        return None, 0

    for depth in range(len(graph)):
        path, distance = dls(start, depth, [start], 0)
        if path:
            return path, distance

    return None, 0

# Best-First Search Algorithm
def best_first_search(graph, coordinates, start, goal):
    visited = set()  # Tracks visited cities
    open_set = PriorityQueue()  # Stores the cities to be explored
    open_set.put((0, start, [start]))  # Initialize with start city; format: (heuristic, city, path)

    while not open_set.empty():
        current_heuristic, current_city, path = open_set.get()

        # If the goal is reached, calculate total path distance and return the path and distance
        if current_city == goal:
            total_distance = 0
            for i in range(len(path) - 1):
                total_distance += calculate_distance(coordinates[path[i]], coordinates[path[i + 1]])
            return path, total_distance

        if current_city not in visited:
            visited.add(current_city)
            
            for neighbor in graph[current_city]:
                if neighbor not in visited:
                    # Calculate heuristic for neighbor (distance from neighbor to goal)
                    neighbor_heuristic = calculate_distance(coordinates[neighbor], coordinates[goal])
                    # Put neighbor in the priority queue with updated path
                    open_set.put((neighbor_heuristic, neighbor, path + [neighbor]))

    return None, 0  # Return None if no path is found



# A* Search Algorithm
from queue import PriorityQueue

def a_star_search(graph, coordinates, start, goal):
    # Initialize the open set with the start node
    open_set = PriorityQueue()
    open_set.put((0, start, [start], 0))  # (Estimated total cost, current node, path, cost so far)

    # Costs from start to all nodes initialized to infinity, except the start node
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    # Estimated cost from start to goal through each node
    f_score = {node: float('inf') for node in graph}
    f_score[start] = calculate_distance(coordinates[start], coordinates[goal])

    while not open_set.empty():
        current_f_score, current, path, current_cost = open_set.get()

        if current == goal:
            return path, current_cost

        for neighbor in graph[current]:
            tentative_g_score = current_cost + calculate_distance(coordinates[current], coordinates[neighbor])
            
            if tentative_g_score < g_score[neighbor]:  # A shorter path to neighbor has been found
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + calculate_distance(coordinates[neighbor], coordinates[goal])
                open_set.put((f_score[neighbor], neighbor, path + [neighbor], tentative_g_score))

    return None, 0


# Function to select and execute a search algorithm, including normalization for algorithm names
def execute_search(graph, coordinates, start, goal, algorithm):
    search_algorithms = {
        'BFS': bfs_search,
        'DFS': dfs_search,
        'IDDFS': iddfs_search,
        'BESTFIRST': best_first_search,  # Note the normalization
        'A*': a_star_search,
    }
    
    # Normalize input to match keys in the search_algorithms dictionary
    algorithm_key = algorithm.replace('-', '').replace(' ', '').upper()
    
    if algorithm_key in search_algorithms:
        return search_algorithms[algorithm_key](graph, coordinates, start, goal)
    else:
        print("Invalid search algorithm.")
        return None, 0

# Main execution block with normalization and repeat option
if __name__ == "__main__":
    adjacencies_path = 'Adjacencies.txt'
    coordinates_path = 'coordinates.csv'
    
    graph = parse_adjacencies(adjacencies_path)
    coordinates = parse_coordinates(coordinates_path)

    while True:
        start_city = input("Enter the start city: ")
        end_city = input("Enter the end city: ")
        print("Available search algorithms: BFS, DFS, ID-DFS, BestFirst, A*")
        algorithm = input("Enter the search algorithm: ")

        path, total_distance = execute_search(graph, coordinates, start_city, end_city, algorithm)

        if path:
            print("Route:", " -> ".join(path))
            print(f"Total distance: {total_distance:.2f} miles")
        else:
            print("No route found or invalid algorithm.")
        
        repeat = input("Do you want to perform another search? (yes/no): ").lower()
        if repeat != 'yes':
            print("Exiting program.")
            break
