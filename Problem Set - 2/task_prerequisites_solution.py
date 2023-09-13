def canFinish(tasks, prerequisites):
    # Create an adjacency list representation of the graph
    graph = [[] for _ in range(tasks)]
    
    # Build the graph based on prerequisites
    for prereq in prerequisites:
        graph[prereq[1]].append(prereq[0])
    
    # Define a recursive function to detect cycles
    def has_cycle(node, visited, stack):
        visited[node] = True
        stack[node] = True
        
        # Explore neighbors of the current node
        for neighbor in graph[node]:
            if not visited[neighbor]:
                if has_cycle(neighbor, visited, stack):
                    return True
            elif stack[neighbor]:
                return True
        
        stack[node] = False
        return False
    
    # Initialize data structures
    visited = [False] * tasks
    stack = [False] * tasks
    
    # Check for cycles in each node
    for i in range(tasks):
        if not visited[i] and has_cycle(i, visited, stack):
            return False
    
    return True

# Take input for the number of test cases
T = int(input("Enter the number of test cases: "))
for _ in range(T):
    tasks = int(input("Enter the number of tasks: "))
    n = int(input("Enter the number of prerequisites: "))
    prerequisites = []
    
    # Input prerequisites for the current test case
    for _ in range(n):
        prerequisite = list(map(int, input().split()))
        prerequisites.append(prerequisite)
    
    # Check if tasks can be finished for the current test case
    result = canFinish(tasks, prerequisites)
    print(result)
