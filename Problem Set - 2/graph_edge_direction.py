def solve(N, M, edges):
    # Create an adjacency list to represent the graph
    adj_list = [[] for _ in range(N+1)]
    # Initialize arrays to keep track of degrees and edge directions
    degree = [0] * (N+1)
    directions = [-1] * M

    # Build the adjacency list and calculate degrees
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
        degree[u] += 1
        degree[v] += 1

    # Assign edge directions based on even degrees
    for i, (u, v) in enumerate(edges):
        if degree[u] % 2 == 0:
            directions[i] = 0
            degree[v] -= 1
        elif degree[v] % 2 == 0:
            directions[i] = 1
            degree[u] -= 1

    # Check if all vertices have even degrees
    if all(deg % 2 == 0 for deg in degree[1:]):
        return directions  # Return the list of directions
    else:
        return [-1]  # Return -1 indicating it's not possible

# Read input
T = int(input())  # Number of test cases
for _ in range(T):
    N, M = map(int, input().split())  # N: vertices, M: edges
    edges = [tuple(map(int, input().split())) for _ in range(M)]  # Edges
    result = solve(N, M, edges)
    
    # Output the result
    if result[0] == -1:
        print(-1)
    else:
        print(" ".join(map(str, result)))
