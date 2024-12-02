import solve_suudoku_2d

def evaluate_sudoku_2d_strict(board):
    """
    空白マスを評価に含めず、候補数とバックトラッキング深さに基づいて評価する。
    複数解が存在する場合、大きなペナルティを与える。
    """
    max_depth = [0]  # 最大バックトラッキング深さを記録する

    def find_best_cell(board):
        """
        候補が最も少ない空セルを探す。
        """
        min_options = 10  # 候補の最大数+1
        best_cell = None

        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    options = sum(1 for num in range(1, 10) if solve_suudoku_2d.is_valid_2d(board, row, col, num))
                    if options < min_options:
                        min_options = options
                        best_cell = (row, col)
                        if min_options == 1:  # 候補が1つのセルは最適なので探索を終了
                            break
        return best_cell

    def solve_and_track_depth(board, depth=0):
        """
        数独を解きながらバックトラッキングの深さを記録する。
        ヒューリスティクスを用いたセル選択を適用。
        """
        # 候補が最も少ない空セルを探す
        empty = find_best_cell(board)
        if not empty:
            return 1  # 解を1つ見つけた

        row, col = empty
        solutions = 0

        for num in range(1, 10):
            if solve_suudoku_2d.is_valid_2d(board, row, col, num):
                board[row][col] = num
                max_depth[0] = max(max_depth[0], depth + 1)  # 深さを更新
                if max_depth[0] > 100:
                    print("バックトラックが100を超えました。")
                solutions += solve_and_track_depth(board, depth + 1)
                board[row][col] = 0  # バックトラック

                # 複数解をチェックするために早期終了
                if solutions > 1:
                    return solutions

        return solutions

    # 唯一解か複数解かチェックし、バックトラッキング深さを記録
    solutions = solve_and_track_depth([row[:] for row in board])

    # 評価値を計算
    evaluation = (
         - max_depth[0] * 5  # バックトラッキング深さに基づく重み
        - (10000 if solutions > 1 else 0)  # 複数解なら大きなペナルティ
    )

    return evaluation


# テスト問題
# problem_2d = [
#     [8, 0, 0, 0, 0, 0, 0, 0, 9],
#     [0, 0, 6, 8, 0, 7, 4, 0, 0],
#     [0, 4, 0, 0, 6, 0, 0, 2, 0],
#     [0, 5, 0, 0, 0, 0, 0, 3, 0],
#     [0, 0, 2, 0, 0, 0, 7, 0, 0],
#     [0, 7, 0, 0, 0, 0, 0, 8, 0],
#     [0, 9, 0, 0, 8, 0, 0, 6, 0],
#     [0, 0, 1, 7, 0, 2, 5, 0, 0],
#     [7, 0, 0, 0, 0, 0, 0, 0, 3],
# ]

# 評価関数を実行
# evaluation, details = evaluate_sudoku_2d_strict(problem_2d)

# print("評価値:", evaluation)
# print("詳細:", details)