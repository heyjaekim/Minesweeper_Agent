import numpy as np
from random import randint

class ImprovedSetting(object):

    def __init__(self, dim, num_mines):
        self.dim = dim
        self.num_mines = num_mines
        self.grid = [[0 for x in range(dim)]for y in range(dim)]
        self.hidden_grid = [[0 for x in range(dim)]for y in range(dim)]
        self.generate_new_grid()
        self.identified_num = 0


    def get_adjacent_count(self, x, y):
        count = 0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x_val, y_val = x+i, y+j
                if (self.isValid(x_val, y_val) and
                        self.grid[x_val][y_val] == -1
                        and not (x_val == x and y_val == y)):
                    count += 1
        return count

    def isValid(self, x, y):
        if(x < 0 or x >= self.dim) or (y<0 or y >= self.dim):
            return False
        else:
            return True

    def generate_new_grid(self):
        # Place the mines
        num_of_mines = self.num_mines
        while num_of_mines > 0:
            i, j = randint(0, self.dim-1), randint(0, self.dim-1)
            if self.grid[i][j] != -1:
                self.grid[i][j] = -1
                num_of_mines -= 1

        # Set the clues
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if self.grid[i][j] != -1:
                    self.grid[i][j] = self.get_adjacent_count(i, j)

        for i in range(self.dim):
            print(self.grid[i])
        print("--------------------------")

    def nextStep(self):
        for i in range(self.dim):
            for j in range(self.dim):
                if self.hidden_grid[i][j] == 2:
                    self.hidden_grid[i][j] = 1

    def mark_mine(self, tile):
        self.hidden_grid[tile[0]][tile[1]] = -1
        self.identified_num += 1

    def mark_safe(self, tile):
        self.hidden_grid[tile[0]][tile[1]] = 2

    def mark_uncover(self, tile):
        self.hidden_grid[tile[0]][tile[1]] = 1
        self.identified_num += 1

    def processQuery(self, x, y, proceed):
        if self.grid[x][y] == -1:
            self.mark_uncover((x,y))
            return False

        elif proceed is True:
            self.mark_safe((x,y))

        else:
            self.mark_uncover((x,y))
        return self.grid[x][y]
