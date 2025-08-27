def calculate_cost(graph, path):
    cost = 0
    for i in range(len(path) - 1):
        cost += graph[path[i]][path[i + 1]]
    cost += graph[path[-1]][path[0]]  # Returning to start
    return cost

def bfs_tsp(graph, start):
    queue = [[start]]
    min_cost = float('inf')
    min_path = []
    
    while queue:
        path = queue.pop(0)
        if len(path) == len(graph):
            path.append(start)
            cost = calculate_cost(graph, path)
            if cost < min_cost:
                min_cost = cost
                min_path = path[:]
        else:
            for i in range(len(graph)):
                if i not in path:
                    new_path = path + [i]
                    queue.append(new_path)
    
    return min_path, min_cost

def dfs_tsp(graph, start):
    stack = [[start]]
    min_cost = float('inf')
    min_path = []
    
    while stack:
        path = stack.pop()
        if len(path) == len(graph):
            path.append(start)
            cost = calculate_cost(graph, path)
            if cost < min_cost:
                min_cost = cost
                min_path = path[:]
        else:
            for i in range(len(graph)-1, -1, -1):
                if i not in path:
                    new_path = path + [i]
                    stack.append(new_path)
    
    return min_path, min_cost

# Example Graph (Adjacency Matrix)
graph = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

start_node = 0
print("BFS Solution:", bfs_tsp(graph, start_node))
print("DFS Solution:", dfs_tsp(graph, start_node))
