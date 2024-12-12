import solve_suudoku_2d
import numpy as np
from opthub_client.api import OptHub
import json

# def evaluate_sudoku_2d_strict(board):
#     """
#     空白マスを評価に含めず、候補数とバックトラッキング深さに基づいて評価する。
#     複数解が存在する場合、大きなペナルティを与える。
#     """
#     max_depth = [0]  # 最大バックトラッキング深さを記録する

#     def find_best_cell(board):
#         """
#         候補が最も少ない空セルを探す。
#         """
#         min_options = 10  # 候補の最大数+1
#         best_cell = None

#         for row in range(9):
#             for col in range(9):
#                 if board[row][col] == 0:
#                     options = sum(1 for num in range(1, 10) if solve_suudoku_2d.is_valid_2d(board, row, col, num))
#                     if options < min_options:
#                         min_options = options
#                         best_cell = (row, col)
#                         if min_options == 1:  # 候補が1つのセルは最適なので探索を終了
#                             break
#         return best_cell

#     def solve_and_track_depth(board, depth=0):
#         """
#         数独を解きながらバックトラッキングの深さを記録する。
#         ヒューリスティクスを用いたセル選択を適用。
#         """
#         # 候補が最も少ない空セルを探す
#         empty = find_best_cell(board)
#         if not empty:
#             return 1  # 解を1つ見つけた

#         row, col = empty
#         solutions = 0

#         for num in range(1, 10):
#             if solve_suudoku_2d.is_valid_2d(board, row, col, num):
#                 board[row][col] = num
#                 max_depth[0] = max(max_depth[0], depth + 1)  # 深さを更新
#                 # if max_depth[0] > 100:
#                 #     print("バックトラックが100を超えました。")
#                 solutions += solve_and_track_depth(board, depth + 1)
#                 board[row][col] = 0  # バックトラック

#                 # 複数解をチェックするために早期終了
#                 if solutions > 1:
#                     return solutions

#         return solutions

#     # 唯一解か複数解かチェックし、バックトラッキング深さを記録
#     solutions = solve_and_track_depth([row[:] for row in board])

#     # 評価値を計算
#     evaluation = (
#          max_depth[0] * 5  # バックトラッキング深さに基づく重み
#         + (10000 if solutions > 1 else 0)  # 複数解なら大きなペナルティ
#         + (20000 if solutions == 0 else 0)  # 解なしもペナルティ
#     )

#     return evaluation, solutions

# テスト問題
sample = [
    # [0, 0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 5, 3, 0, 7, 6, 0, 0],
    # [0, 1, 0, 0, 8, 0, 0, 9, 0],
    # [0, 7, 0, 0, 0, 0, 0, 2, 0],
    # [0, 0, 6, 0, 0, 0, 1, 0, 0],
    # [0, 0, 3, 0, 0, 0, 4, 0, 0],
    # [0, 9, 0, 0, 0, 0, 0, 5, 0],
    # [0, 6, 0, 0, 2, 0, 0, 3, 0],
    # [0, 0, 0, 4, 7, 0, 8, 1, 0]

    [8, 0, 0, 0, 0, 0, 0, 0, 9],
    [0, 0, 6, 8, 0, 7, 4, 0, 0],
    [0, 4, 0, 0, 6, 0, 0, 2, 0],
    [0, 5, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 2, 0, 0, 0, 7, 0, 0],
    [0, 7, 0, 0, 0, 0, 0, 8, 0],
    [0, 9, 0, 0, 8, 0, 0, 6, 0],
    [0, 0, 1, 7, 0, 2, 5, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 3],

]

def is_valid_2d(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def find_best_cell(board):
    min_options = 10
    best_cell = None
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                options = sum(1 for num in range(1, 10) if is_valid_2d(board, row, col, num))
                if options < min_options:
                    min_options = options
                    best_cell = (row, col)
                    if min_options == 1:
                        return best_cell
    return best_cell

def solve_and_track_depth(board):
    empty = find_best_cell(board)
    if not empty:
        return 1
    row, col = empty
    solutions = 0
    for num in range(1, 10):
        if is_valid_2d(board, row, col, num):
            board[row][col] = num
            solutions += solve_and_track_depth(board.copy())
            board[row][col] = 0
            if solutions > 4:
                return solutions
    return solutions

def count_different_cells(original, solved):
    """元の盤面と解いた盤面の異なるマス目をカウント"""
    diff_count = 0
    for row in range(9):
        for col in range(9):
            if original[row][col] != solved[row][col]:
                diff_count += 1
    return diff_count

#マンハッタン距離
def manhattan_distance(original,solved):
    distance = 0
    for row in range(9):
        for col in range(9):
            distance += abs(original[row][col] - solved[row][col])
    return distance

def evaluate_sudoku_2d_strict(original_board):
    # print("board:", np.array(original_board, dtype = int).flatten())
    board = [row[:] for row in original_board]
    # solutions = solve_and_track_depth(board)
    
    # if solutions == 0:
    #     return 10000  # 解なし
    # elif solutions == 1:
    #     return 1 + count_different_cells(sample, board) # ユニークな解
    # else:
    #     return 100 * solutions + count_different_cells(sample, board)
    return manhattan_distance(sample, board) + 1000 * (solve_and_track_depth(board) - 1)

# def evaluate_sudoku_2d_strict(board):
#     with OptHub("ohxmuBTKjB6wzMYVSvliy5WSJIU0Efw66wHBkpOc") as api:
#         opthub_match = api.match("726c509c-4831-47bc-8d8a-d79b52f2cedf")
#         trial = opthub_match.submit(np.array(board, dtype = int).flatten())

#         eval = trial.wait_evaluation()
#         if(eval.error == None):
#             if(eval.feasible):
#                 evaluation = eval.ojective.scalar
#             else:
#                 evaluation = 10
#         else:
#             print("error")
#             evaluation = 10

#     return evaluation
    
# evaluate_opthub(sample)


# problem_2d = [
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
# problem_2d = [
#     [8, 0, 0, 0, 0, 0, 0, 0, 7],
#     [0, 0, 9, 3, 0, 2, 6, 0, 0],
#     [0, 6, 0, 0, 4, 0, 0, 5, 0],
#     [0, 2, 0, 0, 0, 0, 0, 9, 0],
#     [0, 0, 1, 0, 0, 0, 7, 0, 0],
#     [0, 4, 0, 0, 0, 0, 0, 7, 0],
#     [0, 1, 0, 0, 9, 0, 0, 3, 0],
#     [0, 0, 6, 1, 0, 7, 4, 0, 0],
#     [9, 0, 0, 0, 0, 0, 0, 0, 1]
# ]

# print(count_different_cells(sample, problem_2d))
# 評価関数を実行
# evaluation = evaluate_sudoku_2d_strict(problem_2d)

# print("評価値:", evaluation)
# # print("詳細:", details)
# print("解の数:", solutions)