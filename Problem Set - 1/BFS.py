def bfs(graph, start):
    visited = set()
    queue = [start]
    visited.add(start)
    traversal_order = []

    while queue:
        vertex = queue.pop(0)  
        traversal_order.append(vertex)

        for neighbor in graph[vertex]:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

    return traversal_order

# Example usage:
graph = {
    0: [1, 2],
    1: [2],
    2: [0, 3],
    3: [3]
}

start_vertex = 2
result = bfs(graph, start_vertex)
print("BFS traversal starting from vertex", start_vertex, ":", result)
