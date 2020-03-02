import numpy as np
from random import randint


class GameSetting:
    def __init__(self, height, width, num_mines):
        self.height = height
        self.width = width
        self.num_mines = num_mines
        self.grid = np.zeros((width, height))
        self.generate_new_grid()

    def get_adjacent_count(self, x, y):
        
        count = 0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x_val, y_val = x+i, y+j
                if (self.isValid(x_val, y_val) and
                        self.grid[x_val][y_val] == 9
                        and not (x_val == x and y_val == y)):
                    count += 1
        return count

    def isValid(self, x, y):
        if(x < 0 or x >= self.width) or (y<0 or y >= self.height):
            return False
        else:
            return True

    '''FUNCTION FOR GENERATING BOMBS ON THE GRID'''
    def generate_new_grid(self):
        # Place the mines
        num_of_mines = self.num_mines
        while num_of_mines > 0:
            i, j = randint(0, self.width-1), randint(0, self.height-1)
            if self.grid[i][j] != 9:
                self.grid[i][j] = 9
                num_of_mines -= 1
        # Set the clues
        for i in range(0, self.width):
            for j in range(0, self.height):
                if self.grid[i][j] != 9:
                    self.grid[i][j] = self.get_adjacent_count(i, j)
