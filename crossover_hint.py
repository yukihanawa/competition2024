import numpy as np
import random
import evaluate_suudoku
import solve_suudoku_2d
import create_suudoku_ver1 as create

HINT_PATTERN = [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
# HINT_PATTERN = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def is_valid(board, row, col, num):
    """数独の盤面で指定した位置に数値を置くことが有効か確認します。"""
    if num in board[row, :] or num in board[:, col]:
        return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[start_row:start_row+3, start_col:start_col+3]:
        return False

    return True

def fill_child(child, parent1, parent2, i):
    """
    指定された子 (child) の必要な位置を親 (parent1, parent2) から埋める関数
    """
    if random.choice([True, False]):
        primary, secondary = parent1, parent2
    else:
        primary, secondary = parent2, parent1

    if primary[i] not in child:
        child[i] = primary[i]
        for j in range(i + 1, 81):
            if primary[j] == primary[i] and child[j] == 0:
                child[j] = primary[j]
    elif secondary[i] not in child:
        child[i] = secondary[i]
        for j in range(i + 1, 81):
            if secondary[j] == secondary[i] and child[j] == 0:
                child[j] = secondary[j]

#後ろに同じ数字がある場合、それを埋める
def fill_child_rest(child, parent, i):
    for j in range(i + 1, 81):
        if parent[j] == parent[i] and child[j] == 0 and HINT_PATTERN[j] == 1:
            child[j] = parent[j]


def crossover(parent1, parent2, parent1_eval, parent2_eval):
    """親1と親2から位置が被らない数値ペアを選び、子供を生成します。"""
    # 初期化
    child1 = np.zeros(81, dtype=int)
    child2 = np.zeros(81, dtype=int)
    parent1 = np.array(parent1) * HINT_PATTERN
    parent2 = np.array(parent2) * HINT_PATTERN

    # print("parent1:")
    # print(parent1.reshape(9, 9))
    # print()
    # print("parent2:")
    # print(parent2.reshape(9, 9))
    # print()

    hint_index = -1
    #最初の二つは任意の親から数字を入れたい
    for i in range(81):
        if HINT_PATTERN[i] ==1:
            #ヒントが入るべき場所
            if hint_index ==-1:
                #初めてヒントが入るべき場所に到達
                child1[i] = parent1[i]
                child2[i] = parent2[i]
                hint_index = i
                fill_child_rest(child1, parent1, i)
                fill_child_rest(child2, parent2, i)
            else:
                if child1[hint_index] != parent2[i]:
                    child1[i] = parent2[i]
                    fill_child_rest(child1, parent2, i)
                else:
                    child1[i] = parent1[i]
                    fill_child_rest(child1, parent1, i)
                if child2[hint_index] != parent1[i]:
                    child2[i] = parent1[i]
                    fill_child_rest(child2, parent1, i)
                else:
                    child2[i] = parent2[i]
                    fill_child_rest(child2, parent2, i)
                hint_index = i
                break


    for i in range(hint_index + 1,81,1):
        # child1の処理
        if HINT_PATTERN[i] == 1 and child1[i] == 0:
            fill_child(child1, parent1, parent2, i)
        # child2の処理
        if HINT_PATTERN[i] == 1 and child2[i] == 0:
            fill_child(child2, parent1, parent2, i)

    # print("child1:")
    # print(child1.reshape(9, 9))
    # print()
    # print("child2:")
    # print(child2.reshape(9, 9))
    
    #HINTが埋められなかった場所が発生する可能性があり、その場合にはナンプレを解いて埋める
    check_child1 = True
    check_child2 = True
    for i in range(81):
        if HINT_PATTERN[i] == 1 and child1[i] == 0:
            check_child1 = False
            # print("i:", i)
            # print()

    for i in range(81):
        if HINT_PATTERN[i] == 1 and child2[i] == 0:
            check_child2 = False
            # print("i:", i)
            # print()

    #交叉した個体の解が存在しない場合、ナンプレを解いて埋める（解が存在しない場合は親をそのまま使う）
    if check_child1 == False:
        # print("解の作成中...")
        child1 = solve_suudoku_2d.solve_sudoku_fast(np.array(child1).reshape(9, 9))
        if(child1 is not None):
            child1 = np.array(child1).reshape(81) * HINT_PATTERN
        else:
            child1 = create.mutate(parent1)
        # print("解の作成完了")

    if check_child2 == False:
        # print("解の作成中...")
        child2 = solve_suudoku_2d.solve_sudoku_fast(np.array(child2).reshape(9, 9))
        if(child2 is not None):
            child2 = np.array(child2).reshape(81) * HINT_PATTERN
        else:
            child2 = create.mutate(parent2)
        # print("解の作成完了")

    # print("child1:")
    # print(child1.reshape(9, 9))
    # print()
    # print("child2:")
    # print(child2.reshape(9, 9))
    child1_eval = evaluate_suudoku.evaluate_sudoku_2d_strict(np.array(child1).reshape(9, 9))
    child2_eval = evaluate_suudoku.evaluate_sudoku_2d_strict(np.array(child2).reshape(9, 9))

    # if child1_eval > parent1_eval:
    parent1 = child1
    parent1_eval = child1_eval
    
    # if child2_eval > parent2_eval:
    parent2 = child2
    parent2_eval = child2_eval
    
    return parent1, parent2, parent1_eval, parent2_eval


# サンプル親個体（完全に埋まった数独）
# parent1 = [
#     5, 3, 4, 6, 7, 8, 9, 1, 2,
#     6, 7, 2, 1, 9, 5, 3, 4, 8,
#     1, 9, 8, 3, 4, 2, 5, 6, 7,
#     8, 5, 9, 7, 6, 1, 4, 2, 3,
#     4, 2, 6, 8, 5, 3, 7, 9, 1,
#     7, 1, 3, 9, 2, 4, 8, 5, 6,
#     9, 6, 1, 5, 3, 7, 2, 8, 4,
#     2, 8, 7, 4, 1, 9, 6, 3, 5,
#     3, 4, 5, 2, 8, 6, 1, 7, 9
# ]

# parent2 = [
#     8, 2, 7, 1, 5, 4, 3, 9, 6,
#     9, 6, 5, 3, 2, 7, 1, 4, 8,
#     3, 4, 1, 6, 8, 9, 7, 5, 2,
#     5, 9, 3, 4, 6, 8, 2, 7, 1,
#     4, 7, 2, 5, 1, 3, 6, 8, 9,
#     6, 1, 8, 9, 7, 2, 4, 3, 5,
#     7, 8, 6, 2, 3, 5, 9, 1, 4,
#     1, 5, 4, 7, 9, 6, 8, 2, 3,
#     2, 3, 9, 8, 4, 1, 5, 6, 7
# ]


# parent1_eval = evaluate_suudoku.evaluate_sudoku_2d_strict(np.array(parent1).reshape(9, 9))
# parent2_eval = evaluate_suudoku.evaluate_sudoku_2d_strict(np.array(parent2).reshape(9, 9))

# #hintを9*9で表示
# for i in range(81):
#     if i % 9 == 0:
#         print()
#     print(HINT_PATTERN[i], end=" ")
# print()


# 交叉
# parent1, parent2, parent1_eval, parent2_eval = crossover(parent1, parent2, parent1_eval, parent2_eval)

# 結果を表示
#ヒントを9*9行列で表示
# for i in range(81):
#     if i % 9 == 0:
#         print()
#     print(HINT_PATTERN[i], end=" ")



# print("親1の評価値:", parent1_eval)
# print("親1の解:")
# print(np.array(parent1).reshape(9, 9))
# print()
# print("親2の評価値:", parent2_eval)
# print("親2の解:")
# print(np.array(parent2).reshape(9, 9))


#保存用
    # for i in range(81):
    #     # child1の必要な位置に数字がない
    #     if HINT_PATTERN[i] == 1 and child1[i] == 0:
    #         if random.choice([True, False]):
    #             #child1にparent1から数字を入れる
    #             if parent1[i] not in child1:
    #                 #parent1[i]がchild1に入っていない場合
    #                 child1[i] = parent1[i]
    #                 for j in range(i + 1, 81, 1):
    #                     if parent1[j] == parent1[i] and child1[j] == 0:
    #                         child1[j] = parent1[j]
    #             elif parent2[i] not in child1:
    #                 print("in child parent1[i]:", parent1[i])
    #                 #child1にparent2から数字を入れる
    #                 child1[i] = parent2[i]
    #                 for j in range(i + 1, 81, 1):
    #                     if parent2[j] == parent2[i] and child1[j] == 0:
    #                         child1[j] = parent2[j]
    #         else:
    #             #child1にparent2から数字を入れる
    #             if parent2[i] not in child1:
    #                 child1[i] = parent2[i]
    #                 for j in range(i + 1, 81, 1):
    #                     if parent2[j] == parent2[i] and child1[j] == 0:
    #                         child1[j] = parent2[j]
    #             elif parent1[i] not in child1:
    #                 child1[i] = parent1[i]
    #                 for j in range(i + 1, 81, 1):
    #                     if parent1[j] == parent1[i] and child1[j] == 0:
    #                         child1[j] = parent1[j]
    #     # child2の必要な位置に数字がない
    #     if HINT_PATTERN[i] == 1 and child2[i] == 0:
    #         if random.choice([True, False]):
    #             if parent1[i] not in child2:
    #                 child2[i] = parent1[i]
    #                 for j in range(i + 1, 81, 1):
    #                     if parent1[j] == parent1[i] and child2[j] == 0:
    #                         child2[j] = parent1[j]
    #             elif parent2[i] not in child2:
    #                 child2[i] = parent2[i]
    #                 for j in range(i + 1, 81, 1):
    #                     if parent2[j] == parent2[i] and child2[j] == 0:
    #                         child2[j] = parent2[j]
    #         else:
    #             if parent2[i] not in child2:
    #                 child2[i] = parent2[i]
    #                 for j in range(i + 1, 81, 1):
    #                     if parent2[j] == parent2[i] and child2[j] == 0:
    #                         child2[j] = parent2[j]
    #             elif parent1[i] not in child2:
    #                 child2[i] = parent1[i]
    #                 for j in range(i + 1, 81, 1):
    #                     if parent1[j] == parent1[i] and child2[j] == 0:
    #                         child2[j] = parent1[j]