import copy


# ゴール可能かどうか判定
def can_solve():
    start_arr = copy.copy(start_board) # 配列をコピー
    index = start_arr.index(0) # 選択マス位置
    row = XY_coord(index)[1] + 1 # y行目
    counts = row # 初期値
    start_arr.remove(start_arr[index]) # 選択マス位置の値を削除

    # 交換回数をカウント
    for i in range(len(start_arr)):
        for j in range(len(start_arr) - 1, i, -1):
            if start_arr[i] > start_arr[j]:
                counts += 1
    
    return counts % 2 == 0


# 盤面配列からXY座標を取得
def XY_coord(index):
    x = index % width  # X座標
    y = index // width # Y座標

    return x, y        # XY座標を返す


# 実行
if __name__ == '__main__':
    global width, height, start_board

    width = 6
    height = 2
    start_board = [ 4, 3, 2, 1, 5, 6, 7, 8, 12, 11, 10, 9, 13, 15, 14, 0]
    
    print(can_solve()) # ゴール可能かどうか判定
