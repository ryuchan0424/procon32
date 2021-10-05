class Board():

    # コンストラクタ
    def __init__(self, board_list, distance, parent):
        self._array = board_list                        # 盤面
        self.distance = distance                        # 現在の探索盤面までの手数
        self.parent = parent                            # 親の盤面
        self.cost = self.distance                       # コスト（評価関数）
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