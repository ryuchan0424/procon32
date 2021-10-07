"""
A* 探索アルゴリズムによる解法
"""

# モジュールをインポート
from heapq import heappush, heappop
from random import shuffle
import random
import copy
import time # デバッグ用

# グローバル変数
#LIMIT_SELECTION = 0
#SELECTON_RATE = 0
#EXCHANGE_RATE = 0
#ALL_COST = 0
MAX_DISTANCE = 9999999
HEURISTIC_MAGNIFICATION = 1.9  # heuristicに 1.9 をかけることで高速化

# sBoard Classを定義
class sBoard():

    # コンストラクタ
    def __init__(self, board_list, distance, parent):
        self._array = board_list                        # 盤面
        self.heuristic = calc_heuristic(self._array)    # 現在の探索盤面からゴール盤面までの手数の予測値（マンハッタン距離）
        self.distance = distance                        # 現在の探索盤面までの手数
        self.cost = self.distance + self.heuristic      # コスト（評価関数）
        self.parent = parent                            # 親の盤面
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

# A* 探索アルゴリズム
def astar():
    queue = []    # 待ち行列
    dist_dic = {} # 初期盤面からの手数
    visited = {}  # 過去の盤面

    # インスタンス化
    start = sBoard(init_board, 0, None) # 初期盤面
    end = sBoard(goal_board1, MAX_DISTANCE, None) # ゴール盤面

    # open-listのstart-node（コストとインスタンスを登録）
    heappush(queue, (start.cost, start))
    No = 0 # 実行回数

    # ゴールに到達するまで新しい盤面を探索
    while len(queue) > 0: # queueが空になるまでwhile
        # No += 1 # 実行回数

        # open-listからコスト最小の探索済みnode（盤面）を取得
        now_tuple = heappop(queue) # 現在のタプル
        now_board = now_tuple[1]   # 現在の盤面
        
        # 現在の盤面がゴール盤面の時
        if now_board._array == goal_board1 or now_board._array == goal_board2:
            end = now_board # 現在の盤面をゴール盤面として終了
            break

        # 現在の盤面がゴール盤面のではない時

        # ピースのない位置へ入ることのできる隣接座標
        index = now_board._array.index(elected_position) # 盤面配列の先頭の値
        x, y = XY_coord(index)                           # 盤面配列の先頭の値をXY座標に変換
        coord_next_OK = coord_next(x, y)                 # 空の位置へ移動できる隣接マスの配列

        # 次のnodeを探索；ピースのない位置へスライドを試行
        for coord in coord_next_OK:
            next_board = now_board._array[:] # next_boardに今の盤面配列を代入
            next_index = coord['XY'][0] * No_Y + coord['XY'][1] # XY座標から配列に変換
            next_board[index], next_board[next_index] = next_board[next_index], next_board[index] # 現在と次ののピース位置を入れ替え

            # インスタンス化
            new_sboard = sBoard(next_board, now_board.distance + 1, now_board) # 次の盤面
            new_distance = new_sboard.cost                                     # コストをnew_distanceに代入

            # 未訪問 or 訪問済みで現在のコストのほうが小さい時
            if tuple(new_sboard._array) not in visited or new_distance < dist_dic[new_sboard]:
                dist_dic[new_sboard] = new_distance            # 初期盤面からのコストを登録
                visited[tuple(new_sboard._array)] = new_sboard # 訪問済みリストに登録
                new_sboard.parent = now_board                  # 親盤面を登録
                new_sboard.move = coord['move']
                heappush(queue, (new_sboard.cost, new_sboard)) # 待ち行列に登録

    # 手順計算
    var = end                         # ゴール盤面をvarへ代入
    solution = []                     # solutionを作成

    # varが初期盤面になるまでループ
    while var != start:
        solution += [var._getsMove()] # solution配列に追加
        var = var.parent              # varに親盤面を代入

    solution.reverse()                # 配列を反転
    solution = ''.join(solution)      # 配列を文字列に変換

    return solution, No               # 解と実行回数を返す

# 現在の探索盤面からゴール盤面までの手数の予測値（マンハッタン距離）を計算するヒューリスティック関数
def calc_heuristic(array):
    board_list = array # 現在の盤面
    same = 0           # ゴール盤面と一致しないピースの数
    manhattan = 0      # マンハッタン距離

    # board_listの数だけループ
    for var in board_list:

        # ゴール盤面と一致しないピースの数を計算
        x, y = XY_coord(var)
        if goal_board1.index(var) != board_list.index(var): # ゴール盤面と一致しない時
            same += 1
            
        # ゴール盤面へ移動するときのマンハッタン距離
        pos = goal_board1.index(var)                               # ゴール盤面のピースの位置
        goal_board_x, goal_board_y = XY_coord(pos)                 # ゴール盤面のピースの位置をXY座標に変換
        x, y = XY_coord(board_list.index(var))                     # 現在の盤面のピースの位置をXY座標に変換
        manhattan += abs(x - goal_board_x) + abs(y - goal_board_y) # XY座標の絶対値を足したものをマンハッタン距離とする

    # heuristic = same + manhattan # 速くなるが最適解ではない
    heuristic = manhattan * HEURISTIC_MAGNIFICATION

    return heuristic

# 空の位置へ移動できる隣接マスを計算
def coord_next(x, y):
    coord_next_OK = [{'move': 'None', 'XY': [x, y]}] # 隣接マスの配列

    # up
    if (x - 1 >= 0): coord_next_OK.append({'move': 'U', 'XY': [x - 1, y]})

    # down
    if (x + 1 < No_X): coord_next_OK.append({'move': 'D', 'XY': [x + 1, y]})

    # right
    if (y + 1 < No_Y): coord_next_OK.append({'move': 'R', 'XY': [x, y + 1]})

    # left
    if (y - 1 >= 0): coord_next_OK.append({'move': 'L', 'XY': [x, y - 1]})

    return coord_next_OK

# 盤面配列からXY座標を取得
def XY_coord(index):
    x = index // No_Y # X座標
    y = index % No_Y  # Y座標
    return x, y        # XY座標を返す

# メイン関数
def main():
    global No_X, No_Y, init_board, goal_board1, goal_board2              # グローバル変数宣言
    global elected_position
    
    elected_position = 0                                                 # 選択位置
    No_X = 4                                                             # 盤面の縦の大きさ
    No_Y = 4                                                             # 盤面の横の大きさ
    init_board =  [3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12] # ボードの初期盤面 最短53手
    # init_board =  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 13, 14, 15] # ボードの初期盤面 right x3
    # init_board =  [1, 2, 3, 0, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12] # ボードの初期盤面 down x3
    # init_board =  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 0, 13] # ボードの初期盤面 left x3 (13選択時)
    # init_board =  [1, 2, 3, 8, 5, 6, 7, 12, 9, 10, 11, 0, 13, 14, 15, 4] # ボードの初期盤面 up x3 (4選択時)
    goal_board1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0] # ボードのゴール盤面1
    goal_board2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14, 0] # ボードのゴール盤面2

    if isSolvable(init_board): 
        print("Solvable")
    else:
        print("unsolvable")
        return

    timer_start = time.time() # 処理速度計測

    # shuffle(init_board)       # init_boardをシャッフルする
    solution, visit = astar() # astar()をsolution, visitに代入

    timer_end = time.time() # 処理速度計測

    print('処理時間: ', timer_end - timer_start) # ログ出力（処理速度）

    return solution, visit    # solution, visitを返す

# 答えをtextファイルに出力
def outputAnswer(solution):
    answer = ''

    # ランダムな数を生成（回転）
    for i in init_board: answer += str(random.randrange(3)) # 回転情報

    XY = XY_coord(init_board.index(elected_position)) # 選択位置のXY座標
    hex_X = str(hex(XY[1])).replace('0x','').upper()  # 10進数 -> 16進数
    hex_Y = str(hex(XY[0])).replace('0x','').upper()  # 10進数 -> 16進数

    answer += '\n1\n'                   # 選択回数
    answer += hex_X + hex_Y + '\n'      # 選択画像位置
    answer += str(len(solution)) + '\n' # 交換回数
    answer += solution                  # 交換操作

    print(answer)                    # answerを出力
    file = open('solution.txt', 'w') # solution.txtを開く
    file.write(answer)               # ファイルに書き込み
    file.close()                     # ファイルを閉じる

# ゴール可能かどうか判定
def isSolvable(arr):
    newarr = copy.copy(arr)
    x = XY_coord(newarr.index(elected_position))[0] + 1
    counts = x
    newarr.remove(elected_position)

    for i in range(len(newarr)):
        for j in range(len(newarr)-1, i, -1):
            if newarr[i] > newarr[j]:
                counts += 1
  
    return counts % 2 == 0

# 実行
if __name__ == '__main__':
    solution, visit = main()    # main()をsolution, visitに代入
    outputAnswer(solution)      # 答えを出力
