import tkinter as tk
import random

class Game2048(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()
        self.init_game()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=400, height=400, bg='white')
        self.canvas.grid()
        self.new_game_button = tk.Button(self, text='New game', command=self.init_game)
        self.new_game_button.grid()
        self.score_label = tk.Label(self, text='Score: 0')
        self.score_label.grid()
        self.tile_colors = {
            2: '#EEE4DA',
            4: '#EDE0C8',
            8: '#F2B179',
            16: '#F59563',
            32: '#F67C5F',
            64: '#F65E3B',
            128: '#EDCF72',
            256: '#EDCC61',
            512: '#EDC850',
            1024: '#EDC53F',
            2048: '#EDC22E'
        }

    def init_game(self):
        self.tiles = [[0 for j in range(4)] for i in range(4)]
        self.score = 0
        self.add_tile()
        self.add_tile()
        self.update_board()

    def add_tile(self):
        #новая плитка 
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.tiles[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.tiles[i][j] = 2 if random.random() < 0.9 else 4

    def update_board(self):
        #обновление доски 
        self.canvas.delete('tile')
        for i in range(4):
            for j in range(4):
                x0, y0 = j*100, i*100
                x1, y1 = x0+100, y0+100
                value = self.tiles[i][j]
                color = self.tile_colors.get(value, '#FFFFFF')
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tag='tile')
                if value:
                    self.canvas.create_text(x0+50, y0+50, text=str(value), tag='tile')

        self.score_label.config(text='Score: {}'.format(self.score))
        self.update()

    def slide(self, row):
        #объединение соседних 
        new_row = [i for i in row if i != 0]
        for i in range(len(new_row)-1):
            if new_row[i] == new_row[i+1]:
                new_row[i], new_row[i+1] = new_row[i]*2, 0
                self.score += new_row[i]
        new_row = [i for i in new_row if i != 0]
        new_row += [0] * (4 - len(new_row))
        return new_row

    def move(self, direction):
        #cдвиги
        if direction == 'left':
            self.tiles = [self.slide(row) for row in self.tiles]
        elif direction == 'right':
            self.tiles = [self.slide(row[::-1])[::-1] for row in self.tiles]
        elif direction == 'up':
            self.tiles = [list(row) for row in zip(*self.tiles)]
            self.tiles = [self.slide(row) for row in self.tiles]
            self.tiles = [list(row) for row in zip(*self.tiles)]
        elif direction == 'down':
            self.tiles = [list(row[::-1])[::-1] for row in zip(*self.tiles)]
            self.tiles = [self.slide(row[::-1])[::-1] for row in self.tiles]
            self.tiles = [list(row[::-1])[::-1] for row in zip(*self.tiles)]

        self.add_tile()
        self.update_board()

    def game_over(self):
        #проверка на конец игры
        for i in range(4):
            for j in range(4):
                if self.tiles[i][j] == 0:
                    return False
                if j < 3 and self.tiles[i][j] == self.tiles[i][j+1]:
                    return False
                if i < 3 and self.tiles[i][j] == self.tiles[i+1][j]:
                    return False
        return True

root = tk.Tk()
root.title('Game 2048')
game = Game2048(root)

root.bind('<Left>', lambda event: game.move('left'))
root.bind('<Right>', lambda event: game.move('right'))
root.bind('<Up>', lambda event: game.move('up'))
root.bind('<Down>', lambda event: game.move('down'))

game.mainloop()
