import copy

def create(initial_state, level):
    def print_state_with_heuristic(state):
        for row in state:
            for col in row:
                print(col, end=" ")
            print()
        heuristic_value = find_heuristic(state, goal_state)
        print("Heuristic Value:", heuristic_value)
        print()

    def generate_successors(state):
        successors = []
        i, j = find_blank_position(state)

        
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        actions = ["Up", "Down", "Left", "Right"]

        for move, action in zip(moves, actions):
            new_i, new_j = i + move[0], j + move[1]
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = copy.deepcopy(state)
                new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
                successors.append((new_state, action))
        
        return successors

    def find_blank_position(state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j

    def find_heuristic(state, goal_state):
        heuristic_value = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != goal_state[i][j]:
                    heuristic_value += 1
        return heuristic_value

    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    queue = [(initial_state, 0)]  

    while queue:
        current_state, current_level = queue.pop(0)
        if current_level > level:
            break  
        print_state_with_heuristic(current_state)

        
        for successor_state, _ in generate_successors(current_state):
            queue.append((successor_state, current_level + 1))



initial_state = [[2, 8, 3], [1, 6, 4], [7, 0, 5]]
level = 4  
create(initial_state, level)
