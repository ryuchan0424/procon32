"""
A* 探索アルゴリズムによる解法
"""

from heapq import heappush, heappop
import time


# 盤面
class Board():

    # コンストラクタ
    def __init__(self, board_list, distance, parent):
        self._array = board_list                        # 盤面
        self.distance = distance                        # 現在の探索盤面までの手数
        self.heuristic = calc_heuristic(self._array)    # ヒューリスティック関数
        self.parent = parent                            # 親の盤面
        self.cost = self.distance + self.heuristic      # コスト（評価関数）
        self.hashvalue = hash(tuple(self._array))       # ハッシュ値
        self.move = ''                                  # 移動方向

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
    dist_dic = {} # 初期盤面からの手数

    start = Board(start_board, 0, None)     # 初期盤面
    goal = Board(goal_board, 9999999, None) # ゴール盤面

    heappush(queue, (start.cost, start))

    # ゴールに到達するまで新しい盤面を探索
    while queue:

        No += 1 # 実行回数
        now_tuple = heappop(queue) # 現在のタプル
        now_board = now_tuple[1]   # 現在の盤面
        
        # 現在の盤面がゴール盤面の時
        if now_board._array == goal_board:
            goal = now_board
            break

        # ピースのない位置へ入ることのできる隣接座標
        now_index = now_board._array.index(0)            # 盤面配列の先頭の値
        x, y = XY_coord(now_index)                       # 盤面配列の先頭の値をXY座標に変換
        coord_next_array = coord_next(x, y)              # 空の位置へ移動できる隣接マスの配列

        # ピースのない位置へスライドを試行
        for coord in coord_next_array:
            next_board = now_board._array[:] # next_boardに今の盤面配列を代入
            next_index = coord[0] + width * coord[1] # XY座標から配列に変換
            next_board[now_index], next_board[next_index] = next_board[next_index], next_board[now_index] # 現在と次ののピース位置を入れ替え

            # インスタンス化
            new_sboard = Board(next_board, now_board.distance + 1, now_board) # 次の盤面
            new_distance = new_sboard.cost                                    # コストをnew_distanceに代入

            # 未訪問 or 訪問済みで現在のコストのほうが小さい時
            if tuple(new_sboard._array) not in visited or new_distance < dist_dic[new_sboard]:
                dist_dic[new_sboard] = new_distance            # 初期盤面からのコストを登録
                visited[tuple(new_sboard._array)] = True       # 訪問済みリストに登録
                new_sboard.parent = now_board                  # 親盤面を登録
                new_sboard.move = coord[2]
                heappush(queue, (new_sboard.cost, new_sboard)) # 待ち行列に登録

    # 手順計算
    solution = []                       # solutionを作成
    while goal != start:
        solution += [str(goal._getsBoard()) + '\n']  # solution配列に追加
        goal = goal.parent              # varに親盤面を代入
    solution.reverse()                  # 配列を反転
    solution = ''.join(solution)        # 配列を文字列に変換


    # 手順計算
    # solution = []                       # solutionを作成

    # # varが初期盤面になるまでループ
    # while goal != start:
    #     solution += [goal._getsMove()]  # solution配列に追加
    #     goal = goal.parent              # varに親盤面を代入

    # solution.reverse()                  # 配列を反転
    # solution = ''.join(solution)        # 配列を文字列に変換

    print('counts: ', No)

    return solution


# 現在の探索盤面からゴール盤面までの手数の予測値（マンハッタン距離）を計算するヒューリスティック関数
def calc_heuristic(array):
    board_list = array # 現在の盤面
    same = 0           # ゴール盤面と一致しないピースの数
    manhattan = 0      # マンハッタン距離

    # board_listの数だけループ
    for var in board_list:

        # ゴール盤面と一致しないピースの数を計算
        x, y = XY_coord(var)
        if goal_board.index(var) != board_list.index(var): # ゴール盤面と一致しない時
            same += 1
            
        # ゴール盤面へ移動するときのマンハッタン距離
        pos = goal_board.index(var)                                # ゴール盤面のピースの位置
        goal_board_x, goal_board_y = XY_coord(pos)                 # ゴール盤面のピースの位置をXY座標に変換
        x, y = XY_coord(board_list.index(var))                     # 現在の盤面のピースの位置をXY座標に変換
        manhattan += abs(x - goal_board_x) + abs(y - goal_board_y) # XY座標の絶対値を足したものをマンハッタン距離とする

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


# メイン関数
def main():
    global width, height, start_board, goal_board
    global HEURISTIC_MAGNIFICATION

    HEURISTIC_MAGNIFICATION = 1.0  # heuristicに 1.9 をかけることで高速化

    # 3x3
    # width = 3
    # height = 3

    # start_board = [8, 6, 7, 2, 5, 4, 3, 0, 1]
    # goal_board = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    # 4x4
    width = 4
    height = 4

    start_board =  [3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12] # ボードの初期盤面 最短53手
    # start_board =  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 13, 14, 15] # ボードの初期盤面 right x3
    # start_board =  [1, 2, 3, 0, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12] # ボードの初期盤面 down x3
    # start_board =  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 0, 13] # ボードの初期盤面 left x3 (13選択時)
    # start_board =  [1, 2, 3, 8, 5, 6, 7, 12, 9, 10, 11, 0, 13, 14, 15, 4] # ボードの初期盤面 up x3 (4選択時)
    goal_board = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0] # ボードのゴール盤面

    # 5x5
    # width = 5
    # height = 5

    # start_board =  [1,3,2,4,5,6,7,8,13,10,11,12,9,14,15,16,17,18,19,20,21,22,23,24,0]
    # goal_board = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,0] # ボードのゴール盤面

    timer_start = time.time()
    solution = search()
    timer_end = time.time()

    print('time  : ', timer_end - timer_start)
    print(solution, len(solution))


# 実行
if __name__ == '__main__':
    main()
