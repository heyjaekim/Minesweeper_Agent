from GameSetting import GameSetting, KB, ID
from copy import deepcopy
import random
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns

class MineSweeperAgent:

    #--------------------------------------------------------
    # define basic self structures for basic agent
    # argument 1 and 2 : size of the dimension, number of the mines in global
    #--------------------------------------------------------
    def __init__(self, dim, num_mines):
        self.dim = dim
        self.kb = KB(dim)
        self.gamesetting = GameSetting(dim, num_mines)
        self.won = True
        self.identified_num = 0
        self.gameover = False
        self.score = 0

    #--------------------------------------------------------
    # start to decide which tile to query
    # guess if there is nothing clear and PBC on every viable option
    # randomly starts at the square of the board and keep iterating until everything reveals
    #--------------------------------------------------------
    def startGame(self):
        
        unvisited_clr_tiles = set()
        fringe = set() # unknown tiles that are adjacent to discovered nodes

        #randomly starts at the cell of the grid
        randX, randY= random.randint(0, self.dim-1), random.randint(0, self.dim-1)
        first_tile = self.checkQuery(randX, randY)

        #Now assign below four var and lists to keep tracking the position of the uncovering cell
        prev_tile = first_tile

        adj_unvisited = self.kb.get_hidden_adj_tiles(first_tile)

        for tile in adj_unvisited:
            fringe.add(tile)
        while self.identified_num < self.dim * self.dim:

            if len(unvisited_clr_tiles) != 0:
                # If there are any safe nodes to go to make those moves
                #print("Clear tiles:" + str(len(unvisited_clr_tiles)))                
                #print("Current state of the knowledge base")
                self.kb.drawGrid()
                print("--------------------------------------")

                tile = unvisited_clr_tiles.pop()
                self.checkQuery(tile.x,tile.y)
                
                if(self.gameover is True):
                    tile.blowup = True
                    #print("BLEW UP THE BOMB")

                adj_unvisited = self.kb.get_hidden_adj_tiles(tile)
                for t in adj_unvisited:
                    fringe.add(t)
                prev_tile = tile

            '''first_tile starts here when the unvis_clr_tileSet is empty'''
            if len(fringe) != 0:
                # Nowhere safe rn to go to so search fringe for safe node
                removing_tiles = []
                for tile in fringe:
                    is_tile_mined = self.verify_knowledgebase(tile.x,tile.y)
                    if is_tile_mined is not ID.hidden:
                        if is_tile_mined is ID.true:
                            self.kb.flagOnTile(tile)
                            #print(tile.coord_str()+ " flagged as mine")
                            #self.kb.drawGrid()

                        elif is_tile_mined is ID.false:
                            tile.is_mined = ID.false
                            unvisited_clr_tiles.add(tile)
                            #print(tile.coord_str()+ " flagged as clear")
                            #self.kb.drawGrid()
                        removing_tiles.append(tile)
                        continue

                for tile in removing_tiles:
                    fringe.remove(tile)

                if len(unvisited_clr_tiles) == 0 and len(fringe) != 0:
                    # Have to guess because we only have hidden tiles left,
                    # no cleared tiles (predicate false or true)
                    #print("guess - nowhere safe to go")
                    guess_tile = fringe.pop()
                    #print("guessing: "+str(guess_tile.x)+','+str(guess_tile.y))
                    unvisited_clr_tiles.add(guess_tile)


            elif len(unvisited_clr_tiles) == 0:

                candidates = []
                for i in range(len(self.kb.tile_arr)):
                    for j in range(len(self.kb.tile_arr[i])):
                        if(self.kb.tile_arr[i][j].is_mined is ID.hidden):
                            candidates.append(self.kb.tile_arr[i][j])
                if len(candidates) == 0:
                    #self.gameover = True
                    #self.won = True
                    break
                #print("guess -surroundded by mines")
                rand_index = random.randint(0, len(candidates) - 1)
                chosen = candidates[rand_index]
                unvisited_clr_tiles.add(chosen)

        if self.won:
            print("WINNER WINNER CHICKEN DINNER")
        else:
            print("AGENT BLEW UP THE BOMB")
        return self.score

    #--------------------------------------------------------
    # argument 1: assigned number in the square
    # argument 2: current square that we are exploring
    #--------------------------------------------------------
    def checkNum(self, num, cur_tile):
        if num == 9:
            #print("Blew up at x = " + str(cur_tile.x))
            #print("Blew up at y = " + str(cur_tile.y))
            self.won = False
            self.gameover = True
            self.score += 1
            return
        elif num >= 0 and num <= 8:
            self.kb.visitCurrentTile(cur_tile, num)
        else:
            # Error invalid num
            return
    
    #--------------------------------------------------------
    # returns 0-8 for num of adj mines or 0 if the tile is mined
    # argument: x and y coordinate
    #--------------------------------------------------------
    def checkQuery(self, x, y):
        num = int(self.gamesetting.grid[x][y])
        cur_tile = self.kb.tile_arr[x][y]
        self.checkNum(num, cur_tile)
        self.identified_num += 1
        return cur_tile

    def verify_knowledgebase(self, x, y):
        test_kb = deepcopy(self.kb)
        cur_tile = test_kb.tile_arr[x][y]
        if cur_tile.is_mined is not ID.hidden:
            return

        test_kb.flagOnTile(cur_tile)
        if test_kb.check_local_grid(cur_tile) > 0:
            P = False
        else:
            P = test_kb.is_mine_or_clear()

        # Add not p to KB and try to satisfy
        test_kb = deepcopy(self.kb)
        cur_tile = test_kb.tile_arr[x][y]
        cur_tile.is_mined = ID.false
        notP = test_kb.is_mine_or_clear()


        if P and notP:
            return ID.hidden
        elif P and not notP:
            return ID.true
        elif not P and notP:
            return ID.false

#------------------------------------------------------------------------
#this function will iterate to get a plot
#x-axis is representing for each of mines that is tested, increased by 5
#y-axis is representing for the score rate, ((score / num_games) * 100)
#------------------------------------------------------------------------
def iterateAgent(num_games, num_mines, dim):
    mines = num_mines
    iterations = 5
    score = 0
    avg_score = []
    for t in range(iterations):
        blowup = 0
        for i in range(num_games):
            basic_agent = MineSweeperAgent(dim, mines)
            num_blowup = basic_agent.startGame()
            blowup += num_blowup
            score += ((mines - num_blowup) / mines)

        avg_score.append((score / num_games) * 100)
        mines += 5
        score = 0
        print (t)

    sns.set(style="whitegrid", color_codes=True)
    plt.figure(figsize=(10,5))
    x = np.arange(10, mines, 5)

    plt.bar(x , avg_score, width=0.8)
    plt.xlabel("# OF THE MINE")
    plt.ylabel("AVG SCORE PERCENTAGE (%)")
    plt.title("AVG SCORE DISTRIBUTION PLOT FOR IMPROVED AGENT")
    plt.xticks(x)

    plt.show()


if __name__ == '__main__':
    score = 0
    blowup = 0
    num_mines = 20
    num_games = 5
    dim = 10

    agent = MineSweeperAgent(dim, num_mines)
    num_blowup = agent.startGame()
    print("The total # of bombs blew up is : " + str(num_blowup))
    print("The score rate is " + str((num_mines-num_blowup)/num_mines * 100) + "%.")

    # here is the code lines for rendering the plot data for basic agent.
    # I encourage to iterate under number of 30 mines.
    """ 
    for i in range(num_games):
        agent = MineSweeperAgent(dim, num_mines)
        num_blowup = agent.startGame()
        blowup += num_blowup
        score += ((num_mines - num_blowup) / num_mines)
    iterateAgent(num_games, num_mines, dim)
    """
