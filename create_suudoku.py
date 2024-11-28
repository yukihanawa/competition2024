import numpy as np
import random
import math


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

#1~3行目or4~6行目or7~9行目の中で行を入れ替える(ランダム)
def change_row(answer):
    a = random.randint(1, 3)
    b = random.randint(1, 3)
    if a == b:
        change_row(answer)
    else:
        answer[(a-1)*3,:], answer[(b-1)*3,:] = answer[(b-1)*3,:].copy(), answer[(a-1)*3,:].copy()
    return answer

#1~3列目or4~6列目or7~9列目の中で列を入れ替える(ランダム)
def change_column(answer):
    a = random.randint(1, 3)
    b = random.randint(1, 3)
    if a == b:
        change_column(answer)
    else:
        answer[:,(a-1)*3:(a*3)], answer[:,(b-1)*3:(b*3)] = answer[:,(b-1)*3:(b*3)].copy(), answer[:,(a-1)*3:(a*3)].copy()
    return answer


# answer = create_first_answer(answer)
# answer = change_row_block(answer)
# answer = change_column_block(answer)
# answer = change_row(answer)
# answer = change_column(answer)
# print(answer)

def create_answer():
    answer = create_first_answer()
    if random.random() < 0.5:
        answer = change_row_block(answer)
    if random.random() < 0.5:
        answer = change_column_block(answer)
    if random.random() < 0.5:
        answer = change_row(answer)
    if random.random() < 0.5:
        answer = change_column(answer)
    return answer.flatten()