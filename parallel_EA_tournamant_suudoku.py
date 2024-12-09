import parallel_create_suudou_ver1 as create
import evaluate_suudoku
import crossover_hint
import solve_suudoku_2d
import _find_all
import numpy as np
import random
from concurrent.futures import ThreadPoolExecutor

HINT_PATTERN = [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
# HINT_PATTERN = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

population = 20 #個体数
max_generation = 40 #最大世代数
cr = 0.7 #交叉率
cn = 2 * round(cr * population/2) #交叉数
mr = 0.3 #突然変異率
# print("cn:",cn//2)
tournament_size = 4
replace_ratio = 2/3
#問題の整合性を確認
# 問題の整合性を確認
def check_problem(answer, a):
    for i in range(answer.shape[0]):
        problem = answer[i, :].reshape(9, 9)  # 9×9の形式に変換
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

#81要素のリストを9×9行列に変換
def convert_1d_to_2d(board):
    return np.array(board).reshape(9, 9)

def tournament_selection(answer, evaluation, tournament_size):
    selected_index = []
    for i in range(population):
        index = np.random.choice(population, tournament_size, replace=False)
        selected_index.append(index[np.argmin(evaluation[index])])
    return answer[selected_index,:], evaluation[selected_index]

# 並列化するタスクの定義
def process_replace_task(idx, HINT_PATTERN):
    # 個別のインデックスに対する処理
    temp_answer = create.create_answer()
    repaired_answer, _ = create.repair(temp_answer, np.array(HINT_PATTERN))
    evaluation_score = evaluate_suudoku.evaluate_sudoku_2d_strict(
        convert_1d_to_2d(np.array(repaired_answer) * HINT_PATTERN)
    )
    return idx, repaired_answer, evaluation_score

# 並列化のメイン部分
def parallel_replace(replace_indices, HINT_PATTERN, answer, evaluation):
    with ThreadPoolExecutor() as executor:
        # タスクを並列実行
        futures = [
            executor.submit(process_replace_task, idx, HINT_PATTERN)
            for idx in replace_indices
        ]
        # 結果を収集
        for future in futures:
            idx, repaired_answer, evaluation_score = future.result()
            # 結果を answer と evaluation に書き込み
            answer[idx, :] = repaired_answer
            evaluation[idx] = evaluation_score
    return answer, evaluation

#各個体は81要素のリストで表現される
#1世代の個体数は20
#初期解生成
if __name__ == "__main__":
    answer = np.zeros((population,81), dtype=int)

    answer = create.parallel_execution(population,np.array(HINT_PATTERN))

    # print("初期解")
    # for i in range(population):
    #     print(np.unique(answer[i,:]*HINT_PATTERN))

    #初期解の評価
    evaluation = np.zeros(population, dtype=int)
    for i in range(population):
        evaluation[i] = evaluate_suudoku.evaluate_sudoku_2d_strict(convert_1d_to_2d(answer[i,:]*HINT_PATTERN))



    # for i in range(population):
    #     print("evaluation[",i,"]=",evaluation[i])

    #評価値の低い順にソート
    index = np.argsort(evaluation)
    answer = answer[index,:]
    evaluation = evaluation[index]

    check_problem(answer, "初期解")

    #新たな解を作成し、その評価値が親より高い場合には置き換える
    #親の評価値が最も高いものを選ぶ
    for i in range(max_generation):
        print("generation[",i,"]")

        if np.all(evaluation == evaluation[0]):
            print("すべて同じ評価値のため一部個体を新規作成")
            num_replace = int(population - 2)
            replace_indices = np.random.choice(population, num_replace, replace=False)
            answer, evaluation = parallel_replace(replace_indices, HINT_PATTERN, answer, evaluation)
            
        
        #トーナメント選択
        selected_answer, selected_evaluation = tournament_selection(answer, evaluation, tournament_size)

        #交叉させる個体
        answer_cross = selected_answer[0:cn,:].copy()
        evaluation_cross = selected_evaluation[0:cn].copy()
        answer_mutate = answer[cn:,:].copy()
        evaluation_mutate = evaluation[cn:].copy()
        # print("cossover:",i)
        #交叉
        for j in range(0, cn//2):
            answer_cross[2*j,:], answer_cross[2*j + 1,:], evaluation_cross[2*j], evaluation_cross[2*j+1] = crossover_hint.crossover(answer_cross[2*j,:], answer_cross[2*j+1,:], evaluation_cross[2*j], evaluation_cross[2*j+1])
            for k in range(81):
                if HINT_PATTERN[k] == 1 and answer_cross[j,k] == 0:
                    print("正しく交叉されていません")
        
        check_problem(answer_cross, "交叉")
        
        # print("mutate:",i)
        #突然変異
        for j in range(population - cn):
            answer_mutate[j,:] = create.mutate(answer_mutate[j,:])
            # print("finish mutate")
            # print("answer_mutate[:,j]:",answer_mutate[j,:])
            evaluation_mutate[j] = evaluate_suudoku.evaluate_sudoku_2d_strict(convert_1d_to_2d(answer_mutate[j,:]*HINT_PATTERN))
            # print("finish evaluate_mutate")
            for k in range(81):
                if HINT_PATTERN[k] == 1 and answer_mutate[j,k] == 0:
                    print("正しく突然変異されていません")
        # print("突然変異終了")
        check_problem(answer_mutate, "突然変異")

        #交叉と突然変異で生成した個体を結合 + 親
        answer = np.vstack((answer_cross, answer_mutate, answer))
        evaluation = np.hstack((evaluation_cross, evaluation_mutate, evaluation))

        # #すべての個体を表示
        # print("generation[",i,"]が終わった")
        print(evaluation)
        # for j in range(population * 2):
        #     print(evaluation[j])


        #評価値の低い順にソート
        index = np.argsort(evaluation)
        index = index[0:population]
        # print("index:",index)
        answer = answer[index,:]
        evaluation = evaluation[index]


        
        print("best_parent_eval[",i,"]=",evaluation[0])
        print("list of evaluation:")
        print(evaluation)



    #最も評価値が高い解を出力
    print(answer[0,:].reshape(9, 9))
    print(evaluation[0])
# print("評価値が最も高い解")
# print((np.array(answer[0,:] * HINT_PATTERN)).reshape(9, 9))
# a = find_all.solve_sudoku(convert_1d_to_2d(answer[0,:] * HINT_PATTERN))
# find_all.print_solutions(a)