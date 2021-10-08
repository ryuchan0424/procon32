import numpy as np
import random

# ゴール配列を取得
def output_answer(solution):
    answer = ''

    # ランダムな数を生成（回転）
    for i in start_board: answer += str(random.randrange(3)) # 回転情報

    XY = XY_coord(start_board.index(position)) # 選択位置のXY座標

    hex_X = str(hex(XY[0])).replace('0x','').upper()  # 10進数 -> 16進数
    hex_Y = str(hex(XY[1])).replace('0x','').upper()  # 10進数 -> 16進数

    answer += '\n1\n'                   # 選択回数
    answer += hex_X + hex_Y + '\n'      # 選択画像位置
    answer += str(len(solution)) + '\n' # 交換回数

    for item in solution: answer += item['d']

    print(answer)                    # answerを出力
    file = open('solution.txt', 'w') # solution.txtを開く
    file.write(answer)               # ファイルに書き込み
    file.close()                     # ファイルを閉じる


# 盤面配列からXY座標を取得
def XY_coord(index):
    x = index % width  # X座標
    y = index // width # Y座標

    return x, y         # XY座標を返す


# 実行
if __name__  ==  '__main__':
    global width, start_board, goal_board, position

    width = 4
    position = 0

    start_board = [3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12]
    solution = [{'array': [3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12], 'd': ''}, {'array': [3, 2, 1, 4, 7, 6, 5, 0, 11, 10, 9, 8, 15, 14, 13, 12], 'd': 'D'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 11, 10, 9, 0, 15, 14, 13, 12], 'd': 'D'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 11, 10, 0, 9, 15, 14, 13, 12], 'd': 'L'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 11, 0, 10, 9, 15, 14, 13, 12], 'd': 'L'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 11, 14, 10, 9, 15, 0, 13, 12], 'd': 'D'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 11, 14, 10, 9, 0, 15, 13, 12], 'd': 'L'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 0, 14, 10, 9, 11, 15, 13, 12], 'd': 'U'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 9, 14, 10, 0, 11, 15, 13, 12], 'd': 'L'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 9, 14, 10, 12, 11, 15, 13, 0], 'd': 'D'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 9, 14, 10, 12, 11, 15, 0, 13], 'd': 'L'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 9, 14, 10, 12, 11, 0, 15, 13], 'd': 'L'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 9, 14, 10, 12, 0, 11, 15, 13], 'd': 'L'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 9, 14, 10, 12, 13, 11, 15, 0], 'd': 'L'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 9, 14, 10, 12, 13, 11, 0, 15], 'd': 'L'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 9, 14, 10, 12, 13, 0, 11, 15], 'd': 'L'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 9, 0, 10, 12, 13, 14, 11, 15], 'd': 'U'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 9, 10, 0, 12, 13, 14, 11, 15], 'd': 'R'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 9, 10, 11, 12, 13, 14, 0, 15], 'd': 'D'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 9, 10, 11, 12, 13, 14, 15, 0], 'd': 'R'}, {'array': [3, 2, 1, 4, 7, 6, 5, 8, 9, 10, 11, 0, 13, 14, 15, 12], 'd': 'U'}, {'array': [3, 2, 1, 4, 7, 6, 5, 0, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'U'}, {'array': [3, 2, 1, 0, 7, 6, 5, 4, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'L'}, {'array': [3, 2, 0, 1, 7, 6, 5, 4, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'L'}, {'array': [3, 0, 2, 1, 7, 6, 5, 4, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'L'}, {'array': [0, 3, 2, 1, 7, 6, 5, 4, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'L'}, {'array': [1, 3, 2, 0, 7, 6, 5, 4, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'L'}, {'array': [1, 3, 0, 2, 7, 6, 5, 4, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'L'}, {'array': [1, 0, 3, 2, 7, 6, 5, 4, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'D'}, {'array': [1, 6, 3, 2, 7, 0, 5, 4, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'R'}, {'array': [1, 6, 3, 2, 7, 5, 0, 4, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'U'}, {'array': [1, 6, 0, 2, 7, 5, 3, 4, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'R'}, {'array': [1, 6, 2, 0, 7, 5, 3, 4, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'D'}, {'array': [1, 6, 2, 4, 7, 5, 3, 0, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'R'}, {'array': [1, 6, 2, 4, 0, 5, 3, 7, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'R'}, {'array': [1, 6, 2, 4, 5, 0, 3, 7, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'U'}, {'array': [1, 0, 2, 4, 5, 6, 3, 7, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'R'}, {'array': [1, 2, 0, 4, 5, 6, 3, 7, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'D'}, {'array': [1, 2, 3, 4, 5, 6, 0, 7, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'R'}, {'array': [1, 2, 3, 4, 5, 6, 7, 0, 9, 10, 11, 8, 13, 14, 15, 12], 'd': 'D'}, {'array': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 13, 14, 15, 12], 'd': 'D'}, {'array': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0], 'd': ''}]
    
    output_answer(solution)

