from MinesweeperKB import KB, ID
from GameSetting import GameSetting
from copy import deepcopy
import random
from enum import Enum

class ImprovedAgent:

    def __init__(self):
        height,width,num_mines = (5,5,5)

        self.height = height
        self.width = width
        self.kb = KB(height, width)
        self.gamesetting = GameSetting(height, width, num_mines)
        self.gameover = False
        self.won = False

    def startGame(self):
        '''
        Decide the random tile to query and we examine the tile is safe to declare 
        as mine or unvisited cleaer tile.
        Once we have to guess the tile, we select one tile from the fringe.
        '''
        
        #clear tiles are basically unvisited clear tiles
        clear_tiles = set()
        fringe = set() # unknown tiles that are adjacent to discovered nodes
        
        #randomly starts at the cell of the grid
        randX, randY= random.randint(0, self.width-1), random.randint(0, self.height-1)
        #first_tile = self.checkQuery(0, 0)
        first_tile = self.checkQuery(randX, randY)
        
        #Now assign below four var and lists to keep tracking the position of the uncovering cell
        prev_tile = first_tile

        #first tile 주변 모든 adjcent tile들을 여기에 append시킨다
        adj_unvisited = self.kb.get_hidden_adj_tiles(first_tile)
        
        for tile in adj_unvisited:
            fringe.add(tile)
        while not self.gameover:
            print("")

            if len(clear_tiles) != 0:
                # If there are any safe nodes to go to make those moves
                
                print("Clear tiles:" + str(len(clear_tiles)))                
                print("Current state of the knowledge base")
                self.kb.drawGrid()
                print("--------------------------------------")
                
                tile = clear_tiles.pop()
                self.checkQuery(tile.x,tile.y)
                print("Visiting tile: "+tile.coord_str())
                if(self.gameover is True):
                    tile.blowup = True
                    print("TERMINATE THE GAME")
                    break
                adj_unvisited = self.kb.get_hidden_adj_tiles(tile)
                for t in adj_unvisited:
                    fringe.add(t)
                prev_tile = tile

            '''first_tile starts here when the unvis_clr_tileSet is empty'''
            if len(fringe) != 0:
                # There is no safe tile to visit according to the the fringe
                removing_tiles = []
                for tile in fringe:
                    is_tile_mined = self.test_knowledgebase(tile.x,tile.y)
                    
                    if is_tile_mined is not ID.hidden:
                        
                        if is_tile_mined is ID.true:
                            self.kb.flagOnTile(tile)
                            print(tile.coord_str()+ " flagged as mine")
                            self.kb.drawGrid()
                        
                        elif is_tile_mined is ID.false:                       
                            tile.is_mined = ID.false
                            clear_tiles.add(tile)
                            print(tile.coord_str()+ " flagged as clear")
                            self.kb.drawGrid()

                        removing_tiles.append(tile)
                        continue

                for tile in removing_tiles:
                    fringe.remove(tile)
                    
                if len(clear_tiles) == 0 and len(fringe) != 0:
                    #Guess one tile from the from the hiddle tiles under the condition 
                    #if there are no more clear tiles surrounded by the safe tiles.
                    guess = fringe.pop()
                    print("guessing: "+str(guess.x)+','+str(guess.y))
                    clear_tiles.add(guess)

                
            elif len(clear_tiles) == 0:
                
                candidates = []
                for i in range(len(self.kb.tile_arr)):
                    for j in range(len(self.kb.tile_arr[i])):
                        if(self.kb.tile_arr[i][j].is_mined is ID.hidden):
                            candidates.append(self.kb.tile_arr[i][j])
                if len(candidates) == 0:
                    self.gameover = True
                    self.won = True
                    break
                print("guess -surroundded by mines")
                rand_index = random.randint(0, len(candidates) - 1)
                chosen = candidates[rand_index]
                clear_tiles.add(chosen)

        if self.won:
            print("WINNER WINNER CHICKEN DINNER")
        else:
            print("GAMEOVER")
        self.kb.drawGrid()
        return

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

    def test_knowledgebase(self, x, y):
        test_kb = deepcopy(self.kb)
        cur_tile = test_kb.tile_arr[x][y]
        # Returns a predicate on if the arg tile is mined
        if cur_tile.is_mined is not ID.hidden:
            # Error no need to do PBC on an already known tile
            return

        # Add p to KB and try to satisfy
        test_kb.flagOnTile(cur_tile)
        if test_kb.check_local_grid(cur_tile) > 0:
            P = False
        else:
            #p1 will be true only if check_global_sat is true
            P = test_kb.is_mine_or_clear()

        # Add not p to KB and try to satisfy
        test_kb = deepcopy(self.kb)
        cur_tile = test_kb.tile_arr[x][y]
        cur_tile.is_mined = ID.false;
        notP = test_kb.is_mine_or_clear()


        if P and notP:
            self.kb.drawGrid()
            return ID.hidden
        elif P and not notP:
            self.kb.drawGrid()
            return ID.true
        elif not P and notP:
            self.kb.drawGrid()
            return ID.false


if __name__ == '__main__':

    
    improved_agent = ImprovedAgent()
    improved_agent.startGame()