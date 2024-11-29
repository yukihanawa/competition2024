import numpy as np
import random
HINT_PATTERN = [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]

def is_valid(board, row, col, num):
    """数独の盤面で指定した位置に数値を置くことが有効か確認します。"""
    if num in board[row, :] or num in board[:, col]:
        return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[start_row:start_row+3, start_col:start_col+3]:
        return False

    return True

def solve_sudoku(board, solutions):
    """バックトラック法で数独を解き、すべての解をリストに追加します。"""
    for row in range(9):
        for col in range(9):
            if board[row, col] == 0:  # 空きセルを見つけた場合
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row, col] = num
                        solve_sudoku(board, solutions)
                        board[row, col] = 0  # 戻す（バックトラック）
                return  # 他の可能性を試すために戻る
    solutions.append(board.copy())

def choose_non_overlapping_numbers_and_positions(parent1, parent2):
    """位置が被らない数値ペアを選択し、それぞれの位置情報を返します。"""
    nums = list(range(1, 10))
    random.shuffle(nums)
    for num1 in nums:
        for num2 in nums:
            if num1 != num2:  # 数値が異なる
                indices_p1 = np.argwhere(parent1 == num1)
                indices_p2 = np.argwhere(parent2 == num2)
                # 位置が重ならないかチェック
                overlap = any((i1 == i2).all() for i1 in indices_p1 for i2 in indices_p2)
                if not overlap:
                    return num1, num2, indices_p1, indices_p2
    raise ValueError("適切な数値ペアが見つかりませんでした。")

def crossover_with_non_overlapping_numbers(parent1, parent2):
    """親1と親2から位置が被らない数値ペアを選び、子供を生成します。"""
    # 初期化
    child = np.zeros((9, 9), dtype=int)
    parent1 = np.array(parent1).reshape(9, 9)
    parent2 = np.array(parent2).reshape(9, 9)

    # 被らない数値ペアとその位置を選択
    num1, num2, indices_p1, indices_p2 = choose_non_overlapping_numbers_and_positions(parent1, parent2)

    # 親1からnum1の位置を引き継ぎ
    for row, col in indices_p1:
        child[row, col] = num1

    # 親2からnum2の位置を引き継ぎ
    for row, col in indices_p2:
        child[row, col] = num2

    # バックトラック法で残りを埋める
    solutions = []
    solve_sudoku(child, solutions)
    return solutions, num1, num2

# サンプル親個体（完全に埋まった数独）
parent1 = [
    5, 3, 4, 6, 7, 8, 9, 1, 2,
    6, 7, 2, 1, 9, 5, 3, 4, 8,
    1, 9, 8, 3, 4, 2, 5, 6, 7,
    8, 5, 9, 7, 6, 1, 4, 2, 3,
    4, 2, 6, 8, 5, 3, 7, 9, 1,
    7, 1, 3, 9, 2, 4, 8, 5, 6,
    9, 6, 1, 5, 3, 7, 2, 8, 4,
    2, 8, 7, 4, 1, 9, 6, 3, 5,
    3, 4, 5, 2, 8, 6, 1, 7, 9
]

parent2 = [
    8, 2, 7, 1, 5, 4, 3, 9, 6,
    9, 6, 5, 3, 2, 7, 1, 4, 8,
    3, 4, 1, 6, 8, 9, 7, 5, 2,
    5, 9, 3, 4, 6, 8, 2, 7, 1,
    4, 7, 2, 5, 1, 3, 6, 8, 9,
    6, 1, 8, 9, 7, 2, 4, 3, 5,
    7, 8, 6, 2, 3, 5, 9, 1, 4,
    1, 5, 4, 7, 9, 6, 8, 2, 3,
    2, 3, 9, 8, 4, 1, 5, 6, 7
]

# 新しい子供の解を生成
solutions, num1, num2 = crossover_with_non_overlapping_numbers(parent1, parent2)

# 結果表示
print(f"Numbers chosen: Parent1 -> {num1}, Parent2 -> {num2}")
print(f"Found {len(solutions)} solutions.")
for i, solution in enumerate(solutions, 1):
    print(f"Solution {i}:\n{solution}")