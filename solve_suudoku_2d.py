def solve_sudoku_all_2d(board, solutions, max_solutions=2):
    """
    2次元リスト形式の数独ソルバー。
    """
    # 空きマスを探す
    empty = find_empty_2d(board)
    if not empty:
        # 解が見つかったら保存
        solutions.append([row[:] for row in board])  # 盤面をコピー
        return len(solutions) >= max_solutions

    row, col = empty

    # 数字1～9を試す
    for num in range(1, 10):
        if is_valid_2d(board, row, col, num):
            board[row][col] = num  # 数字を仮置き
            if solve_sudoku_all_2d(board, solutions, max_solutions):
                return True  # 必要な解が見つかったら終了
            board[row][col] = 0  # 戻す（バックトラッキング）

    return False


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


def solve_sudoku_wrapper_2d(board):
    """
    2次元リスト形式の数独ソルバーのラッパー関数。
    - 解を求めるとともに複数解かどうかも確認。
    """
    solutions = []
    solve_sudoku_all_2d(board, solutions, max_solutions=2)
    if len(solutions) == 0:
        print("解なし")
    elif len(solutions) == 1:
        print("唯一解: ")
        for row in solutions[0]:
            print(row)
    else:
        print("複数解あり:")
        for solution in solutions:
            print("解:")
            for row in solution:
                print(row)
            print()
    #解が複数ある場合or解がないにはfalse,解が唯一解の場合にはtrueとsolutionsを返す
    return len(solutions) == 1, solutions


# テスト問題（2次元リスト形式）
problem_2d = [
    [2, 0, 0, 0, 0, 0, 0, 0, 9],
    [0, 0, 6, 8, 0, 7, 4, 0, 0],
    [0, 4, 0, 0, 6, 0, 0, 2, 0],
    [0, 5, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 2, 0, 0, 0, 7, 0, 0],
    [0, 7, 0, 0, 0, 0, 0, 8, 0],
    [0, 9, 0, 0, 8, 0, 0, 6, 0],
    [0, 0, 1, 7, 0, 2, 5, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 3],
]

# 実行
# solve_sudoku_wrapper_2d(problem_2d)