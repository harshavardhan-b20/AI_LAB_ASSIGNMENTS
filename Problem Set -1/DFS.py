def dfs_recursive(graph, vertex, visited):
    if vertex not in visited:
        print(vertex, end=" ")  
        visited.add(vertex)
        for neighbor in graph[vertex]:
            dfs_recursive(graph, neighbor, visited)


graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

start_node = 'A'
visited_nodes = set()
dfs_recursive(graph, start_node, visited_nodes)
