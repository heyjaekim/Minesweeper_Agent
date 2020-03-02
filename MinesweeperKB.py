from enum import Enum

class KB():

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.tile_arr = [[Tile(x, y) for y in range(height)] for x in range(width)]
        self.mismatched_tiles = []

    def visitCurrentTile(self, tile, num):
            tile.visited = True
            tile.adj_mines = num
            tile.is_mined = ID.false
            i = self.check_adj_tiles(tile)
            if i >= 0:
                # Error conflict when discovering new node
                return
            else:
                self.mismatched_tiles.append(tile)
                print(self.mismatched_tiles)

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
                        
                        self.tile_arr[x][y].is_mined = ID.false #the tile is not mined
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
            #literally, potential_mine can be true or false depending on discovering 
            #more mines on adjcent tiles around the the tile or not
            #ex) count = 2 but tile.adj_mines is 3, which it returns -1(potentially mine)
            prev_mine_list.append(subset_end)

            # Local sat
            local_sat = self.check_local_grid(potential_mines[subset_end])
            
            
            if local_sat <= 0:
                continue

            elif local_sat == 0 and self.check_global_sat:
                return True

            elif local_sat >= 0:
                prev_mine_list.pop() #0 이 pop했을때 그럼 last_min_stack에 아무것도 없겠지?
                potential_mines[subset_end].is_mined = ID.false

    def check_adj_tiles(self, tile):
        count = 0

        # Count adjacent mines
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x, y = tile.x+i, tile.y+j
                if (self.isValid(x, y) 
                    and self.tile_arr[x][y].is_mined == ID.true
                        and not (x == tile.x and y == tile.y)):
                    count += 1
        #count the adj mines
        return count - tile.adj_mines
    
    def check_all_grid(self):
        for x in range(self.width):
            for y in range(self.height):
                t = self.tile_arr[x][y]
                if(t.visited and self.check_adj_tiles(t) != 0):
                    return False #this is when if there's at least one unsatisfied condition
                    #for checking mines = count - tile.adj_mines which has to be 0 globally.
        return True

    def check_local_grid(self, tile):

        under_satisfied = False
        # Count adjacent mines of neighbors of tile
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x, y = tile.x+i, tile.y+j
                if (self.isValid(x, y)):
                    if not self.tile_arr[x][y].visited:
                        continue
                    count = self.check_adj_tiles(self.tile_arr[x][y])
                    if count > 0:
                        # too many mines, oversatisfied
                        return 1
                    elif count < 0:
                        # under satisfied at one point, but don't return
                        # since it still may over satisfy at one point
                        under_satisfied = True
        # if it is not under satisfied then it's satisfied locally
        if under_satisfied:
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
                    count = self.check_adj_tiles(adj_tile)
                    if count == 0:
                        #remove when adj_tile == 1?
                        self.mismatched_tiles.remove(adj_tile)

    def printGrid(self):
        t = ""
        for y in range(self.height):
            for x in range(self.width):
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
                    else:
                        #covered
                        t += "X "
            t += "\n"
        print(t)

    def get_hidden_adj_tiles(self, tile):
        
        adj_tiles = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x, y = tile.x+i, tile.y+j
                if (self.isValid(x, y) and self.tile_arr[x][y].is_mined is ID.hidden 
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
        self.adj_mines = -9
        self.blowup = False

    def coord_str(self):
        return f"({self.x},{self.y})"