import parallel_create_suudou_ver1 as create
import evaluate_suudoku
import crossover_hint
import solve_suudoku_2d
import _find_all
import numpy as np
import random
from concurrent.futures import ProcessPoolExecutor

HINT_PATTERN = [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
# HINT_PATTERN = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

population = 20 #個体数
max_generation = 50 #最大世代数
cr = 0.7 #交叉率
cn = 2 * round(cr * population/2) #交叉数
mr = 0.3 #突然変異率
# print("cn:",cn//2)
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

def parallel_evaluation(args):
        i, answer, hint_pattern = args
        return evaluate_suudoku.evaluate_sudoku_2d_strict(convert_1d_to_2d(answer[i, :] * hint_pattern))

def eval_pop_in_parallel(answer,hint_pattern):
    evaluation_ = np.zeros(population)  # 結果を格納する配列
    with ProcessPoolExecutor() as executor:
        args = [(i, answer, hint_pattern)for i in range(population)]
        results = list(executor.map(parallel_evaluation, args))
    evaluation_[:] = results
    return evaluation_

def parallel_crossover(args):
    j, answer_cross, evaluation_cross, hint_pattern = args
    # 2つの親を取得して交叉を実行
    child1, child2, eval1, eval2 = crossover_hint.crossover(
        answer_cross[2 * j, :],
        answer_cross[2 * j + 1, :],
        evaluation_cross[2 * j],
        evaluation_cross[2 * j + 1],
    )
    # 交叉結果を検証
    for k in range(81):
        if hint_pattern[k] == 1 and (child1[k] == 0 or child2[k] == 0):
            print(f"正しく交叉されていません: ペア {j}, インデックス {k}")
    return (2 * j, child1, child2, eval1, eval2)

# 並列実行する関数
def crossover_population_in_parallel(cn, answer_cross, evaluation_cross, hint_pattern):
    # 並列実行
    with ProcessPoolExecutor() as executor:
        # 各タスクに必要な引数をまとめて渡す
        args = [
            (j, answer_cross, evaluation_cross, hint_pattern) for j in range(cn // 2)
        ]
        results = list(executor.map(parallel_crossover, args))

    # 結果を反映
    for idx, child1, child2, eval1, eval2 in results:
        answer_cross[idx, :] = child1
        answer_cross[idx + 1, :] = child2
        evaluation_cross[idx] = eval1
        evaluation_cross[idx + 1] = eval2

    return answer_cross, evaluation_cross

# グローバル関数として定義
def parallel_mutation(args):
    j, answer_mutate, hint_pattern = args
    # 突然変異を実行
    mutated = create.mutate(answer_mutate[j, :])
    _evaluation = evaluate_suudoku.evaluate_sudoku_2d_strict(
        convert_1d_to_2d(mutated * hint_pattern)
    )

    # 突然変異結果を検証
    for k in range(81):
        if hint_pattern[k] == 1 and mutated[k] == 0:
            print(f"正しく突然変異されていません: 個体 {j}, インデックス {k}")
    return j, mutated, _evaluation

# 並列実行する関数
def mutate_population_in_parallel(population, cn, answer_mutate, evaluation_mutate, hint_pattern):
    # 並列実行
    with ProcessPoolExecutor() as executor:
        # 各タスクに必要な引数をまとめて渡す
        args = [
            (j, answer_mutate, hint_pattern) for j in range(population - cn)
        ]
        results = list(executor.map(parallel_mutation, args))

    # 結果を反映
    for idx, mutated, _evaluation in results:
        answer_mutate[idx, :] = mutated
        evaluation_mutate[idx] = _evaluation

    return answer_mutate, evaluation_mutate

#各個体は81要素のリストで表現される
#1世代の個体数は20

if __name__ == "__main__":
    #初期解生成
    answer = np.zeros((population,81), dtype=int)

    #初期解生成（20個作成）
    # for i in range(population):
    #     answer[i,:] = create.create_answer()
    #     answer[i,:], _ = create.repair(answer[i,:],HINT_PATTERN)
    answer = create.parallel_execution(population,np.array(HINT_PATTERN))

    # print("初期解")
    # for i in range(population):
    #     print(np.unique(answer[i,:]*HINT_PATTERN))

    #初期解の評価
    evaluation = np.zeros(population, dtype=float)
    # for i in range(population):
    #     evaluation[i] = evaluate_suudoku.evaluate_sudoku_2d_strict(convert_1d_to_2d(answer[i,:]*HINT_PATTERN))
    evaluation = eval_pop_in_parallel(answer,HINT_PATTERN)



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
        # #最良個体は保存
        # best_parent = answer[0,:]
        # best_parent_eval = evaluation[0]
        #親をランダムに並び替え
        index = np.random.permutation(population)
        answer = answer[index,:]
        evaluation = evaluation[index]

        #交叉させる個体
        answer_cross = answer[0:cn,:].copy()
        evaluation_cross = evaluation[0:cn].copy()
        answer_mutate = answer[cn:,:].copy()
        evaluation_mutate = evaluation[cn:].copy()
        # print("cossover:",i)
        #交叉
        # for j in range(0, cn//2):
        #     answer_cross[2*j,:], answer_cross[2*j + 1,:], evaluation_cross[2*j], evaluation_cross[2*j+1] = crossover_hint.crossover(answer_cross[2*j,:], answer_cross[2*j+1,:], evaluation_cross[2*j], evaluation_cross[2*j+1])
        #     for k in range(81):
        #         if HINT_PATTERN[k] == 1 and answer_cross[j,k] == 0:
        #             print("正しく交叉されていません")
        print("crossover")
        answer_cross, evaluation_cross = crossover_population_in_parallel(cn, answer_cross, evaluation_cross, HINT_PATTERN)

        check_problem(answer_cross, "交叉")

        # print("mutate:",i)
        #突然変異
        # for j in range(population - cn):
        #     answer_mutate[j,:] = create.mutate(answer_mutate[j,:])
        #     # print("finish mutate")
        #     # print("answer_mutate[:,j]:",answer_mutate[j,:])
        #     evaluation_mutate[j] = evaluate_suudoku.evaluate_sudoku_2d_strict(convert_1d_to_2d(answer_mutate[j,:]*HINT_PATTERN))
        #     # print("finish evaluate_mutate")
        #     for k in range(81):
        #         if HINT_PATTERN[k] == 1 and answer_mutate[j,k] == 0:
        #             print("正しく突然変異されていません")
        print("mutate")
        answer_mutate, evaluation_mutate = mutate_population_in_parallel(population, cn, answer_mutate, evaluation_mutate,HINT_PATTERN)
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