def topological_sort(graph):
    visited = set()
    stack = []
    ordering = []

    def dfs(vertex):
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(vertex)

    for vertex in graph:
        if vertex not in visited:
            dfs(vertex)

    while stack:
        ordering.append(stack.pop())

    return ordering

# Example usage:
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['E'],
    'D': [],
    'E': []
}

result = topological_sort(graph)
print("Topological Sort:", result)
