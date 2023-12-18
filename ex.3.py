import pyxel
import random

class TetrisBlock:
    def __init__(self):
        self.x = 90
        self.y = 0
        self.size = 8  # テトリミノのサイズを変更
        self.velocity_y = 1  # 落下速度を変更
        self.rotation = 0
        self.stopped = False
        self.current_tetromino = self.get_random_tetromino()

    def get_random_tetromino(self):
        tetrominos = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1, 0], [1, 1, 1]]
        ]
        return random.choice(tetrominos)

    def update(self):
        if not self.stopped:
            # 左右移動
            if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
                self.x -= 2
            elif pyxel.btn(pyxel.KEY_RIGHT) and self.x < pyxel.width - self.size * len(self.current_tetromino[0]):
                self.x += 2

            # 下を押したら加速して落下
            elif pyxel.btn(pyxel.KEY_DOWN):
                self.velocity_y += 0.1

            # 上を押したら一番下まで行く
            elif pyxel.btn(pyxel.KEY_UP):
                self.y = pyxel.height - self.size * len(self.current_tetromino)
                self.velocity_y = 0
                self.stopped = True

            # 位置更新
            self.y += self.velocity_y

            # 画面の一番下に到達したら停止
            if self.y + self.size * len(self.current_tetromino) >= pyxel.height:
                self.y = pyxel.height - self.size * len(self.current_tetromino)
                self.velocity_y = 0
                self.stopped = True

            # スペースキーで回転させたいけど分からない
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.rotation = (self.rotation + 90) % 360

    def draw(self):
        for i, row in enumerate(self.current_tetromino):
            for j, value in enumerate(row):
                if value == 1:
                    pyxel.rect(self.x + j * self.size, self.y + i * self.size, self.size, self.size, 8)

# 初回の TetrisBlock インスタンス生成
tetris_block = TetrisBlock()
blocks = []  # 落下済みのブロックを保存するリスト

# メインループ
def update():
    tetris_block.update()

    if tetris_block.stopped:
        blocks.extend([(tetris_block.x + j * tetris_block.size, tetris_block.y + i * tetris_block.size) 
                       for i, row in enumerate(tetris_block.current_tetromino) 
                       for j, value in enumerate(row) if value == 1])
        tetris_block.__init__()

def draw():
    pyxel.cls(7)
    for block in blocks:
        pyxel.rect(block[0], block[1], tetris_block.size, tetris_block.size, 8)
    tetris_block.draw()

# 初回実行
pyxel.init(200, 200)
pyxel.run(update, draw)
