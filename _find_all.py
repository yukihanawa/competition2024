from copy import deepcopy
def is_valid_move(grid, row, col, num):
    """指定された位置に数字を置けるか確認する"""
    # 同じ行のチェック
    for x in range(9):
        if grid[row][x] == num:
            return False
    
    # 同じ列のチェック
    for x in range(9):
        if grid[x][col] == num:
            return False
    
    # 3x3のブロックのチェック
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    
    return True

def find_empty_location(grid):
    """空のマスを見つける"""
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

def solve_sudoku(grid):
    """数独を解くための再帰関数"""
    empty_loc = find_empty_location(grid)
    
    # 空のマスがない場合は解が見つかった
    if not empty_loc:
        return [grid]
    
    row, col = empty_loc
    solutions = []
    
    # 1から9までの数字を試す
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            # 数字を一時的に置く
            grid[row][col] = num
            
            # 再帰的に解を探索
            sub_solutions = solve_sudoku([row[:] for row in grid])
            solutions.extend(sub_solutions)
            
            # バックトラック
            grid[row][col] = 0
    
    return solutions

def print_solutions(solutions):
    """解を整形して表示する"""
    if not solutions:
        print("解は見つかりませんでした。")
        return
    
    print(f"解の数: {len(solutions)}")
    for solution in solutions:
        for row in solution:
            print(" ".join(map(str, row)))
        print()  # 解の間に空行を入れる

# # 数独の問題を定義（0は空のマス）
# sudoku_grid = [
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 9]
# ]
# puzzle = [
#     [2, 0, 0, 0, 0, 0, 0, 0, 7],
#     [0, 0, 3, 4, 0, 8, 5, 0, 0],
#     [0, 8, 0, 0, 6, 0, 0, 2, 0],
#     [0, 3, 0, 0, 0, 0, 0, 5, 0],
#     [0, 0, 2, 0, 0, 0, 7, 0, 0],
#     [0, 7, 0, 0, 0, 0, 0, 3, 0],
#     [0, 4, 0, 0, 8, 0, 0, 6, 0],
#     [0, 0, 6, 3, 0, 4, 2, 0, 0],
#     [8, 0, 0, 0, 0, 0, 0, 0, 3]
# ]

# print(puzzle)

# # # 解を見つけて表示
# solutions = solve_sudoku([row[:] for row in puzzle])
# print_solutions(solutions)