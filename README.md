# Route Finding Across Cities

This project tackles a fundamental problem in computer science and logistics: finding the optimal route between two points. Specifically, it focuses on route-finding across a network of cities, leveraging various algorithmic approaches to identify the most efficient path from city A to city X.

## Problem Context

The challenge involves navigating a simplified map of southern Kansas, marked by small towns and their connections (adjacencies). Unlike real-world mapping applications, which consider numerous variables for route optimization, this project simplifies the problem to focus on the algorithmic exploration of paths based on given adjacencies and geographic locations.

## Implemented Algorithms

This project implements five distinct search algorithms, each offering a different approach to route finding:

### Breadth-First Search (BFS)

Explores the network level by level, ensuring the shortest path is found in an unweighted graph.

### Depth-First Search (DFS)

Dives deep into the network, exploring as far down a branch as possible before backtracking. Efficient for exhaustive searches.

### Iterative Deepening Depth-First Search (ID-DFS)

Combines the benefits of DFS and BFS, using depth as a limiting factor to systematically explore all possible paths.

### Best-First Search

A heuristic-driven approach that expands the most promising node based on a specific rule or heuristic, such as geographic proximity.

### A* Search

An advanced search algorithm that uses both the cost to reach a node and an estimate of the cost to reach the goal, making it efficient for finding the shortest path.


## Results and Analysis

After executing a search, the program displays:
- The chosen route from the start to the destination city.
- The total distance of the route.
- Execution time and, optionally, memory usage for the search.

Screenshots demonstrating each algorithm's execution and output are included for reference.
