"""
双方向A* 探索アルゴリズムによる解法
"""

from heapq import heappush, heappop
from random import shuffle
import numpy as np
import random
import time

# グローバル変数
OPEN = 0
CLOSE = 1
toGOAL = 0
toINIT = 1

# 盤面
class Board():

    # コンストラクタ
    def __init__(self, board_list, distance, parent, dir, node = OPEN):
        self._array = board_list                        # 盤面
        self.distance = distance                        # 現在の探索盤面までの手数
        self.parent = parent                            # 親の盤面
        self.hashvalue = hash(tuple(self._array))       # ハッシュ値
        self.move = ''                                  # 移動方向
        self.heuristic = calc_heuristic(board_list, goal_board) if dir == toGOAL else calc_heuristic(board_list, start_board) # ヒューリスティック関数
        self.cost = self.distance + self.heuristic      # コスト（評価関数）
        self.dir = dir
        self.node = node

    # Board情報を取得
    def _getsBoard(self):
        return self._array

    # move情報を取得
    def _getsMove(self):
        return self.move

    # hash情報を取得
    def __hash__(self):
        return self.hashvalue

    # Board情報が等しいか比較
    def __eq__(self, other):
        return self._array == other._array

    # Board情報の大きさ比較
    def __lt__(self, other):
        return self._array < other._array


# 探索アルゴリズム
def search():
    No = 0        # 実行回数
    queue = []    # 待ち行列
    visited = {}  # 過去の盤面

    start = Board(start_board, 0, None, toGOAL) # 初期盤面
    goal = Board(goal_board, 0, None, toINIT)   # ゴール盤面

    # 訪問リストに登録
    visited[start.hashvalue] = start
    visited[goal.hashvalue] = goal

    # キューに追加
    heappush(queue, (start.cost, start))
    heappush(queue, (goal.cost, goal))

    # ゴールに到達するまで新しい盤面を探索
    while queue:

        now_tuple = heappop(queue) # 現在のタプル
        now_board = now_tuple[1]   # 現在の盤面

        if now_board.node == CLOSE: continue #nodeがCLOSEの時はスキップ

        No += 1 # 実行回数

        # ピースのない位置へ入ることのできる隣接座標
        now_index = now_board._array.index(position) # 盤面配列の先頭の値
        x, y = XY_coord(now_index)            # 盤面配列の先頭の値をXY座標に変換
        coord_next_array = coord_next(x, y)   # 空の位置へ移動できる隣接マスの配列

        # ピースのない位置へスライドを試行
        for coord in coord_next_array:
            next_board = now_board._array[:] # next_boardに今の盤面配列を代入
            next_index = coord[0] + width * coord[1] # XY座標から配列に変換
            next_board[now_index], next_board[next_index] = next_board[next_index], next_board[now_index] # 現在と次ののピース位置を入れ替え
            key = hash(tuple(next_board))

            # 訪問済みか確認
            if key in visited:
                
                visited_board = visited[key]
                
                if now_board.dir != visited_board.dir: # 両者の探索方向を確認
                    
                    # ゴールを発見
                    if now_board.dir == toGOAL:
                        # print('OOOOOOOOOO')
                        sol1 = get_solution(now_board)
                        sol2 = get_solution(visited_board)
                        sol2 = reverse_direction(sol2)
                        sol1.reverse()
                        # print('xxx', sol1)
                        # add_last_direction(sol1[-1], sol2[0], sol1)
                        # print('xxx',sol1)
                    else:
                        # print('KKKKKKKKK')
                        sol1 = get_solution(visited_board)
                        sol1.reverse()
                        sol2 = get_solution(now_board)
                        sol2 = reverse_direction(sol2)

                    sol = sol1 + sol2

                    # print('counts: ', No)

                    get_first_direction(sol[0], sol[1]) # 盤面最後の移動方向を追加
                    get_last_direction(sol[-2], sol[-1]) # 盤面最後の移動方向を追加

                    # a = 0
                    # for i in range(len(sol) - 1):
                    #     if (sol[i]['d'] == 'D'):
                            
                    #         if (sol[i - 1]['d'] != 'D'):
                    #             if (sol[i + 1]['d'] == 'D'):
                    #                 a = 1
                    #                 # print('sol', sol[i])
                    #                 sol.insert(i, {'array': [], 'd': 'D'})
                    # if a == 1: sol.pop(-1)

                    return sol

                # 訪問済みで現在のコストのほうが小さい時
                if visited_board.cost > now_board.cost + 1:
                    visited_board.node = CLOSE #nodeをCLOSEにする
                else:
                    continue

            # 未訪問 or 訪問済みで現在のコストのほうが小さい時
            new_board = Board(next_board, now_board.distance+1, now_board, now_board.dir) # 次の盤面
            new_board.move = coord[2]
            # if (new_board.move == 'D'):  print('AAA', new_board._array)
            visited[key] = new_board # 訪問済みリストに登録
            heappush(queue, (new_board.cost, new_board)) # 待ち行列に登録
    
        now_board.node = CLOSE #nodeをCLOSEにする


# 解答を取得
def get_solution(board):
    solution = []                   # solutionを作成

    while board is not None:
        # solution += [{'array':[board._getsBoard()], 'd': str(board._getsMove()) } ]  # solution配列に追加
        solution.append({
            'array': board._getsBoard(),
            'd': str(board._getsMove())
        })
        board = board.parent        # boardに親盤面を代入

    return solution


# ヒューリスティック関数
def calc_heuristic(list, list2):
    now_board = list  # 現在盤面
    std_board = list2 # 比較盤面
    same = 0          # 一致しないピースの数
    manhattan = 0     # マンハッタン距離

    for i in now_board:

        # 一致しないピースの数を計算
        x, y = XY_coord(i)

        if std_board.index(i) != now_board.index(i):
            same += 1

        # 盤面へ移動するときのマンハッタン距離
        pos = std_board.index(i)
        std_board_x, std_board_y = XY_coord(pos)
        x, y = XY_coord(now_board.index(i))
        manhattan += abs(x - std_board_x) + abs(y - std_board_y)

    heuristic = manhattan * HEURISTIC_MAGNIFICATION

    return heuristic


# 空の位置へ移動できる隣接マスを計算
def coord_next(x, y):
    coord_next_array = [] # 隣接マスの配列

    # up
    if (y - 1 >= 0):
        coord_next_array.append([x, y - 1, 'U'])
    else:
        coord_next_array.append([x, height - 1, 'U']) # 飛び越え

    # down
    if (y + 1 < height):
        coord_next_array.append([x, y + 1, 'D'])
    else:
        coord_next_array.append([x, 0, 'D']) # 飛び越え

    # right
    if (x + 1 < width):
        coord_next_array.append([x + 1, y, 'R'])
    else:
        coord_next_array.append([0, y, 'R']) # 飛び越え

    # left
    if (x - 1 >= 0):
        coord_next_array.append([x - 1, y, 'L'])
    else:
        coord_next_array.append([width - 1, y, 'L']) # 飛び越え

    return coord_next_array


# 盤面配列からXY座標を取得
def XY_coord(index):
    x = index % width  # X座標
    y = index // width # Y座標

    return x, y         # XY座標を返す


# 盤面配列からindexを取得
def XY_index(x, y):
    max_index = width * height - 1
    index = x + width * y
    
    if max_index < index:
        print('error')
        return 0
    
    return index # indexを返す


# ゴール配列を取得
def get_goal_array():
    global width, height, rot

    rot = np.array([], int)
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
            rot = np.append(rot, int(data[2]))
    
    for i in in_array: out_array = np.append(out_array, XY_index(i[0], i[1]))

    return out_array.tolist()


# 初期配列を取得
def get_start_array():
    index = width * height
    out_array = np.array(range(index))
    
    return out_array.tolist()


# 盤面最初の移動方向を追加
def get_first_direction(now, next):

    # ゴール一つ前のの盤面
    now_array = np.array(now['array'])
    now_index = np.where(now_array == position)[0][0]
    x, y = XY_coord(now_index)

    # ゴール盤面
    next_array = np.array(next['array'])
    next_index = np.where(next_array == position)[0][0]
    next_x, next_y = XY_coord(next_index)

    # up
    if (y - 1 >= 0):
        if x == next_x and y - 1 == next_y: direction = 'U'
    else:
        if x == next_x and height - 1 == next_y: direction = 'U'

    # down
    if (y + 1 < height):
        if x == next_x and y + 1 == next_y: direction = 'D'
    else:
        if x == next_x and 0 == next_y: direction = 'D'

    # right
    if (x + 1 < width):
        if x + 1 == next_x and y == next_y: direction = 'R'
    else:
        if 0 == next_x and y == next_y: direction = 'R'

    # left
    if (x - 1 >= 0):
        if x - 1 == next_x and y == next_y: direction = 'L'
    else:
        if width - 1 == next_x and y == next_y: direction = 'L'

    now['d'] = direction


# 盤面最後の移動方向を追加
def get_last_direction(now, next):

    # ゴール一つ前のの盤面
    now_array = np.array(now['array'])
    now_index = np.where(now_array == position)[0][0]
    x, y = XY_coord(now_index)

    # ゴール盤面
    next_array = np.array(next['array'])
    next_index = np.where(next_array == position)[0][0]
    next_x, next_y = XY_coord(next_index)

    # up
    if (y - 1 >= 0):
        if x == next_x and y - 1 == next_y: direction = 'U'
    else:
        if x == next_x and height - 1 == next_y: direction = 'U'

    # down
    if (y + 1 < height):
        if x == next_x and y + 1 == next_y: direction = 'D'
    else:
        if x == next_x and 0 == next_y: direction = 'D'

    # right
    if (x + 1 < width):
        if x + 1 == next_x and y == next_y: direction = 'R'
    else:
        if 0 == next_x and y == next_y: direction = 'R'

    # left
    if (x - 1 >= 0):
        if x - 1 == next_x and y == next_y: direction = 'L'
    else:
        if width - 1 == next_x and y == next_y: direction = 'L'

    next['d'] = direction


# 盤面最後の移動方向を追加
def add_last_direction(now, next, out):

    # ゴール一つ前のの盤面
    now_array = np.array(now['array'])
    now_index = np.where(now_array == position)[0][0]
    x, y = XY_coord(now_index)

    # ゴール盤面
    next_array = np.array(next['array'])
    next_index = np.where(next_array == position)[0][0]
    next_x, next_y = XY_coord(next_index)

    # up
    if (y - 1 >= 0):
        if x == next_x and y - 1 == next_y: direction = 'U'
    else:
        if x == next_x and height - 1 == next_y: direction = 'U'

    # down
    if (y + 1 < height):
        if x == next_x and y + 1 == next_y: direction = 'D'
    else:
        if x == next_x and 0 == next_y: direction = 'D'

    # right
    if (x + 1 < width):
        if x + 1 == next_x and y == next_y: direction = 'R'
    else:
        if 0 == next_x and y == next_y: direction = 'R'

    # left
    if (x - 1 >= 0):
        if x - 1 == next_x and y == next_y: direction = 'L'
    else:
        if width - 1 == next_x and y == next_y: direction = 'L'
    
    # out.append({'array': [], 'd': direction})
    # print('aaa',{'array': [], 'd': direction})


# 解答の探索方向を逆転
def reverse_direction(array):
    dict = {
        'U': 'D',
        'D': 'U',
        'R': 'L',
        'L': 'R'
    }

    for i in range(len(array)):
        if array[i]['d']: array[i]['d'] = dict[array[i]['d']]

    return array


# 移動
def move(now_array, goal_number, confirm_array):
    global start_board, goal_board, position

    pp = False
    if goal_number == 7: pp = True

    start_array = np.array(now_array)
    goal_array = np.array(goal_board)
    r_start_array = np.array(now_array)
    r_goal_array = np.array(goal_board)
    free_number = width * height + 1 # 自由に動かせるマスの番号

    confirm_array_index = np.array([], int)
    for i in confirm_array:
        index = np.where(start_array == i)[0][0] # 指定したマスのindex
        confirm_array_index = np.append(confirm_array_index, index)

    # 現在の盤面
    index = np.where(start_array == goal_number)[0][0] # 指定したマスのindex
    start_array = np.full(width * height, free_number) # マスをfree_numberで埋める
    start_array[index] = goal_number # 指定したマスを元の値に戻す

    confirm_array_index2 = np.array([], int)
    for i in range(len(confirm_array)):
        index2 = confirm_array_index[i]
        start_array[index2] = confirm_array[i]

        index = np.where(goal_array == confirm_array[i])[0][0] # 指定したマスのindex
        confirm_array_index2 = np.append(confirm_array_index2, index)

    # ゴール盤面
    index = np.where(goal_array == goal_number)[0][0] # 指定したマスのindex
    goal_array = np.full(width * height, free_number) # マスをfree_numberで埋める
    goal_array[index] = goal_number  # 指定したマスを元の値に戻す
    position = goal_number

    for i in range(len(confirm_array)):
        index3 = confirm_array_index[i]
        goal_array[index3] = confirm_array[i]

    # グローバル変数に代入
    start_board = start_array.tolist()
    goal_board = goal_array.tolist()

    # print(start_board, goal_board)

    # 探索
    solution = search()

    start_board = r_start_array.tolist()
    goal_board = r_goal_array.tolist()
    
    # print(solution)
    if pp:
        array2 = []
        for i in range(len(solution) - 1):
            array2.append(solution[i + 1]['array'])

    pp = False
    array = []
    for i in range(len(solution) - 1):
        array.append(solution[i + 1]['d'])

    return array


# 盤面移動
def move_board(board_array, position, root):
    now_array = np.array(board_array)
    position = np.where(now_array == position)[0][0]
    # print('start: ', now_array)

    for direction in root:
        # print(direction)
        x, y = XY_coord(position) # XY座標に変換

        # up
        if direction == 'U':
            index = XY_index(x, y - 1) if y - 1 >= 0 else XY_index(x, height - 1)

        # down
        if direction == 'D':
            index = XY_index(x, y + 1) if y + 1 < height else XY_index(x, 0)

        # right
        if direction == 'R':
            index = XY_index(x + 1, y) if x + 1 < width else XY_index(0, y)

        # left
        if direction == 'L':
            index = XY_index(x - 1, y) if x - 1 >= 0 else XY_index(width - 1, y)

        now_array[position], now_array[index] = now_array[index], now_array[position] # マスを交換
        # print('',now_array)
        position = index # 新しい位置を指定
        # print(now_array, direction)

    # print('goal: ', now_array)
    return now_array


# メイン関数
def main():
    global start_board, goal_board, position
    global HEURISTIC_MAGNIFICATION
    global all_result

    # HEURISTIC_MAGNIFICATION = 0.79
    HEURISTIC_MAGNIFICATION = 10000

    goal_board = get_goal_array()
    start_board = get_start_array()

    # global width, height, position
    global position

    position = 0
    # width = 3
    # height = 3

    # goal_board = [8, 6, 7, 2, 5, 4, 3, 0, 1]
    # start_board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    print('can_solve: ', can_solve())
    
    for i in range(width * height):
        if (can_solve()):
            solution = search()
            output_answer(solution)
            break
        else:
            position += 1
            continue


    # width = 4
    # height = 4

    # goal_board =  [3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12] # ボードの初期盤面 最短53手
    # goal_board =  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 13, 14, 15] # ボードの初期盤面 right x3
    # goal_board =  [1, 2, 3, 0, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12] # ボードの初期盤面 down x3
    # start_board =  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 0, 13] # ボードの初期盤面 left x3 (13選択時)
    # start_board =  [1, 2, 3, 8, 5, 6, 7, 12, 9, 10, 11, 0, 13, 14, 15, 4] # ボードの初期盤面 up x3 (4選択時)
    # start_board = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0] # ボードのゴール盤面

    # root = move(start_board, 0, []) # 特定のピースをゴールの位置へ移動 (現在の盤面, 移動したい値)
    # board = move_board(start_board, position, root)
    # print('board: ',root, board)

    # root = move(board, 1, [0]) # 特定のピースをゴールの位置へ移動 (現在の盤面, 移動したい値)
    # board = move_board(board, position, root)
    # print('board: ',root, board)

    # root = move(board, 2, [0,1]) # 特定のピースをゴールの位置へ移動 (現在の盤面, 移動したい値)
    # board = move_board(board, position, root)
    # print('board: ',root, board)

    # root = move(board, 3, [0,1,2]) # 特定のピースをゴールの位置へ移動 (現在の盤面, 移動したい値)
    # board = move_board(board, position, root)
    # print('board: ',root, board)

    # root = move(board, 4, [0,1,2,3]) # 特定のピースをゴールの位置へ移動 (現在の盤面, 移動したい値)
    # board = move_board(board, position, root)
    # print('board: ',root, board)

    # root = move(board, 5, [0,1,2,3,4]) # 特定のピースをゴールの位置へ移動 (現在の盤面, 移動したい値)
    # board = move_board(board, position, root)
    # print('board: ',root, board)

    # root = move(board, 6, [0,1,2,3,4,5]) # 特定のピースをゴールの位置へ移動 (現在の盤面, 移動したい値)
    # board = move_board(board, position, root)
    # print('board: ',root, board)

    # root = move(board, 7, [0,1,2,3,4,5,6]) # 特定のピースをゴールの位置へ移動 (現在の盤面, 移動したい値)
    # board = move_board(board, position, root)
    # print('board: ',root, board)

    # root = move(board, 8, [0,1,2,3,4,5,6,7]) # 特定のピースをゴールの位置へ移動 (現在の盤面, 移動したい値)
    # print(root)
    # board = move_board(board, position, root)
    # print('board',root, board)

    # ok_array = []
    # for i in start_board:
    #     print('a ', i)
    #     ok_array.append(i)
    #     print(ok_array)

    # print(start_board)

    # timer_start = time.time()
    # solution = search()
    # timer_end = time.time()

    # print('time  : ', timer_end - timer_start)
    
    # print('length: ', len(solution))
    # print(solution)

    # array = []
    # for i in range(len(solution)):
    #     array.append(solution[i]['d'])
    #     print(solution[i])
    # print(array)

    # output_answer(solution)


# ゴール配列を取得
def output_answer(solution):
    answer = ''

    for i in rot: answer += str(i)

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


# 配列を作成
def create_array(array):
    out_array = np.array(array) # 出力配列
    index = np.where(out_array == position)[0][0] # 0の位置
    out_array = np.delete(out_array, index) # 指定したindexを削除
    # print('pos', position)

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

    # print('can_solve: ', counts) # ログ出力
    return counts % 2 == 0


# 実行
if __name__ == '__main__':
    main()
