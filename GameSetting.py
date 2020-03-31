import numpy as np
from random import randint
from enum import Enum


class GameSetting:
    def __init__(self, dim, num_mines):
        self.dim = dim
        self.num_mines = num_mines
        self.grid = np.zeros((dim, dim))
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
        if(0 <= x < self.dim) and (0 <= y < self.dim):
            return True
        else:
            return False

    '''FUNCTION FOR GENERATING BOMBS ON THE GRID'''
    def generate_new_grid(self):
        # Place the mines
        num_of_mines = self.num_mines
        while num_of_mines > 0:
            i, j = randint(0, self.dim-1), randint(0, self.dim-1)
            if self.grid[i][j] != 9:
                self.grid[i][j] = 9
                num_of_mines -= 1
        # Set the clues
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if self.grid[i][j] != 9:
                    self.grid[i][j] = self.get_adjacent_count(i, j)


class KB():

    def __init__(self, dim):
        self.dim = dim
        self.tile_arr = [[Tile(x, y) for y in range(dim)] for x in range(dim)]
        self.mismatched_tiles = []

    def visitCurrentTile(self, tile, num):
            tile.visited = True
            tile.adj_mines = num
            tile.is_mined = ID.false
            i = self.check_adj_mines(tile)
            if i >= 0:
                # Error conflict when discovering new node
                return
            else:
                self.mismatched_tiles.append(tile)
                '''
                for i in range(len(self.mismatched_tiles)):
                    print("print the mismatch tiles: x = "
                    + str(self.mismatched_tiles[i].x) +" y = "+
                    str(self.mismatched_tiles[i].y) + " adj_mines = "+
                    str(self.mismatched_tiles[i].adj_mines))
                '''
    def isValid(self, x, y):
        if(0 <= x < self.dim) and (0 <= y < self.dim):
            return True
        else:
            return False

    def is_mine_or_clear(self):

        potential_mines = set()

        for unsat_tile in self.mismatched_tiles:

            # Count adjacent mines
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    x, y = unsat_tile.x+i, unsat_tile.y+j
                    if (self.isValid(x, y) and self.tile_arr[x][y].is_mined is ID.hidden):

                        #the tile is not mined
                        self.tile_arr[x][y].is_mined = ID.false
                        potential_mines.add(self.tile_arr[x][y])

        #condition of the possible mines: isValid, hidden.
        potential_mines = list(potential_mines)
        prev_mine_list = []
        subset_end = -1 #starts at -1 because for checking each of the list in possible mines

        while True:
            #condition to verify every tile from potential_mines have checked
            if subset_end+1 >= len(potential_mines):
                global_sat = self.check_all_grid()
                if global_sat is True:
                    return True
                else:
                    if len(prev_mine_list) == 0:
                        return False
                    subset_end = prev_mine_list.pop()
                    potential_mines[subset_end].is_mined = ID.false
                    continue

            # Add Mine
            subset_end += 1
            potential_mines[subset_end].is_mined = ID.true
            temp_mine_tile = potential_mines[subset_end]
            #literally, potential_mine can be true or false depending on discovering
            #more mines on adjcent tiles around the the tile or not
            #ex) count = 2 but tile.adj_mines is 3, which it returns -1(potentially mine)
            prev_mine_list.append(subset_end)

            # Local sat
            local_sat = self.check_local_grid(temp_mine_tile)
            if local_sat <= 0:
                #take into consideration for the temp_mine_tile as a real mine
                continue

            elif local_sat > 0:
                #process to remove the consideration about the tmp_mine_tile is the real mine
                prev_mine_list.pop()
                potential_mines[subset_end].is_mined = ID.false

    def check_adj_mines(self, tile):
        count = 0
        # Count adjacent mines
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x, y = tile.x+i, tile.y+j
                if (self.isValid(x, y)
                    and self.tile_arr[x][y].is_mined == ID.true
                        and not (x == tile.x and y == tile.y)):
                    count += 1
        #count the number of hidden neighbors, every hidden neighbor is a mine.
        hidden_mines = count - tile.adj_mines
        return hidden_mines

    def check_adj_safes(self, tile):
        count = 0
        #Count adjacent mines
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x, y = tile.x+i, tile.y+j
                if (self.isValid(x, y)
                    and self.tile_arr[x][y].is_mined == ID.false
                        and not (x == tile.x and y == tile.y)):
                    count += 1
        #count the number of hidden neighbors, every hidden neighbor is safe.
        hidden_safe = (8 - tile.adj_mines) - count
        return hidden_safe


    def check_all_grid(self):
        for x in range(self.dim):
            for y in range(self.dim):
                t = self.tile_arr[x][y]
                if(t.visited and self.check_adj_mines(t) != 0):
                    return False #this is when if there's at least one unsatisfied condition
                    #for checking mines = count - tile.adj_mines which has to be 0 globally.
        return True

    def check_local_grid(self, tile):

        satisfiaction = False
        # Count adjacent mines of neighbors of tile
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x, y = tile.x+i, tile.y+j
                if (self.isValid(x, y)):
                    if not self.tile_arr[x][y].visited:
                        continue

                    #counted the number of the hidden mines
                    hiddenMines = self.check_adj_mines(self.tile_arr[x][y])
                    if hiddenMines > 0:
                        # too many mines, oversatisfied
                        return 1

                    elif hiddenMines < 0:
                        # under satisfied at one point, but don't return
                        # since it still may over satisfy at one point
                        satisfiaction = True

        # if it is not under satisfied then it's satisfied locally
        if satisfiaction:
            return -1
        else:
            return 0

    def flagOnTile(self, tile):
        tile.is_mined = ID.true

        # Count adjacent mines of neighbors of tile
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x, y = tile.x+i, tile.y+j
                if (self.isValid(x, y)):
                    adj_tile = self.tile_arr[x][y]
                    hiddenMines = self.check_adj_mines(adj_tile)

                    if hiddenMines == 0:
                        #remove when adj_tile == 1?
                        self.mismatched_tiles.remove(adj_tile)
    
    def drawGrid(self):
        t = ""
        for x in range(self.dim):
            for y in range(self.dim):
                tile = self.tile_arr[x][y]

                if tile.is_mined is ID.true:
                    t += "M "

                elif tile.visited:
                    t += str(tile.adj_mines)+" "

                else:
                    if tile.is_mined is ID.false:
                        #unvsiited clear tile
                        t += "C "
                    elif tile.blowup is True:
                        t += "B "
                    else: #covered
                        t += "X "
            t += "\n"
        print(t)
    
    def get_hidden_adj_tiles(self, tile):

        adj_tiles = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x, y = tile.x+i, tile.y+j
                if (self.isValid(x, y)
                    and self.tile_arr[x][y].is_mined is ID.hidden
                        and not(x == tile.x and y == tile.y)):
                    adj_tiles.append(self.tile_arr[x][y])
        return adj_tiles

class ID(Enum):
    true = 1
    false = 2
    hidden = 3

class Tile():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.is_mined = ID.hidden
        self.adj_mines = -99
        self.blowup = False

    def coord_str(self):
        return f"({self.x},{self.y})"
