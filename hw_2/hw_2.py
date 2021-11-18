import time
import random
import functools

all_conflicts = {}



def generate_positions_for_queens(board_size, conflicts):
    positions = {}
    for col in range(board_size):
        row = get_random_row_of_queen_with_min_conflicts(positions, col, board_size, conflicts)
        positions[col] = row
        update_conflicts_for_queen_position(row, col, board_size, conflicts)
    return positions

def remove_conflicts_for_queen(row, col, board_size, conflicts):
    conflicts[col][row] -= 1
    for j in range(board_size) :
        if j == row:
            continue
        conflicts[col][j] -= 1
    for j in range(board_size):
        if j == col :
            continue
        conflicts[j][row] -= 1
    ccol = col - 1
    rrow = row + 1
    while ccol >= 0 and rrow < board_size:
        conflicts[ccol][rrow] -= 1
        ccol -= 1
        rrow += 1
    ccol = col + 1
    rrow = row - 1
    while ccol < board_size and rrow >= 0:
        conflicts[ccol][rrow] -= 1
        ccol += 1
        rrow -= 1
    ccol = col + 1
    rrow = row + 1
    while ccol < board_size and rrow < board_size:
        conflicts[ccol][rrow] -= 1
        ccol += 1
        rrow += 1
    ccol = col - 1
    rrow = row - 1
    while ccol >= 0 and rrow >= 0:
        conflicts[ccol][rrow] -= 1
        ccol -= 1
        rrow -= 1    


def get_random_col_of_queen_with_max_conflicts(positions, board_size, conflicts):
    if positions == {}:
        return random.randint(0, board_size - 1)
    max_conflicts = 0
    columns = []
    for col, row in positions.items():
        current_conflicts = conflicts[col][row]
        if current_conflicts > max_conflicts:
            max_conflicts = current_conflicts
            columns = []
            columns.append(col)
        elif current_conflicts == max_conflicts:
            columns.append(col)
    if max_conflicts == 1:
        return
    return random.choice(columns)


def update_conflicts_for_queen_position(row,col, board_size, conflicts):
    conflicts[col][row] += 1
    for j in range(board_size) :
        if j == row:
            continue
        conflicts[col][j] += 1
    for j in range(board_size):
        if j == col :
            continue
        conflicts[j][row] += 1
    ccol = col - 1
    rrow = row + 1
    while ccol >= 0 and rrow < board_size:
        conflicts[ccol][rrow] += 1
        ccol -= 1
        rrow += 1
    ccol = col + 1
    rrow = row - 1
    while ccol < board_size and rrow >= 0:
        conflicts[ccol][rrow] += 1
        ccol += 1
        rrow -= 1
    ccol = col + 1
    rrow = row + 1
    while ccol < board_size and rrow < board_size:
        conflicts[ccol][rrow] += 1
        ccol += 1
        rrow += 1
    ccol = col - 1
    rrow = row - 1
    while ccol >= 0 and rrow >= 0:
        conflicts[ccol][rrow] += 1
        ccol -= 1
        rrow -= 1    




def get_random_row_of_queen_with_min_conflicts(positions, col, board_size, conflicts):
    if positions == {}:
        return random.randint(0, board_size - 1)

    min_conflicts = min(conflicts[col])
    rows = []
    for row in range(len(conflicts[col])):
        current_conflicts = conflicts[col][row]
        if current_conflicts == min_conflicts:
            rows.append(row)
    return random.choice(rows)


def print_board(queen_positions, size):
    for i in range(size):
        for j in range(size):
            if queen_positions.get(j, None) == i:
                print('Q', end=' ')
            else:
                print('_', end=' ')
        print()
    print()

def solve(size):
    conflicts = []
    for i in range(size):
        conflicts.append([])
        for _ in range(size):
            conflicts[i].append(0)
    queen_positions = generate_positions_for_queens(size, conflicts)
    count = 0
    while count < 3 * size and has_conflicts(conflicts,queen_positions):
        col = get_random_col_of_queen_with_max_conflicts(queen_positions, size,conflicts)
        if not col:
            break
        row = get_random_row_of_queen_with_min_conflicts(queen_positions, col, size, conflicts)
        remove_conflicts_for_queen(queen_positions[col], col, size, conflicts)
        queen_positions[col] = row
        update_conflicts_for_queen_position(row, col, size, conflicts)
        count += 1
    if has_conflicts(conflicts, queen_positions):
        return solve(size)
    else:
        return queen_positions

def has_conflicts(conflicts, positions):
    for col, row in positions.items():
        if conflicts[col][row] > 1:
            return True
    return False

def main():
    board_size = int(input('Enter board size: '))
    start_time = time.time()
    positions = solve(board_size)
    print(time.time() - start_time)
    print_board(positions, board_size)
    


main()

