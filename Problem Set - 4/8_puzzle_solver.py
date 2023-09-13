def is_valid(x, y):
    return 0 <= x < 3 and 0 <= y < 3

def create(initial_state, level):
    
    queue = [(initial_state, 0)]

    
    visited = set()
    visited.add(tuple(map(tuple, initial_state)))

    while queue:
        current_state, current_level = queue.pop(0)

        if current_level > level:
            break

        print(f"Level {current_level}:\n")
        for row in current_state:
            print(row)

        
        for i in range(3):
            for j in range(3):
                if current_state[i][j] == 0:
                    x, y = i, j

        
        actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in actions:
            new_x, new_y = x + dx, y + dy

            if is_valid(new_x, new_y):
                
                new_state = [list(row) for row in current_state]
                new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]

               
                new_state_tuple = tuple(map(tuple, new_state))

                if new_state_tuple not in visited:
                    visited.add(new_state_tuple)
                    queue.append((new_state, current_level + 1))


initial_state = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 5, 8]
]
level = 2

create(initial_state, level)
