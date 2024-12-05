import numpy as np


def find_empty_2d(board):
    """
    空きマスを探す（2次元リスト）。
    """
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None


def is_valid_2d(board, row, col, num):
    """
    その数字がそのマスに置けるかチェック（2次元リスト）。
    """
    # 行のチェック
    if num in board[row]:
        return False

    # 列のチェック
    if num in [board[r][col] for r in range(9)]:
        return False

    # 3×3ブロックのチェック
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False

    return True


# def solve_sudoku_wrapper_2d(board):
#     """
#     2次元リスト形式の数独ソルバーのラッパー関数。
#     - 解を求めるとともに複数解かどうかも確認。
#     """
#     solutions = []
#     solve_sudoku_all_2d(board, solutions, max_solutions=2)
#     if len(solutions) == 0:
#         print("解なし")
#     elif len(solutions) == 1:
#         print("唯一解: ")
#         for row in solutions[0]:
#             print(row)
#     else:
#         print("複数解あり:")
#         for solution in solutions:
#             print("解:")
#             for row in solution:
#                 print(row)
#             print()
#     #解が複数ある場合or解がないにはfalse,解が唯一解の場合にはtrueとsolutionsを返す
#     return len(solutions) == 1, solutions


def find_best_cell(board):
    """候補が最も少ないセルを探す"""
    min_options = 10  # 最大9なので、初期値を10に設定
    best_cell = None

    for row in range(9):
        for col in range(9):
            if board[row, col] == 0:
                options = sum(1 for num in range(1, 10) if is_valid_2d(board, row, col, num))
                if options == 0:
                    return None
                if options < min_options:
                    min_options = options
                    best_cell = (row, col)
    return best_cell

def solve_sudoku_fast(board):
    """高速なナンプレ解法"""
    # すべてのセルが埋まっているか確認
    if all(board[row, col] != 0 for row in range(9) for col in range(9)):
        return board  # すべてのセルが埋まっている場合にboardを返す
    
    cell = find_best_cell(board)
    if not cell:
        return None  # 解けない場合はNoneを返す

    row, col = cell
    for num in range(1, 10):
        if is_valid_2d(board, row, col, num):
            board[row, col] = num
            result = solve_sudoku_fast(board)  # 再帰的に解を探索
            if result is not None:  # 解が見つかった場合
                return result
            board[row, col] = 0  # バックトラック

    return None  # 解なし（解けなかった場合）


# テスト問題（2次元リスト形式）
# problem_2d = [
#     [8, 0, 0, 0, 0, 0, 0, 0, 5],
#     [0, 0, 6, 8, 0, 7, 4, 0, 0],
#     [0, 4, 0, 0, 6, 0, 0, 2, 0],
#     [0, 5, 0, 0, 0, 0, 0, 3, 0],
#     [0, 0, 2, 0, 0, 0, 7, 0, 0],
#     [0, 7, 0, 0, 0, 0, 0, 8, 0],
#     [0, 9, 0, 0, 8, 0, 0, 6, 0],
#     [0, 0, 1, 7, 0, 2, 5, 0, 0],
#     [7, 0, 0, 0, 0, 0, 0, 0, 3],
# ]

# problem_2d = [
#     [7, 0, 0, 0, 0, 0, 0, 0, 5],
#     [0, 0, 9, 8, 0, 5, 1, 0, 0],
#     [0, 2, 0, 0, 1, 0, 0, 6, 0],
#     [0, 7, 0, 0, 0, 0, 0, 4, 0],
#     [0, 0, 6, 0, 0, 0, 7, 0, 0],
#     [0, 9, 0, 0, 0, 0, 0, 5, 0],
#     [0, 6, 0, 0, 3, 0, 0, 8, 0],
#     [0, 0, 8, 1, 0, 4, 5, 0, 0],
#     [3, 0, 0, 0, 0, 0, 0, 0, 1],
# ]

# 実行
# solve_sudoku_wrapper_2d(problem_2d)
# print(not None)
# print(solve_sudoku_fast(np.array(problem_2d)))