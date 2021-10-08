import numpy as np


# 配列を作成
def create_array(array):
    out_array = np.array(array) # 出力配列
    index = np.where(out_array == 0)[0][0] # 0の位置
    out_array = np.delete(out_array, index) # 指定したindexを削除

    return out_array

# 交換回数をカウント
def counter(start, goal):
    counts = 0
    start_array = np.array(start)
    goal_array = np.array(goal)

    for i in range(len(start_array)):
        if start_array[i] != goal_array[i]:
            index = np.where(start_array == goal_array[i])[0][0] # 位置
            start_array[i], start_array[index] = start_array[index], start_array[i] # 交換
            counts += 1 # カウントを1増やす

    return counts

# ゴール可能かどうか判定
def can_solve():
    start = create_array(start_board)
    goal = create_array(goal_board)
    counts = counter(start, goal)

    print(counts) # ログ出力
    return counts % 2 == 0


# 実行
if __name__ == '__main__':
    global width, height, start_board, goal_board

    width = 3
    height = 3
    start_board = [1,3,2,0,7,6,5,8,4]
    goal_board = [1,2,3,4,5,6,7,8,0]

    print(can_solve())
