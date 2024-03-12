import math
import time
from collections import deque, defaultdict
from queue import PriorityQueue

def parse_adjacencies(file_path):
    graph = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file:
            city_a, city_b = line.strip().split()
            graph[city_a].append(city_b)
            graph[city_b].append(city_a)
    return graph

def parse_coordinates(file_path):
    coordinates = {}
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            city, lat, lon = line.strip().split(',')
            coordinates[city] = (float(lat), float(lon))
    return coordinates

def calculate_distance(coord1, coord2):
    lat1, lon1, lat2, lon2 = *coord1, *coord2
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 3958.8 * c
    return distance

def bfs_search(graph, coordinates, start, goal):
    start_time = time.time()
    queue = deque([(start, [start], 0)])
    visited = {start}
    while queue:
        current, path, distance = queue.popleft()
        if current == goal:
            return path, distance, time.time() - start_time
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor], distance + calculate_distance(coordinates[current], coordinates[neighbor])))
    return None, 0, time.time() - start_time

def dfs_search(graph, coordinates, start, goal):
    start_time = time.time()
    stack = deque([(start, [start], 0)])
    visited = {start}
    while stack:
        current, path, distance = stack.pop()
        if current == goal:
            return path, distance, time.time() - start_time
        for neighbor in reversed(graph[current]):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor], distance + calculate_distance(coordinates[current], coordinates[neighbor])))
    return None, 0, time.time() - start_time

def iddfs_search(graph, coordinates, start, goal, max_depth=30):
    start_time = time.time()
    def dls(node, depth):
        if node == goal:
            return [node], 0
        if depth == 0:
            return None, 0
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                path, dist = dls(neighbor, depth - 1)
                if path:
                    return [node] + path, dist + calculate_distance(coordinates[node], coordinates[neighbor])
        return None, 0
    for depth in range(max_depth):
        visited = {start}
        path, dist = dls(start, depth)
        if path:
            return path, dist, time.time() - start_time
    return None, 0, time.time() - start_time

def best_first_search(graph, coordinates, start, goal):
    start_time = time.time()
    open_set = PriorityQueue()
    open_set.put((0, start, [start], 0))
    visited = {start}
    while not open_set.empty():
        _, current, path, dist = open_set.get()
        if current == goal:
            return path, dist, time.time() - start_time
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                open_set.put((calculate_distance(coordinates[neighbor], coordinates[goal]), neighbor, path + [neighbor], dist + calculate_distance(coordinates[current], coordinates[neighbor])))
    return None, 0, time.time() - start_time

def a_star_search(graph, coordinates, start, goal):
    start_time = time.time()
    open_set = PriorityQueue()
    open_set.put((0, start, [start], 0))
    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0
    f_score = defaultdict(lambda: float('inf'))
    f_score[start] = calculate_distance(coordinates[start], coordinates[goal])
    while not open_set.empty():
        _, current, path, current_dist = open_set.get()
        if current == goal:
            return path, current_dist, time.time() - start_time
        for neighbor in graph[current]:
            tentative_g_score = current_dist + calculate_distance(coordinates[current], coordinates[neighbor])
            if tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + calculate_distance(coordinates[neighbor], coordinates[goal])
                open_set.put((f_score[neighbor], neighbor, path + [neighbor], tentative_g_score))
    return None, 0, time.time() - start_time

def execute_search(graph, coordinates, start, goal, algorithm):
    search_methods = {
        'BFS': bfs_search,
        'DFS': dfs_search,
        'IDDFS': iddfs_search,
        'BESTFIRST': best_first_search,
        'A*': a_star_search,
    }
    if algorithm in search_methods:
        return search_methods[algorithm](graph, coordinates, start, goal)
    else:
        print(f"Invalid search algorithm: {algorithm}")
        return None, 0, 0

if __name__ == "__main__":
    adjacencies_path = 'Adjacencies.txt'
    coordinates_path = 'coordinates.csv'
    graph = parse_adjacencies(adjacencies_path)
    coordinates = parse_coordinates(coordinates_path)
    while True:
        start_city = input("Enter the start city: ")
        end_city = input("Enter the end city: ")
        print("Available search algorithms: BFS, DFS, IDDFS, BESTFIRST, A*")
        algorithm = input("Enter the search algorithm: ").upper()
        path, total_distance, elapsed_time = execute_search(graph, coordinates, start_city, end_city, algorithm)
        if path:
            print("Route:", " -> ".join(path))
            print(f"Total distance: {total_distance:.2f} miles")
            print(f"Elapsed time: {elapsed_time:.4f} seconds")
        else:
            print("No route found or invalid algorithm.")
        repeat = input("Do you want to perform another search? (yes/no): ").lower()
        if repeat != 'yes':
            print("Exiting program.")
            break
