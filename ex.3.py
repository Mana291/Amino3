import pyxel
import random
#落下時にx座標を8の倍数、だけど左側に寄せるから時々空白が生まれてしまう＝なるべくぴったりと落としてもらう
class TetrisBlock:
    def __init__(self):
        self.x = 88 #落下時点
        self.y = 0
        self.size = 8 #1セルが８ピクセル
        self.velocity_y = 1
        self.rotation = 0
        self.stopped = False
        self.current_tetromino = self.get_random_tetromino()
        self.block_data = self.generate_block_data()
        self.block_colors = {'A': 3, 'G': 10, 'C': 8, 'U': 2}

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
        block_data = [[' ' for _ in range(len(self.current_tetromino[0]))] for _ in range(len(self.current_tetromino))]
        #len(self.current_tetromino) は、高さ、len(self.current_tetromino[0]) は、横幅
        for i in range(len(self.current_tetromino)):#列
            for j in range(len(self.current_tetromino[i])):#行
                if self.current_tetromino[i][j] == 1:#テトリミノの数字が１だった場合、そのセルの中にランダムに文字を入れる
                    block_data[i][j] = random.choice(['A', 'G', 'C', 'U'])
        return block_data

    def rotate_tetromino(self):#めっちゃ難しい
        rotated_tetromino = list(zip(*reversed(self.current_tetromino)))
        #reversed(self.current_tetromino) によって、行の順番が逆転
        #zip(*...)は各行を新しいグループにする
        #listでリスト[]に変換される
        original_block_data = self.block_data#現在のブロックのデータを original_block_data として保存
        self.current_tetromino = rotated_tetromino#テトロミノの形状を回転後の状態に更新
        self.block_data = self.generate_block_data()#新しいブロックのデータを生成
        for i in range(min(len(original_block_data), len(self.block_data))):
            #行数について、minで取得した2つの行数の小さい方の値を取得
            for j in range(min(len(original_block_data[i]), len(self.block_data[i]))):#同様に列について
                if self.current_tetromino[i][j] == 1:
                    self.block_data[i][j] = original_block_data[i][j]

    def adjust_position(self, stopped_blocks):
        for block in stopped_blocks:
            if (
                self.x < block[0] + self.size#テトロミノの右端がブロックの左端よりも左にある
                and self.x + self.size * len(self.current_tetromino[0]) > block[0]#テトロミノの左端がブロックの右端よりも右にある
                and self.y + self.size * len(self.current_tetromino) > block[1]#テトロミノの下端がブロックの上端よりも下にある
                and self.y < block[1] + self.size#テトロミノの上端がブロックの下端よりも上にある
            ):
                self.y = block[1] - self.size * len(self.current_tetromino)
                # 落下時にx座標を8の倍数
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
                # 落下時にx座標を8の倍数に補正
                self.x = (self.x // 8) * 8
                self.velocity_y = 0
                self.stopped = True
                if any(block[1] < 24 for block in stopped_blocks):
                    pyxel.quit()
                    return
            self.adjust_position(stopped_blocks)

            if self.stopped and not any(block[1] < 20 for block in stopped_blocks):
                pyxel.sound(0).set(notes='A2', tones='TT', volumes='3', effects='NN', speed=10)
                pyxel.play(0, 0)

    def draw(self):
        for i in range(len(self.current_tetromino)):
            for j in range(len(self.current_tetromino[i])):
                value = self.current_tetromino[i][j]
                if value == 1:
                    x_pos = self.x + j * self.size
                    y_pos = self.y + i * self.size
                    pyxel.rect(x_pos, y_pos, self.size, self.size, self.block_colors.get(self.block_data[i][j], 0))
                    #x_pos と y_pos の左上の座標
                    #self.size はブロックのサイズ、
                    #self.block_colors.get(self.block_data[i][j], 0) はブロックの色を指定
                    if not self.stopped:
                        pyxel.text(self.x + j * self.size + 2, self.y + i * self.size + 2, self.block_data[i][j], 0)

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
            #テトロミノが停止しており、かつブロックが画面上部に到達していない場合
            blocks.extend([
                (
                    tetris_block.x + j * tetris_block.size,
                    tetris_block.y + i * tetris_block.size,
                    tetris_block.block_data[i][j]
                )#ブロックの左上の x 座標,
                #ブロックの左上の y 座標,
                #blocks リストに、新しいブロックの情報を一括で追加
                for i in range(len(tetris_block.current_tetromino))
                for j in range(len(tetris_block.current_tetromino[i]))
                if tetris_block.current_tetromino[i][j] == 1
            ])
            tetris_block.adjust_position(blocks)
            tetris_block.__init__()
            if any(block[1] < 24 for block in blocks):#追加したブロックの中に、画面上部に到達したものがあるかどうかを確認
                game_over = True
            else:
                score += 1

def draw():
    pyxel.cls(7)
    # 縦線
    for x in range(0, pyxel.width, 8):
        pyxel.line(x, 0, x, pyxel.height, 6)

    # 横線
    for y in range(0, pyxel.height, 8):
        pyxel.line(0, y, pyxel.width, y, 6)
    
    for block in blocks:
        pyxel.rect(block[0], block[1], tetris_block.size, tetris_block.size, tetris_block.block_colors.get(block[2], 0))
        pyxel.text(block[0] + 2, block[1] + 2, block[2], 0)
        
    tetris_block.draw()
    pyxel.line(0, 24, pyxel.width, 24, 12)
    pyxel.text(10, 5, f"Score: {score}", 1)
    if game_over:
        pyxel.text(80, 90, "GAME OVER", pyxel.frame_count % 16)
        pyxel.text(40, 120, "press space button to restart", pyxel.frame_count % 16)

pyxel.init(200, 200)
pyxel.run(update, draw)
