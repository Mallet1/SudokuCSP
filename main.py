import time

def print_grid(grid):
    for row in grid:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

def is_valid(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num or grid[x][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True

def find_unassigned_location(grid, mrv_domains):
    min_size = 10
    best_cell = None
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                size = len(mrv_domains[(row, col)])
                if size < min_size:
                    min_size = size
                    best_cell = (row, col)

    return best_cell

def forward_check(grid, row, col, value, mrv_domains):
    changes = []
    for x in range(9):
        if grid[row][x] == 0 and value in mrv_domains[(row, x)]:
            mrv_domains[(row, x)].remove(value)
            changes.append((row, x, value))

        if grid[x][col] == 0 and value in mrv_domains[(x, col)]:
            mrv_domains[(x, col)].remove(value)
            changes.append((x, col, value))

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == 0 and value in mrv_domains[(start_row + i, start_col + j)]:
                mrv_domains[(start_row + i, start_col + j)].remove(value)
                changes.append((start_row + i, start_col + j, value))

    return changes

def undo_forward_check(mrv_domains, changes):
    for row, col, value in changes:
        mrv_domains[(row, col)].append(value)

def solve_sudoku(grid):
    mrv_domains = {(row, col): [num for num in range(1, 10) if is_valid(grid, row, col, num)]
                   for row in range(9) for col in range(9) if grid[row][col] == 0}

    def backtrack():
        cell = find_unassigned_location(grid, mrv_domains)
        if not cell:
            return True

        row, col = cell
        for value in sorted(mrv_domains[(row, col)]):
            if is_valid(grid, row, col, value):
                grid[row][col] = value
                changes = forward_check(grid, row, col, value, mrv_domains)

                if backtrack():
                    return True

                grid[row][col] = 0
                undo_forward_check(mrv_domains, changes)

        return False

    start_time = time.time()
    success = backtrack()
    end_time = time.time()

    if success:
        print("Solution found:")
        print_grid(grid)
        print(f"CPU time: {end_time - start_time:.2f} seconds")
    else:
        print("No solution exists or the computation was terminated after exceeding the time limit.")

grid = [
    [0,0,1,0,0,2,0,0,0],
    [0,0,5,0,0,6,0,3,0],
    [4,6,0,0,0,5,0,0,0],
    [0,0,0,1,0,4,0,0,0],
    [6,0,0,8,0,0,1,4,3],
    [0,0,0,0,9,0,5,0,8],
    [8,0,0,0,4,9,0,5,0],
    [1,0,0,3,2,0,0,0,0],
    [0,0,9,0,0,0,3,0,0]
]

grid = [
    [0,0,5,0,1,0,0,0,0],
    [0,0,2,0,0,4,0,3,0],
    [1,0,9,0,0,0,2,0,6],
    [2,0,0,0,3,0,0,0,0],
    [0,4,0,0,0,0,7,0,0],
    [5,0,0,0,0,7,0,0,1],
    [0,0,0,6,0,3,0,0,0],
    [0,6,0,1,0,0,0,0,0],
    [0,0,0,0,7,0,0,5,0]
]

grid = [
    [6,7,0,0,0,0,0,0,0],
    [0,2,5,0,0,0,0,0,0],
    [0,9,0,5,6,0,2,0,0],
    [3,0,0,0,8,0,9,0,0],
    [0,0,0,0,0,0,8,0,1],
    [0,0,0,4,7,0,0,0,0],
    [0,0,8,6,0,0,0,9,0],
    [0,0,0,0,0,0,0,1,0],
    [1,0,6,0,5,0,0,7,0]
]

solve_sudoku(grid)
