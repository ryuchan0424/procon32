import cv2
import time


# グローバル変数
PATH_IMG = './test_server/1-1.ppm' # 問題画像Path
PATH_SOLUTION = 'solution.txt' # 解答Path


# メイン関数
def main():
    timer_start = time.time()
    
    ### 処理開始 ###
    solution = read_solution()
    print(solution)

    img = read_img()
    print(img)

    cv2.imshow("image", img)
    cv2.waitKey(0) #キーボードが押されるまで待機

    ### 処理終了 ###

    timer_end = time.time()
    print('time  : ', timer_end - timer_start)


# 問題画像読み込み
def read_img():
    img = cv2.imread(PATH_IMG, cv2.IMREAD_COLOR)

    return img



# 解答読み込み
def read_solution():
    file = open(PATH_SOLUTION, 'r', encoding='UTF-8') # 開く
    data = file.read() # データ
    file.close() # 閉じる

    data = data.split('\n') # 改行ごとに分割

    return data


# 実行
if __name__ == '__main__':
    main()
