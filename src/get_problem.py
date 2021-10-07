import numpy as np


# ゴール配列を取得
def get_goal_array():
    global width, height

    in_array = np.empty((0, 2), int) # 入力配列
    out_array = np.array([], int) # 出力配列
    filet = open('problem.txt', 'r',encoding = 'utf-8').read()

    y_wari = filet.split("\n")
    x_wari = y_wari[0].split("\t")
    data = x_wari[0].split(",")
    y_wari = filet.split("\n")

    width = len(x_wari)
    height = len(y_wari)
    
    for i2 in range(len(y_wari)):

        x_wari = y_wari[i2].split("\t")

        for i1 in range(len(x_wari)):

            data = x_wari[i1].split(",")
            in_array = np.append(in_array, [[int(data[0]), int(data[1])]], axis = 0)
    
    for i in in_array: out_array = np.append(out_array, XY_index(i[0], i[1]))

    return out_array


# 盤面配列からindexを取得
def XY_index(x, y):
    max_index = width * height - 1
    index = x + width * y
    
    if max_index < index:
        print('error')
        return 0
    
    return index         # indexを返す


# 初期配列を取得
def get_start_array():
    index = width * height
    out_array = np.array(range(index))
    
    return out_array


# 実行
if __name__  ==  '__main__':
    global start_board, goal_board

    goal_board = get_goal_array()
    start_board = get_start_array()

    print(start_board)
    print(goal_board)
