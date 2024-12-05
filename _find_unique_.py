import numpy as np
from copy import deepcopy
import random

# ナンプレのサイズ
GRID_SIZE = 9

# HINT_PATTERNを定義（穴を開ける場所）
HINT_PATTERN = [
    1, 0, 0, 0, 0, 0, 0, 0, 1, 
    0, 0, 1, 1, 0, 1, 1, 0, 0, 
    0, 1, 0, 0, 1, 0, 0, 1, 0, 
    0, 1, 0, 0, 0, 0, 0, 1, 0, 
    0, 0, 1, 0, 0, 0, 1, 0, 0, 
    0, 1, 0, 0, 0, 0, 0, 1, 0, 
    0, 1, 0, 0, 1, 0, 0, 1, 0, 
    0, 0, 1, 1, 0, 1, 1, 0, 0, 
    1, 0, 0, 0, 0, 0, 0, 0, 1
]

# ナンプレグリッドの初期化
def create_empty_grid():
    return np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

# 3x3のブロックの中で数字が有効かをチェック
def is_valid(grid, row, col, num):
    """指定した位置に数字を置けるかを確認"""
    if num in grid[row, :]: return False  # 行のチェック
    if num in grid[:, col]: return False  # 列のチェック
    # セクションのチェック
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in grid[start_row:start_row+3, start_col:start_col+3]:
        return False
    return True

# 再帰的なバックトラッキングでナンプレを解く
def solve_sudoku(grid):
    """バックトラッキングでナンプレを解く"""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:  # 空きマスを探す
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0  # バックトラック
                return False  # 解がない場合
    return True  # 全て埋まった

# ナンプレをランダムに解いて完全な解を作る
def generate_full_solution():
    grid = create_empty_grid()
    solve_sudoku(grid)
    return grid

# 問題を生成する（ヒントを設定）
def generate_sudoku_problem():
    full_solution = generate_full_solution()
    problem = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    # HINT_PATTERNに基づき、問題にヒントを設定
    for i, hint in enumerate(HINT_PATTERN):
        if hint == 1:
            row, col = divmod(i, GRID_SIZE)
            problem[row, col] = full_solution[row, col]

    # 唯一解を持つことを確認
    if not has_unique_solution(problem):
        return generate_sudoku_problem()  # 解が一意でない場合、再帰的に問題を再生成

    return problem

def count_solutions(grid):
    """解を数える"""
    solutions = []

    def backtrack(grid):
        """再帰的に解を探索して解の数を数える"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(grid, row, col, num):
                            grid[row][col] = num
                            backtrack(grid)
                            grid[row][col] = 0
                    return  # 解を数えるのが目的なので、途中で終了
        # 解を記録
        solutions.append(deepcopy(grid))

    backtrack(grid)
    return len(solutions)

def has_unique_solution(grid):
    """解が一意であるかどうかを確認"""
    return count_solutions(grid) == 1

# 問題を生成
problem = generate_sudoku_problem()

# 問題の表示
print("生成されたナンプレ問題:")
print(problem)