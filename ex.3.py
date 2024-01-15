import pyxel
import random
#音が鳴る
class TetrisBlock:
    def __init__(self):
        self.x = 90
        self.y = 0
        self.size = 8
        self.velocity_y = 1
        self.rotation = 0
        self.stopped = False
        self.current_tetromino = self.get_random_tetromino()
        self.block_data = self.generate_block_data()
        self.block_colors = {'A': 3, 'G': 10, 'C': 8, 'U': 2}

    def get_random_tetromino(self):
        tetrominos = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1, 0], [1, 1, 1]]
        ]
        return random.choice(tetrominos)

    def generate_block_data(self):
        block_data = [[' ' for _ in range(len(self.current_tetromino[0]))] for _ in range(len(self.current_tetromino))]
        for i in range(len(self.current_tetromino)):
            for j in range(len(self.current_tetromino[i])):
                if self.current_tetromino[i][j] == 1:
                    block_data[i][j] = random.choice(['A', 'G', 'C', 'U'])
        return block_data

    def rotate_tetromino(self):
        rotated_tetromino = list(zip(*reversed(self.current_tetromino)))
        original_block_data = self.block_data
        self.current_tetromino = rotated_tetromino
        self.block_data = self.generate_block_data()
        for i in range(min(len(original_block_data), len(self.block_data))):
            for j in range(min(len(original_block_data[i]), len(self.block_data[i]))):
                if self.current_tetromino[i][j] == 1:
                    self.block_data[i][j] = original_block_data[i][j]

    def adjust_position(self, stopped_blocks):
        for block in stopped_blocks:
            if (
                self.x < block[0] + self.size
                and self.x + self.size * len(self.current_tetromino[0]) > block[0]
                and self.y + self.size * len(self.current_tetromino) > block[1]
                and self.y < block[1] + self.size
            ):
                self.y = block[1] - self.size * len(self.current_tetromino)
                self.velocity_y = 0
                self.stopped = True

    def update(self, stopped_blocks):
        if not self.stopped:
            if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
                self.x -= 8
            elif pyxel.btn(pyxel.KEY_RIGHT) and self.x < pyxel.width - self.size * len(self.current_tetromino[0]):
                self.x += 8
            elif pyxel.btn(pyxel.KEY_DOWN):
                self.velocity_y += 0.2
            elif pyxel.btnp(pyxel.KEY_SPACE):
                self.rotate_tetromino()
            self.y += self.velocity_y
            if self.y + self.size * len(self.current_tetromino) >= pyxel.height:
                self.y = pyxel.height - self.size * len(self.current_tetromino)
                self.velocity_y = 0
                self.stopped = True
                if any(block[1] < 20 for block in stopped_blocks):
                    pyxel.quit()
                    return
            self.adjust_position(stopped_blocks)

            # Play a sound when a block stops
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
        if tetris_block.stopped and not any(block[1] < 20 for block in blocks):
            blocks.extend([
                (
                    tetris_block.x + j * tetris_block.size,
                    tetris_block.y + i * tetris_block.size,
                    tetris_block.block_data[i][j]
                )
                for i in range(len(tetris_block.current_tetromino))
                for j in range(len(tetris_block.current_tetromino[i]))
                if tetris_block.current_tetromino[i][j] == 1
            ])
            tetris_block.adjust_position(blocks)
            tetris_block.__init__()
            if any(block[1] < 20 for block in blocks):
                game_over = True
            else:
                score += 1

def draw():
    pyxel.cls(7)
    pyxel.line(0, 20, pyxel.width, 20, 12)
    pyxel.text(10, 5, f"Score: {score}", 1)
    for block in blocks:
        pyxel.rect(block[0], block[1], tetris_block.size, tetris_block.size, tetris_block.block_colors.get(block[2], 0))
        pyxel.text(block[0] + 2, block[1] + 2, block[2], 0)
    tetris_block.draw()

    if game_over:
        pyxel.text(80, 90, "GAME OVER", pyxel.frame_count % 16)
        pyxel.text(40, 120, "press space button to restart", pyxel.frame_count % 16)

pyxel.init(200, 200)
pyxel.run(update, draw)
