import create_suudoku as create
import evaluate_suudoku
import crossover_hint
import numpy as np
import random

HINT_PATTERN = [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
population = 20 #個体数
max_generation = 100 #最大世代数
cr = 0.7 #交叉率
cn = round(population * cr) #交叉数
mr = 0.3 #突然変異率

#81要素のリストを9×9行列に変換
def convert_1d_to_2d(board):
    return np.array(board).reshape(9, 9)

#各個体は81要素のリストで表現される
#1世代の個体数は20
#初期解生成
answer = np.zeros((population,81), dtype=int)

#初期解生成（20個作成）
for i in range(population):
    answer[i,:] = create.create_answer()

#初期解の評価
evaluation = np.zeros(population, dtype=int)
for i in range(population):
    evaluation[i] = evaluate_suudoku.evaluate_sudoku_2d_strict(convert_1d_to_2d(answer[i,:]*HINT_PATTERN))

#評価値の高い順にソート
index = np.argsort(-evaluation)
answer = answer[index,:]
evaluation = evaluation[index]

#新たな解を作成し、その評価値が親より高い場合には置き換える
#親の評価値が最も高いものを選ぶ
for i in range(max_generation):
    print("generation[",i,"]")
    #最良個体は保存
    best_parent = answer[0,:]
    best_parent_eval = evaluation[0]
    #親をランダムに並び替え
    index = np.random.permutation(population)
    answer = answer[index,:]
    evaluation = evaluation[index]

    #交叉させる個体
    answer_cross = answer[0:cn,:]
    evaluation_cross = evaluation[0:cn]
    answer_mutate = answer[cn:,:]
    evaluation_mutate = evaluation[cn:]
    # print("cossover:",i)
    #交叉
    for j in range(0, cn, 2):
        answer_cross[j,:], answer_cross[j+1,:], evaluation_cross[j], evaluation_cross[j+1] = crossover_hint.crossover(answer_cross[j,:], answer_cross[j+1,:], evaluation_cross[j], evaluation_cross[j+1])
        for k in range(81):
            if HINT_PATTERN[k] == 1 and answer_cross[j,k] == 0:
                print("正しく交叉されていません")
    
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

    
    #交叉と突然変異で生成した個体を結合
    answer = np.vstack((answer_cross, answer_mutate))
    evaluation = np.hstack((evaluation_cross, evaluation_mutate))

    # #すべての個体を表示
    # print("generation[",i,"]が終わった")
    # for j in range(population):
    #     print(answer[j,:])

    #評価値の高い順にソート
    index = np.argsort(-evaluation)
    answer = answer[index,:]
    evaluation = evaluation[index]

    #最良個体を保存
    answer[population-1,:] = best_parent
    evaluation[population-1] = best_parent_eval

    #評価値の高い順にソート
    index = np.argsort(-evaluation)
    answer = answer[index,:]
    evaluation = evaluation[index]


    
    print("best_parent_eval[",i,"]=",evaluation[0])


#最も評価値が高い解を出力
print(answer[0,:].reshape(9, 9))
print(evaluation[0])