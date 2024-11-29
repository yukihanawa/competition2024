import create_suudoku as create
import evaluate_suudoku
import crossover_hint
import numpy as np

HINT_PATTERN = [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]

#数独の解を交叉させる



#81要素のリストを9×9行列に変換
def convert_1d_to_2d(board):
    return np.array(board).reshape(9, 9)

#各個体は81要素のリストで表現される
#1世代の個体数は20
#初期解生成
answer = np.zeros((81, 20), dtype=int)

#初期解生成（20個作成）
for i in range(20):
    answer[:,i] = create.create_answer()

#初期解の評価
evaluation = np.zeros(20, dtype=int)
for i in range(20):
    evaluation[i] = evaluate_suudoku.evaluate_sudoku_2d_strict(convert_1d_to_2d(answer[:,i]*HINT_PATTERN))

#評価値の高い順にソート
index = np.argsort(-evaluation)
answer = answer[:,index]
evaluation = evaluation[index]

#新たな解を作成し、その評価値が親より高い場合には置き換える
#親の評価値が最も高いものを選ぶ
for i in range(20):
    print("evaluation[",i,"]=",evaluation[i])
    new_answer = create.create_answer()
    new_evaluation= evaluate_suudoku.evaluate_sudoku_2d_strict(convert_1d_to_2d(new_answer*HINT_PATTERN))
    if new_evaluation > evaluation[19]:
        answer[:,19] = new_answer
        evaluation[19] = new_evaluation
        #評価値の高い順にソート
        index = np.argsort(-evaluation)
        answer = answer[:,index]
        evaluation = evaluation[index]

#最も評価値が高い解を出力
print(answer[:,0])
print(evaluation[0])