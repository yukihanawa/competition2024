import numpy as np
import random
import solve_suudoku_2d

HINT_PATTERN = [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
# HINT_PATTERN = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# 問題の整合性を確認
def check_problem(problem, a):
    problem = problem.reshape(9, 9)  # 9×9の形式に変換
    for row in range(9):
        for col in range(9):
            if problem[row][col] != 0:  # 既に埋まっているセルを確認
                temp_value = problem[row][col]  # 現在の値を保存
                problem[row][col] = 0  # 一時的に0に設定
                # 有効性をチェック
                if not solve_suudoku_2d.is_valid_2d(problem, row, col, temp_value):
                    print(f"問題の整合性が取れていません: {a}")
                    problem[row][col] = temp_value  # 元の値に戻す
                    print(problem.reshape(9, 9))
                    return False
                problem[row][col] = temp_value  # 元の値に戻す
    return True

def create_first_answer():
    answer = np.zeros((9, 9), dtype=int)
    for i in range(9):
        for j in range(9):
            a = i + j +1
            if(a <= 9):
                answer[i][j] = i + j + 1
            else:
                answer[i][j] = a % 9
    #２列目と4列目を入れ替える
    answer[:,1], answer[:,3] = answer[:,3].copy(), answer[:,1].copy()
    #３列目と7列目を入れ替える
    answer[:,2], answer[:,6] = answer[:,6].copy(), answer[:,2].copy()
    #6列目と8列目を入れ替える
    answer[:,5], answer[:,7] = answer[:,7].copy(), answer[:,5].copy()

    return answer

#1~3行目、4~6行目、7~9行目からランダムに2つ選び、３行をまとめて入れ替える
def change_row_block(answer):
    a = random.randint(1, 3)
    b = random.randint(1, 3)
    if a == b:
        change_row_block(answer)
    else:
        answer[(a-1)*3:a*3,:], answer[(b-1)*3:b*3,:] = answer[(b-1)*3:b*3,:].copy(), answer[(a-1)*3:a*3,:].copy()
    return answer

#1~3列目、4~6列目、7~9列目からランダムに2つ選び、３列をまとめて入れ替える
def change_column_block(answer):
    a = random.randint(1, 3)
    b = random.randint(1, 3)
    if a == b:
        change_column_block(answer)
    else:
        answer[:,(a-1)*3:a*3], answer[:,(b-1)*3:b*3] = answer[:,(b-1)*3:b*3].copy(), answer[:,(a-1)*3:a*3].copy()
    return answer

# 1~3行目or4~6行目or7~9行目の中で行を入れ替える（ランダム）
def change_row(answer):
    # 1~3, 4~6, 7~9のいずれかのブロックをランダムに選ぶ
    block = random.randint(1, 3)
    
    # 同じブロック内で行を選んで入れ替え
    row_indices = range((block-1)*3, block*3)  # 対象となる行ブロックのインデックス
    a, b = random.sample(row_indices, 2)  # 同じブロック内で異なる行をランダムに選ぶ
    
    # 行を入れ替える
    answer[a, :], answer[b, :] = np.copy(answer[b, :]), np.copy(answer[a, :])

    return answer

# 1~3列目or4~6列目or7~9列目の中で列を入れ替える（ランダム）
def change_column(answer):
    # 1~3, 4~6, 7~9のいずれかの列ブロックをランダムに選ぶ
    block = random.randint(1, 3)
    
    # 同じブロック内で列を選んで入れ替え
    col_indices = range((block-1)*3, block*3)  # 対象となる列ブロックのインデックス
    a, b = random.sample(col_indices, 2)  # 同じブロック内で異なる列をランダムに選ぶ
    
    # 列を入れ替える
    answer[:, a], answer[:, b] = np.copy(answer[:, b]), np.copy(answer[:, a])

    return answer


def create_answer():
    answer = create_first_answer()
    for i in range(20):
        
        answer = change_row_block(answer)

        answer = change_column_block(answer)
    
        answer = change_row(answer)
    
        answer = change_column(answer)
    return answer.flatten()

def mutate(answer):
    if(check_problem(answer, "突然変異") == False):
        print("突然変異前のanswer:",answer)
    else:
        A = 1
    answer = answer.reshape(9, 9)
    answer = solve_suudoku_2d.solve_sudoku_fast(answer)
    if(answer is None):
        # print("1解が見つかりませんでした")
        answer = create_answer()
    else:
        # print("突然変異させる前のanswer:")
        # print(answer)
        for i in range(10):
            if random.random() < 0.5:
                # print("突然変異：１")
                answer = change_row_block(answer)
            if random.random() < 0.5:
                # print("突然変異：２")
                answer = change_column_block(answer)
            if random.random() < 0.5:
                # print("突然変異：３")
                answer = change_row(answer)
            if random.random() < 0.5:
                # print("突然変異：４")
                answer = change_column(answer)
        # print("突然変異させた後のanswer:")
        # print(answer)
    answer = answer.flatten()*HINT_PATTERN
    if(A == 1):
        if(check_problem(answer, "突然変異") == False):
            print("突然変異後のanswer:",answer)
    return answer