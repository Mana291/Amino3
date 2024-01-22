import pyxel
import random

class TetrisBlock:
    def __init__(self):
        self.x = 88  # 落下時点のx座標
        self.y = 0  # 落下時点のy座標
        self.size = 8  # 1セルが８ピクセル
        self.velocity_y = 1  # 落下速度
        self.rotation = 0  # 回転状態
        self.stopped = False  # ブロックが停止したかどうかのフラグ
        self.current_tetromino = self.get_random_tetromino()  # ランダムなテトリミノの形
        self.block_data = self.generate_block_data()  
        self.block_colors = {'A': 3, 'G': 10, 'C': 8, 'U': 2}  # ブロックの文字に対する色

    def get_random_tetromino(self):
        tetrominos = [
            [[1, 1, 1, 1]],  # 一列
            [[1, 1], [1, 1]],  # 正方形
            [[0, 1, 1], [1, 1, 0]],  # L字型っぽいやつ
            [[1, 1, 0], [0, 1, 1]],  # L字型の逆
            [[0, 1, 0], [1, 1, 1]]  # T字型
        ]
        return random.choice(tetrominos)

    def generate_block_data(self):
        return [[' ' if cell == 0 else random.choice(['A', 'G', 'C', 'U']) for cell in row] for row in self.current_tetromino]

    def rotate_tetromino(self):
        self.current_tetromino = list(zip(*reversed(self.current_tetromino)))
        self.block_data = self.generate_block_data()
        #reversed(self.current_tetromino) でself.current_tetromino の行を逆順
        #zip(*reversed(self.current_tetromino)) を使って列と行を入れ替える
        #組み合わされた要素をリストに変換して、行の反転と列の入れ替えをすることで、90度反時計回りに回転

    def adjust_position(self, stopped_blocks):
        for block in stopped_blocks:
            if (
                self.x < block[0] + self.size#テトロミノの右端がブロックの左端よりも左にある
                and self.x + self.size * len(self.current_tetromino[0]) > block[0]#テトロミノの左端がブロックの右端よりも右にある
                and self.y + self.size * len(self.current_tetromino) > block[1]#テトロミノの下端がブロックの上端よりも下にある
                and self.y < block[1] + self.size#テトロミノの上端がブロックの下端よりも上にある
            ):
                self.y = block[1] - self.size * len(self.current_tetromino)
                #block[1] は stopped_blocks リスト内の各ブロックの左上の y 座標
                # 落下時にx座標を8の倍数にする
                self.x = (self.x // 8) * 8
                self.velocity_y = 0
                self.stopped = True

    def update(self, stopped_blocks):
        if not self.stopped:
            if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
                self.x -= 2
            elif pyxel.btn(pyxel.KEY_RIGHT) and self.x < pyxel.width - self.size * len(self.current_tetromino[0]):
                self.x += 2
            elif pyxel.btn(pyxel.KEY_DOWN):
                self.velocity_y += 0.2
            elif pyxel.btnp(pyxel.KEY_SPACE):
                self.rotate_tetromino()
            self.y += self.velocity_y
            if self.y + self.size * len(self.current_tetromino) >= pyxel.height:
                self.y = pyxel.height - self.size * len(self.current_tetromino)
                # 落下時にx座標を8の倍数に
                self.x = (self.x // 8) * 8
                self.velocity_y = 0
                self.stopped = True
                if any(block[1] < 24 for block in stopped_blocks):
                    pyxel.quit()
                    return
            self.adjust_position(stopped_blocks)

            if self.stopped and not any(block[1] < 24 for block in stopped_blocks):
                pyxel.sound(0).set(notes='A2', tones='TT', volumes='3', effects='NN', speed=10)
                pyxel.play(0, 0)

    def draw(self):
        for i in range(len(self.current_tetromino)):#行数に対して
            for j in range(len(self.current_tetromino[i])):#列数に対して
                value = self.current_tetromino[i][j]#セル
                if value == 1:
                    x_nagasa = self.x + j * self.size
                    y_nagasa = self.y + i * self.size
                    pyxel.rect(x_nagasa, y_nagasa, self.size, self.size, self.block_colors.get(self.block_data[i][j], 0))
                    pyxel.text(x_nagasa + 2, y_nagasa + 2, self.block_data[i][j], 0)

tetris_block = TetrisBlock()
blocks = []
game_over = False
score = 0

def update():
    global blocks, game_over, score
    if game_over and pyxel.btnp(pyxel.KEY_SPACE):
        blocks.clear()
        tetris_block.__init__()
        game_over = False
        score = 0
    elif not game_over:
        tetris_block.update(blocks)
        if tetris_block.stopped and not any(block[1] < 24 for block in blocks):
            blocks.extend([(tetris_block.x + j * tetris_block.size, tetris_block.y + i * tetris_block.size, tetris_block.block_data[i][j]) for i in range(len(tetris_block.current_tetromino)) for j in range(len(tetris_block.current_tetromino[i])) if tetris_block.current_tetromino[i][j] == 1])
            tetris_block.adjust_position(blocks)
            tetris_block.__init__()
            if any(block[1] < 24 for block in blocks):
                game_over = True
            else:
                score += 1

def draw():
    pyxel.cls(7)
    for x in range(0, pyxel.width, 8):#縦線
        pyxel.line(x, 0, x, pyxel.height, 6)
    for y in range(0, pyxel.height, 8):#横線
        pyxel.line(0, y, pyxel.width, y, 6)
    for block in blocks:
        pyxel.rect(block[0], block[1], tetris_block.size, tetris_block.size, tetris_block.block_colors.get(block[2], 0))
        pyxel.text(block[0] + 2, block[1] + 2, block[2], 0)
    tetris_block.draw()
    pyxel.line(0, 24, pyxel.width, 24, 12)
    pyxel.text(10, 5, "Score: " + str(score), 1)
    if game_over:
        pyxel.text(80, 90, "GAME OVER", pyxel.frame_count % 16)
        pyxel.text(40, 120, "press space button to restart", pyxel.frame_count % 16)

pyxel.init(200, 200)
pyxel.run(update, draw)
