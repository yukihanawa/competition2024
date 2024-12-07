import numpy as np
import random
import solve_suudoku_2d

HINT_PATTERN = [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]

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
        answer = repair(answer, HINT_PATTERN)

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

# ナンプレの盤面に対して可能な解の数を計算する
def count_solutions(sudoku, limit=1e30):
    #各セルに関連する行、列、ブロックのセルを特定し、その位置を記録する
    def relation_listup():
        r = [[] for _ in range(81)] #空のリストを８１個用意する
        for i in range(81):
            x,y = i//9, i%9
            r[i].extend(list(range(y, y+81, 9)))#同じ列をリストについか
            r[i].extend(list(range(9*x, 9*x+9)))#同じ行をリストに追加
            base_x, base_y = x//3*3, y//3*3
            #3*3のブロック内のセルをリストに追加
            r[i].extend(list(range(base_x*9+base_y, base_x*9+base_y+3)))
            r[i].extend(list(range(base_x*9+base_y+9, base_x*9+base_y+12)))
            r[i].extend(list(range(base_x*9+base_y+18, base_x*9+base_y+21)))
        #重複を取り除き、セルの番号を昇順に並べる
        for i in range(81):
            r[i] = sorted(list(set(r[i])))
        return r

    cell_relationship = relation_listup()
    #各セルに入れられる数字の候補をリストアップする
    insertable = [list(range(1,10)) for _ in range(81)]
    #各セルの関連セルに入っている数字を候補から除外する
    for i in range(81):
        for cell in cell_relationship[i]:
            if sudoku[cell] in insertable[i]:
                insertable[i].remove(sudoku[cell])

    #最も候補の少ないセルを探す
    tmp_min = 10
    for i in range(81):
        if sudoku[i] == 0 and len(insertable[i]) < tmp_min:
            tmp_min = len(insertable[i])
            insert_num = insertable[i]
            insert_pos = i

    zeros = sudoku.count(0)
    stack = [(True, insert_pos, i,[], zeros) for i in insert_num] #初期状態として候補の少ないセルの候補を入れる

    cnt = 0
    tmp_solution = None
    while stack:
        pre_order, insert_pos, insert_num, restore, zeros = stack.pop()
        #数字をセルに挿入し、盤面が完成したかどうかを確認する
        if pre_order:
            sudoku[insert_pos] = insert_num
            if zeros == 1:
                if tmp_solution is None:
                    tmp_solution = sudoku.copy()
                cnt += 1
                if cnt > limit:
                    return cnt, tmp_solution
            #挿入した数字の影響を受けるセルの候補から挿入した数字を除外する
            for cell in cell_relationship[insert_pos]:
                if insert_num in insertable[cell]:
                    insertable[cell].remove(insert_num)
                    restore.append(cell)
            tmp_min = 10
            for i in range(81):
                if sudoku[i] == 0 and len(insertable[i]) < tmp_min:
                    tmp_min = len(insertable[i])
                    next_insert_num = insertable[i]
                    next_insert_pos = i
            stack.append((False, insert_pos, insert_num, restore, zeros+1))
            stack.extend([(True, next_insert_pos, nin,[], zeros-1) for nin in next_insert_num])
        else:
            sudoku[insert_pos] = 0
            for r in restore:
                insertable[r].append(insert_num)
    return cnt, tmp_solution

def swap(answer, hint_pattern):
    # squared_answer = answer.reshape(9, 9)
    masked = answer * hint_pattern
    num_counts = [np.sum(masked == i) for i in range(1, 10)] # 1~9の数字の出現回数を数える
    # 1個以上あるものからランダムに選択
    #idx = [i for i in range(9) if num_counts[i] > 0]
    #rand_num = np.random.choice(idx) + 1
    #max_num = rand_num
    
    # 一番多い数字
    max_num = np.argmax(num_counts) + 1
    squared = masked.reshape(9, 9)
    # squaredのなかで行にも列にもmax_numを含まない行列を探す
    row_cols = []
    for row in range(9):
        for col in range(9):
            if squared[row, col] == 0:
                continue
            if squared[row, :].tolist().count(max_num) == 0 and squared[:, col].tolist().count(max_num) == 0: # 行にも列にもmax_numを含まない
                row_cols.append((row, col))
    inversed = answer * (1 - np.array(hint_pattern)) # ヒント以外のセル
    inversed_squared = inversed.reshape(9, 9)
    # ヒント以外のセルのなかで行にも列にもmax_numを含む行と列を探す
    row_cols2 = []
    for row in range(9):
        for col in range(9):
            if inversed_squared[row, col] == 0:
                continue
            if inversed_squared[row, :].tolist().count(max_num) == 1 and inversed_squared[:, col].tolist().count(max_num) == 1:
                row_cols2.append((row, col))
    # print(row_cols, row_cols2)
    s = input()
    applied = False
    if len(row_cols) == 0:
        return answer, applied
    rand_idx = np.random.randint(len(row_cols))
    for row, col in row_cols[rand_idx:]:
        # row_cols2からランダムに選ぶ
        if len(row_cols2) == 0:
            break
        rand_idx2 = np.random.randint(len(row_cols2))
        row2, col2 = row_cols2[rand_idx2]
        # rand_idx2を削除
        row_cols2.pop(rand_idx2)
        if np.random.random() < 0.5:
            # colを交換
            # 同じブロックにある場合
            if row//3 == row2//3:
                squared[row, :], squared[row2, :] = squared[row2, :].copy(), squared[row, :].copy()
            else:
                # ブロックごと交換
                row_block_begin = row//3*3
                row_block_end = row_block_begin + 3
                row2_block_begin = row2//3*3
                row2_block_end = row2_block_begin + 3
                squared[row_block_begin:row_block_end, :], squared[row2_block_begin:row2_block_end, :] = squared[row2_block_begin:row2_block_end, :].copy(), squared[row_block_begin:row_block_end, :].copy()
            applied = True
        else:
            # rowを交換
            # 同じブロックにある場合
            if col//3 == col2//3:
                squared[:, col], squared[:, col2] = squared[:, col2].copy(), squared[:, col].copy()
            else:
                # ブロックごと交換
                col_block_begin = col//3*3
                col_block_end = col_block_begin + 3
                col2_block_begin = col2//3*3
                col2_block_end = col2_block_begin + 3
                squared[:, col_block_begin:col_block_end], squared[:, col2_block_begin:col2_block_end] = squared[:, col2_block_begin:col2_block_end].copy(), squared[:, col_block_begin:col_block_end].copy()
            applied = True
        break
    return squared.flatten(), applied
        
def repair(answer, hint_pattern):
    hint_pattern = np.array(hint_pattern)
    for _ in range(10):
        masked = answer * hint_pattern
        cnt, _ = count_solutions(list(masked))
        # print(cnt)
        best_answer = answer.copy()
        best_masked = masked.copy()
        for _ in range(100):
            # HINT_PATTERN==1のインデックスをランダムに選択
            rand_idx = np.random.choice(np.where(hint_pattern == 1)[0])
            for i in range(1, 10):
                tmp_masked = masked.copy()
                if tmp_masked[rand_idx] == i:
                    continue
                tmp_masked[rand_idx] = i
                new_cnt, tmp_sudoku = count_solutions(list(tmp_masked), limit=cnt)
                if 0 < new_cnt < cnt:
                    best_answer = tmp_sudoku 
                    best_masked = tmp_masked.copy()
                    cnt = new_cnt
                    # print(cnt)
            masked = best_masked.copy()
            if cnt == 1:
                break
        if cnt == 1:
            break
    best_answer = [int(x) for x in best_answer]
    return best_answer, cnt

# if __name__ == "__main__":
#     random.seed(0)
#     best_answers = []
#     for _ in range(10):
#         answer = create_answer()
#         HINT_PATTERN = np.array([1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1])
#         best_answer, cnt = repair(answer, HINT_PATTERN)
#         best_answers.append((best_answer, cnt))
#     for best_answer, cnt in best_answers:
#         print(best_answer, cnt)
#         for row in range(9):
#             for col in range(9):
#                 print(best_answer[row*9+col], end=' ')
#             print()
#         print()
#         best_masked = best_answer * HINT_PATTERN
#         for row in range(9):
#             for col in range(9):
#                 print(best_masked[row*9+col], end=' ')
#             print()
            

from concurrent.futures import ThreadPoolExecutor

def process_task(i, HINT_PATTERN):
    temp_answer = create_answer()
    repaired_answer, _ = repair(temp_answer, HINT_PATTERN)
    return repaired_answer

# 並列化する部分
def parallel_execution(population, HINT_PATTERN):
    answer = np.zeros((population, 81))  # answer_size は問題に応じて指定
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda i: process_task(i, HINT_PATTERN), range(population)))
    
    for i, result in enumerate(results):
        answer[i, :] = result
    return answer

answer = parallel_execution(20, HINT_PATTERN)
for i in range(20):
    print(answer[i].reshape(9, 9))