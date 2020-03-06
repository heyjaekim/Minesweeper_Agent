from enum import Enum
import numpy as np

class KB():

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.tile_arr = [[Tile(x, y) for y in range(height)] for x in range(width)]
        self.mismatched_tiles = []
        self.prob_grid = np.zeros((height, width))


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
                for i in range(len(self.mismatched_tiles)):
                    print("print the mismatch tiles: x = " 
                    + str(self.mismatched_tiles[i].x) +" y = "+ 
                    str(self.mismatched_tiles[i].y) + " adj_mines = "+
                    str(self.mismatched_tiles[i].adj_mines))

    def isValid(self, x, y):
        if(x < 0 or x >= self.width) or (y<0 or y >= self.height):
            return False
        else:
            return True        

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
        for x in range(self.width):
            for y in range(self.height):
                t = self.tile_arr[x][y]
                if(t.visited and self.check_adj_mines(t) != 0):
                    return False #this is when if there's at least one unsatisfied condition
                    #for checking mines = count - tile.adj_mines which has to be 0 globally.
        return True


    def get_local_fringe(self, tile):
        local_fringe_set = set()
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x, y = tile.x+i, tile.y+j
                if (self.isValid(x, y) and not self.tile_arr[x][y].visited):
                    local_fringe_set.add(self.tile_arr[x][y])
        return local_fringe_set

    #TODO: idea for the improved Knowledge base is to gather all the global fringe for the visited tiles and then compute the probability for everytiles.
    #According to the each tile, it would have the adj_mine number assigned, and by finding the maximum probability of those fringe aroudn the visited tile,
    #we can assign the tile as a flag(mine) and proceed another tile to mark flags as well.
    def compute_global_prob(self):
        global_fringe_set = set()
        visited_tiles = set()

        #add_global_fringe
        for x in range(self.width):
            for y in range(self.height):
                #bring visited cells
                t = self.tile_arr[x][y]
                if(t.visited):
                    t.mine_prob = 0
                    visited_tiles(t)
                    global_fringe_set.add(get_local_fringe(t))
                else:
                    t.mine_prob = 0
        
        for tile in visited_tiles:
            
            tile_fringe = list()
            tile_fringe.append(get_local_fringe(tile))
            each_tile_prob = tile.adj_mines/len(tile_fringe)
            
            for adj_tile in tile_fringe:
                
                if not adj_tile.visited:
                    adj_tile.mine_prob += each_tile_prob
            
        for tile in visited_tiles:

            #possible_mines = getPossibleMine(tile)
            #possible_clears = getPossibleClear(tile)
            setPossibleMine(tile)
            setPossibleClear(tile)
        
    def checkNum(self, num, cur_tile):
        if num == 9:
            print("gameover x = " + str(cur_tile.x))
            print("gameover y = " + str(cur_tile.y))
            self.gameover = True
            self.won = False
            return
        elif num >= 0 and num <= 8:
            self.kb.visitCurrentTile(cur_tile, num)
        else:
            # Error invalid num
            return

    def checkQuery(self, x, y):
        # returns 0-8 for num of adj mines or 9 if the tile is mined
        num = int(self.gamesetting.grid[x][y]) #IndexError: index 10 is out of bounds for axis 0 with size 10
        cur_tile = self.kb.tile_arr[x][y]
        self.checkNum(num, cur_tile)
        return cur_tile    


    def setPossibleMine(self, tile):
        max_tile = tile
        possible_mines = set()

        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x, y = tile.x+i, tile.y+j
                if (self.isValid(x, y) 
                    and not self.tile_arr[x][y].visited
                        and self.tile_arr[x][y].mine_prob >= max_tile.mine_prob
                            and self.tile_arr[x][y].is_mined is ID.hidden):
                        max_tile = self.tile_arr[x][y]
        if(self.tile_arr[x][y].mine_prob >= 0.99):
            max_tile.is_mined = ID.true
            max_tile.visited = True
        else: 
            possible_mines.add(max_tile)
            
        return possible_mines
    
    def setPossibleClear(self, tile):
        safest_tiles = list()
        max_tile = 1

        #get current maximum mine probability from the adj_tiles
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x, y = tile.x+i, tile.y+j
                if (self.isValid(x, y) 
                    and not self.tile_arr[x][y].visited
                        and self.tile_arr[x][y].mine_prob < max_tile):
                        max_tile = self.tile_arr[x][y].mine_prob
        
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x, y = tile.x+i, tile.y+j
                if (self.isValid(x, y) 
                    and not self.tile_arr[x][y].visited
                        and self.tile_arr[x][y].mine_prob <= max_tile.mine_prob):
                        safest_tiles.append(self.tile_arr[x][y])
        
        for safe_tile in safest_tiles:
            safe_tile.is_mined = ID.false
            safe_tile.visited = True

        return safest_tiles


    #def compute_global_probability(self, fringe):


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
        for x in range(self.width):
            for y in range(self.height):
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
        self.mine_prob = 0

    def coord_str(self):
        return f"({self.x},{self.y})"