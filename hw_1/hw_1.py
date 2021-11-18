from copy import deepcopy

import math
import time
import heapq




def a_star(start, goal):
    if not is_solveable(start):
        print("Not solvable")
        return
    visited = set()
    path = {tuple(flatten_matrix(start)): None}
    mhd = calculate_manhatan_distance(start, goal)
    heap = [(mhd,start)]
    heapq.heapify(heap)
    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            break
        current_state_flatten = tuple(flatten_matrix(current))
        if current_state_flatten not in visited:
            visited.add(current_state_flatten)
        for entry in get_childs_of_state(current):
            [direction, child_node] = entry
            child_state_flatten = tuple(flatten_matrix(child_node))
            if child_state_flatten in visited:
                continue
            path[child_state_flatten] = (direction, current_state_flatten)
            mhd = calculate_manhatan_distance(child_node, goal)
            visited.add(child_state_flatten)
            heapq.heappush(heap, (mhd, child_node))
    if current != goal:
        print("Not solveable")
        return 
    result = []
    current = tuple(flatten_matrix(current))
    while path[current]:
        result.append(path[current])
        current = path[current][1]
    count = 0
    for (direction, state) in result[::-1]:
        print_state(create_matrix_from_list(state))
        print(direction)
        count += 1
    print_state(goal)        
    print(count)
def print_state(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=' ')
        print()

def create_matrix_from_list(list):
    matrix = [[]]
    matrix_row_col = math.sqrt(len(list))
    current_row = 0
    for i,num in enumerate(list):
        if i != 0 and i % matrix_row_col == 0:
            current_row += 1
            matrix.append([])
        matrix[current_row].append(num)
    return matrix

def get_childs_of_state(state):
    x = -1
    y = -1
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] == 0:
                x = i 
                y = j
    possible_moves = {(x + 1,y): 'U', (x - 1,y): 'D', (x,y - 1): 'R', (x, y + 1): 'L'}
    new_states = []
    for move, direction in possible_moves.items():
        if move[0] < 0 or len(state[0]) <= move[0]:
            continue
        elif move[1] < 0 or len(state) <= move[1]:
            continue
        temp = deepcopy(state)
        temp[move[0]][move[1]], temp[x][y] = temp[x][y], temp[move[0]][move[1]]
        new_states.append([direction,temp])
    return new_states


def get_positions_state(state):
    goal_positions = {}
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] == 0:
                continue
            goal_positions[state[i][j]] = [i,j]
    return goal_positions
def calculate_manhatan_distance(state, goal):
    dist = 0
    goal_positions = get_positions_state(goal)

    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] == 0:
                continue
            dist += abs(goal_positions[state[i][j]][0] - i) + abs(goal_positions[state[i][j]][1] - j)
    return dist

def flatten_matrix(board):
    return [item for lst in board for item in lst]

def is_solveable(state):
    count_inversions = 0
    flat_list = [item for lst in state for item in lst]
    for i,item in enumerate(flat_list):
        if item == 0:
            continue
        inversions = [el for el in flat_list[i+1:] if item > el and el != 0]
        count_inversions += len(inversions)
    return count_inversions % 2 == 0

def get_goal_state(num_row_cols, blocks, empty_index):
    goal_state = []
    nums = list(range(1,blocks + 1))
    if empty_index == -1:
        nums.append(0)
    else:
        nums.insert(empty_index, 0)
    for i in range(0,len(nums),num_row_cols):
        goal_state.append(nums[i: i + num_row_cols])    
    return goal_state

def get_start_state(row_cols):
    start_state = []
    for _ in range(row_cols):
        row_input = input()
        row = [int(x) for x in row_input.split()]
        start_state.append(row)
    return start_state    
def main():
    blocks = int(input("Enter number of non empty blocks: "))
    empty_index = input("Enter the index of the empty block(by default is down right): ") or -1
    empty_index = int(empty_index)
    row_cols = int(math.sqrt(blocks) + 1)
    start_state = get_start_state(row_cols)
    start_time = time.time()
    goal_state = get_goal_state(row_cols, blocks, empty_index)
    a_star(start_state, goal_state)
    print(f"Time elapsed since program start: {time.time() - start_time} seconds")
main()


