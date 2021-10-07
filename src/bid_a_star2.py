"""
双方向A* 探索アルゴリズムによる解法
"""

from heapq import heappush, heappop
from random import shuffle
import numpy as np
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
        now_index = now_board._array.index(0) # 盤面配列の先頭の値
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
                        sol1 = get_solution(now_board)
                        sol2 = get_solution(visited_board)
                        sol1.reverse()
                    else:
                        sol1 = get_solution(visited_board)
                        sol1.reverse()
                        sol2 = get_solution(now_board)

                    sol = sol1 + sol2

                    print('counts: ', No)
                    return sol

                # 訪問済みで現在のコストのほうが小さい時
                if visited_board.cost > now_board.cost + 1:
                    visited_board.node = CLOSE #nodeをCLOSEにする
                else:
                    continue

            # 未訪問 or 訪問済みで現在のコストのほうが小さい時
            new_board = Board(next_board, now_board.distance+1, now_board, now_board.dir) # 次の盤面
            visited[key] = new_board # 訪問済みリストに登録
            heappush(queue, (new_board.cost, new_board)) # 待ち行列に登録
    
        now_board.node = CLOSE #nodeをCLOSEにする


# 解答を取得
def get_solution(board):
    solution = []                   # solutionを作成

    while board is not None:
        solution += [board._array]  # solution配列に追加
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

    return out_array.tolist()


# 初期配列を取得
def get_start_array():
    index = width * height
    out_array = np.array(range(index))
    
    return out_array.tolist()

# メイン関数
def main():
    global start_board, goal_board
    global HEURISTIC_MAGNIFICATION

    HEURISTIC_MAGNIFICATION = 0.79

    goal_board = get_goal_array()
    start_board = get_start_array()

    timer_start = time.time()
    solution = search()
    timer_end = time.time()

    print('time  : ', timer_end - timer_start)
    print('length: ', len(solution), '\n', solution)


# 実行
if __name__ == '__main__':
    main()
