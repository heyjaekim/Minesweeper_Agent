from enum import Enum
import numpy as np
import queue as Q
from ImprovedGamesetting import *
from copy import deepcopy
from itertools import combinations
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns

class ImprovedAgent(object):

    #--------------------------------------------------------
    # define basic self structures for improved agent agent
    # argument: game environment from improvedGameSetting.py
    #--------------------------------------------------------
    def __init__(self, env, imp = 0):
        self.env = env
        self.dim = self.env.dim
        self.board = [[9 for x in range(self.dim)] for y in range(self.dim)]
        self.cell_to_inference = Q.Queue()
        self.cell_unresolved = Q.Queue()
        self.identified_num = 0
        self.finished_num = 0
        self.final_hidden_num = []   
        self.final_num_mines = []      
        self.score = 0
        self.imp = imp #0 for improved agent, 1 for letting agent to know total mine num
        self.isHypothesis = False

    #--------------------------------------------------------
    # check if the exploring square is valid tile
    #--------------------------------------------------------
    def isValid(self, x, y):
        if(0 <= x < self.dim) and (0 <= y < self.dim):
            return True
        else:
            return False

    #--------------------------------------------------------
    # start inferencing here, and going into random query process first
    # it will unreveal the square with multiple clues at a time
    #--------------------------------------------------------
    def gameStart(self):
        score = 0
        #else is when we are solving the mineweeper with improved agent.
        while self.identified_num < self.dim * self.dim:
            score = self.inference_start()
            
        return score

    def inference_start(self):
        inf_state = 0

        if self.identified_num < self.dim * self.dim:
            while self.cell_to_inference.qsize():
                (x,y) = self.cell_to_inference.get()
                baseline_return = self.baseline_inference(x,y)
                if baseline_return == -1:
                    pass

                elif baseline_return:
                    inf_state = 1
                    break
                else:
                    self.cell_unresolved.put((x,y))

            if inf_state == 0:
                if self.computation_inference() == 1:
                    while self.cell_unresolved.qsize():
                        self.cell_to_inference.put(self.cell_unresolved.get())
                    inf_state = 1
            
            if inf_state == 0 and self.imp == 1 and (self.count_global_mines() / self.env.num_mines ) < 0.2:
                while self.cell_unresolved.qsize():
                    (x, y) = self.cell_unresolved.get()
                    if self.number_inference(x, y):
                        inf_state = 1

            if inf_state == 0:
                self.processProbQuery() #from random to select the lowest probability of the squres
                while self.cell_unresolved.qsize(): 
                    self.cell_to_inference.put(self.cell_unresolved.get())
                pass

        else:
            return -1

        return self.score

    #--------------------------------------------------------
    # """process baseline inference from the cell_to_inference square tiles that have found
    # , and we update the board and queue """
    #--------------------------------------------------------
    def baseline_inference(self, x, y):
        if self.board[x][y] == -2:     
            return
        num_mines = self.board[x][y]
        identified_mines, clear_tiles, hidden_num, adj_tiles = self.get_adj_tiles_info(x, y)

        if hidden_num == 0: 
            return -1
        elif num_mines - identified_mines == hidden_num:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if self.isValid(x+i, y+j) and self.board[x + i][y + j] == 9:
                        self.board[x + i][y + j] = -1
                        self.env.mark_mine((x+i, y+j))
                        self.score += 1
                        while self.cell_unresolved.qsize():
                            self.cell_to_inference.put(self.cell_unresolved.get())
                        self.identified_num += 1
            return True
        elif (adj_tiles - num_mines) - clear_tiles == hidden_num:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    
                    if self.isValid(x+i, y+j) and self.board[x + i][y + j] == 9:
                        
                        if self.isHypothesis:
                            self.board[x + i][y + j] = -2
                            pass
                        else:
                            self.board[x + i][y + j] = self.env.processQuery(x + i, y + j, True)
                            self.cell_to_inference.put((x + i, y + j))
                            while self.cell_unresolved.qsize():
                                self.cell_to_inference.put(self.cell_unresolved.get())
                        self.identified_num += 1
            return True
        else:
            return False

    #--------------------------------------------------------
    # """compute each inference that is found from the baseline inference and random query process
    # define each inference is mutually influencing and is valid enough to explore"""
    #--------------------------------------------------------
    def computation_inference(self):
        computed_dic = {}
        tempQ = Q.Queue()

        while self.cell_unresolved.qsize():
            (x, y) = self.cell_unresolved.get()
            tempQ.put((x, y))
            num_mines_revealed = 0
            hidden_tiles = []
            
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if self.isValid(x+i, y+j) and (i != 0 or j != 0):
                        if self.board[x + i][y + j] == -1:
                            num_mines_revealed += 1
                        elif self.board[x + i][y + j] == 9:
                            hidden_tiles.append((x + i, y + j))
            num_adj_tiles = self.board[x][y] - num_mines_revealed
            computed_dic[(x, y)] = (hidden_tiles, num_adj_tiles)  #left hidden squares, right num adj squares
        
        while tempQ.qsize():
            self.cell_unresolved.put(tempQ.get())
        
        cleared_sqrs = []
        flagged_sqrs = []
        equation_keylist = list(computed_dic.keys())
        
        if len(equation_keylist) >= 2:
            #여기서부터는 equation_keylist안에 key값이 2개 이상일때 있을때, 
            for i in range(len(equation_keylist) - 1):
                
                for j in range(i + 1, len(equation_keylist)):
                    (aim_x, aim_y) = equation_keylist[i]
                    (mutual_x, mutual_y) = equation_keylist[j]
                    
                    #We need to confirm if aim_x and mutual_x are mutually influencing
                    #To do that, we need to compute absolute value for (mutual_x - aim_x) which is less than 3. 
                    #Checking the differnece is less than 3 is meaning that mutual_x and aim_x are close enough from 3x3 dimension.
                    if abs(mutual_x - aim_x) < 3 and abs(mutual_y - aim_y) < 3:   # for all cell pairs having mutual influence
                        (temp_hidden_sqrs, temp_adj_num) = deepcopy(computed_dic[(aim_x, aim_y)])
                        (temp_hidden_sqrs2, temp_adj_num2) = deepcopy(computed_dic[(mutual_x, mutual_y)])
                        remove_list = []
                        
                        for point in temp_hidden_sqrs:   # remove same neighbors
                            if point in temp_hidden_sqrs2:
                                remove_list.append(point)
                        
                        for point in remove_list:
                            temp_hidden_sqrs.remove(point)
                            temp_hidden_sqrs2.remove(point)
                        
                        (temp_adj_num, temp_adj_num2, 
                        temp_hidden_sqrs, temp_hidden_sqrs2, 
                        cleared_sqrs, flagged_sqrs) = self.safety_computation(temp_adj_num, temp_adj_num2, 
                                                        flagged_sqrs, temp_hidden_sqrs, temp_hidden_sqrs2, cleared_sqrs)
       
        cleared_sqrs = list(set(cleared_sqrs))
        flagged_sqrs = list(set(flagged_sqrs))
        
        if len(cleared_sqrs) != 0 or len(flagged_sqrs) != 0:
       
            for nodes in cleared_sqrs:
                (x, y) = nodes
                if self.isHypothesis:
                    self.board[x][y] = -2
                    pass
                else:
                    self.board[x][y] = self.env.processQuery(x, y, False)
                    self.cell_unresolved.put(nodes)
                self.identified_num += 1
    
            for nodes in flagged_sqrs:
                (x, y) = nodes
                self.board[x][y] = -1
                self.env.mark_mine((x, y))
                self.identified_num += 1
                self.score += 1
     
            return 1
    
        return -1

    def safety_computation(self, adj_tiles, adj_tiles2, mines, hiddenTiles, hiddenTiles2, clears):

        if adj_tiles2 > adj_tiles:
            if len(hiddenTiles2) == adj_tiles2 - adj_tiles:    
                for item in hiddenTiles2:                             
                    mines.append(item)
                for item in hiddenTiles:
                    clears.append(item)
            if len(hiddenTiles) == adj_tiles2 - adj_tiles == 0:   
                for item in hiddenTiles2:
                    clears.append(item)
        
        else: # adj_tiles2 <= adj_tiles:
            if len(hiddenTiles) == adj_tiles - adj_tiles2:
                for item in hiddenTiles:
                    mines.append(item)
                for item in hiddenTiles2:
                    clears.append(item)
            if len(hiddenTiles2) == adj_tiles - adj_tiles2 == 0:
                for item in hiddenTiles:
                    clears.append(item)

        return adj_tiles, adj_tiles2, hiddenTiles, hiddenTiles2, clears, mines


    def get_adj_tiles_info(self, x, y):
        identified_mines = 0
        clear_tiles = 0
        hidden_num = 0
        adj_tiles = 8
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.isValid(x+i, y+j) and (i != 0 or j != 0):
                    if self.board[x + i][y + j] == -1:
                        identified_mines += 1
                    elif self.board[x + i][y + j] == 9:
                        hidden_num += 1
                    else:
                        clear_tiles += 1
                elif not self.isValid(x+i, y+j):
                    adj_tiles -= 1
        return identified_mines, clear_tiles, hidden_num, adj_tiles

    #--------------------------------------------------------
    # """Compute the lowest probability and then agent will choose the lowest probability square 
    # as it considered as the most safe to uncover"""
    #--------------------------------------------------------
    def probability_inference(self, x, y):
        min_p = 1
        (aim_x, aim_y) = (0, 0)
        for i in range(-1, 2):
            for j in range(-1, 2):
                (neighbor_x, neighbor_y) = (x+i, y+j)
                if (self.isValid(neighbor_x, neighbor_y) 
                    and self.board[neighbor_x][neighbor_y] == 9 
                    and (i != 0 or j != 0)):
                    p = 0
                    cnt = 0
                    
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            (adj_x, adj_y) = (neighbor_x + k, neighbor_y + l)
                            
                            if (self.isValid(adj_x, adj_y) 
                                and 0 <= self.board[adj_x][adj_y] < 9 
                                and (k != 0 or l != 0)):
                                
                                if self.board[adj_x][adj_y] == 0:
                                    return adj_x, adj_y
                                reveal_num_mines = 0
                                hidden_num = 0
                                
                                for n in range(-1, 2):
                                    for m in range(-1, 2):
                                        (ins_x, ins_y) = (adj_x + n, adj_y + m)
                                        if self.isValid(ins_x, ins_y) and (n != 0 or m != 0):
                                            if self.board[ins_x][ins_y] == -1:
                                                reveal_num_mines += 1
                                            elif self.board[ins_x][ins_y] == 9:
                                                hidden_num += 1
                                tmp_p = (self.board[adj_x][adj_y] - reveal_num_mines) / hidden_num
                                if tmp_p == 1:
                                    p = 1
                                else:
                                    p += tmp_p
                                    cnt += 1
                    if cnt != 0 and p / cnt <= min_p: #p <= min_p: #p / cnt <= min_p:
                        min_p = p / cnt
                        #mine_p = p
                        (aim_x, aim_y) = (neighbor_x, neighbor_y)
        if (aim_x, aim_y) != (0, 0):
            return aim_x, aim_y
        else:
            return -1, -1

    def count_global_mines(self):
        count = 0
        for i in range(self.dim):
            for j in range(self.dim):
                if self.board[i][j] == -1:
                    count += 1
        return count

    def count_global_hidden(self):
        count = 0
        for i in range(self.dim):
            for j in range(self.dim):
                if self.board[i][j] == 9:
                    count += 1
        return count

    #------------------------------------------------
    # Inference for number of mines given to the agent
    # Also keep update how many mines are left
    #------------------------------------------------
    def number_inference(self, x, y):
        solutions = []  # only for the first layer
        hidden_cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.isValid(x + i, y + j) and self.board[x + i][y + j] == 9:
                    hidden_cells.append((x + i, y + j))

        # all combinations(stored in tuple format) to be set as mines            
        mine_combs = combinations(hidden_cells, self.board[x][y]) 

        for tup in mine_combs:
            
            agent_deepcopy = ImprovedAgent(self.env)
            agent_deepcopy.board = deepcopy(self.board)
            agent_deepcopy.score = deepcopy(self.score)
            
            for i in self.cell_to_inference.queue:
                agent_deepcopy.cell_to_inference.put(i)
            for j in self.cell_unresolved.queue:
                agent_deepcopy.cell_unresolved.put(j)
            
            agent_deepcopy.improvement = deepcopy(self.imp)
            agent_deepcopy.identified_num = deepcopy(self.identified_num)
            agent_deepcopy.finished_num = deepcopy(self.finished_num)
            agent_deepcopy.isHypothesis = True
            agent_deepcopy.final_hidden_num = deepcopy(self.final_hidden_num)
            agent_deepcopy.final_num_mines = deepcopy(self.final_num_mines)
            
            for c1 in tup:
                (x1, y1) = c1
                agent_deepcopy.board[x1][y1] = -1
            for c2 in hidden_cells:
                if c2 not in tup:
                    (x2, y2) = c2
                    agent_deepcopy.board[x2][y2] = -2    # hypothesis as safe
            #agent_deepcopy.hypothetical_inference() # which does not check or say identify safe cells newly added
            
            #if self.isHypothesis:
            if agent_deepcopy.isHypothesis:   
                if agent_deepcopy.cell_unresolved:
                    self.final_hidden_num += agent_deepcopy.final_hidden_num
                    self.final_num_mines += agent_deepcopy.final_num_mines
                
                else:   # agent_branch is on the last layer of branches.
                    self.final_hidden_num.append(agent_deepcopy.count_global_hidden()) 
                    self.final_num_mines.append(agent_deepcopy.count_global_mines())
            
            # the first layer
            else:
                
                for i in range(len(agent_deepcopy.final_num_mines)):
                    if (agent_deepcopy.final_num_mines[i] <= self.env.mine_num 
                            and agent_deepcopy.final_num_mines[i] + agent_deepcopy.final_hidden_num[i] >= self.env.mine_num):
                        solutions.append(tup)
                        break      # turn to next tuple
        
        if not solutions:
            return False
        
        return True

    #---------------------------------------------------------------------------------
    #"""Processing to compute knowledge base based on the numbers of surrounded mines for each square that is revealed."""
    #"""As long as we know the probability for each square, then we """
    #---------------------------------------------------------------------------------
    def processProbQuery(self):
        possible_mines = []
        tempQ = Q.Queue()

        #With the current board information, define identified mines, clear squares, hidden num, valid number of ajc tiles
        while self.cell_unresolved.qsize():
            (x, y) = self.cell_unresolved.get()
            tempQ.put((x, y))
            num_mines = self.board[x][y]
            identified_mines, clear_tiles, hidden_num, adj_tiles = self.get_adj_tiles_info(x, y)
            #stroe the kb inference for the squares near by (x,y) 
            possible_mines.append(((num_mines - identified_mines) / hidden_num, (x, y)))

        possible_mines.sort()
        while tempQ.qsize():
            self.cell_unresolved.put(tempQ.get())

        if len(possible_mines) != 0 :
            mine_p = 1

            if len(possible_mines) > 1:
                (mine_p, (x, y)) = possible_mines[randint(0,len(possible_mines)-1)]
                if mine_p <= ( 1 - (self.count_global_mines() / self.env.num_mines)):
                    #print("process the query nearby")
                    (aim_x, aim_y) = self.probability_inference(x, y)
                    self.identify_tile(aim_x, aim_y)
                    return True

            elif len(possible_mines) == 1:
                (mine_p, (x, y)) = possible_mines[0]
                if mine_p <= ( 1 - (self.count_global_mines() / self.env.num_mines)):
                    #print("process the query nearby")
                    (aim_x, aim_y) = self.probability_inference(x, y)
                    self.identify_tile(aim_x, aim_y)
                    return True

        self.random_outside()


    def random_outside(self):
        covered_tiles = []
        for x in range(self.dim):
            for y in range(self.dim):
                if self.board[x][y] == 9:
                    covered_tiles.append((x,y))
        if len(covered_tiles) == 0:
            return False
        k = random.randint(0, len(covered_tiles) - 1)
        (x, y) = covered_tiles[k]
        self.identify_tile(x,y)
        #print("random outside")


    def identify_tile(self, aim_x, aim_y):
        if self.env.processQuery(aim_x, aim_y, False) is False:
                    self.board[aim_x][aim_y] = -1
                    self.identified_num += 1
        else:
            self.board[aim_x][aim_y] = self.env.processQuery(aim_x, aim_y, False)
            self.cell_to_inference.put((aim_x, aim_y))
            self.identified_num += 1

def iterateImpAgent(num_games, num_mines, dim):
    mines = num_mines
    iterations = 19
    score = 0
    avg_score = []
    for t in range(iterations):
        for i in range(num_games):
            rendered_grid = ImprovedSetting(dim, mines)
            imp_agent = ImprovedAgent(rendered_grid)
            score += (imp_agent.gameStart() / mines)
        
        avg_score.append((score / num_games) * 100)
        mines += 5
        score = 0
    
    sns.set(style="whitegrid", color_codes=True)
    plt.figure(figsize=(10,5))
    x = np.arange(10, mines, 5)

    plt.bar(x , avg_score, width=0.8)
    plt.xlabel("# OF THE MINE (MINE DENSITY)")
    plt.ylabel("AVG SCORE PERCENTAGE (%)")
    plt.title("IMPROVED AGENT MINE DENSITY WITH AVG SCORE PERCENTAGE")
    plt.xticks(x)
    
    plt.show()

def iterateForComparison(num_games, num_mines, dim):
    mines = num_mines
    iterations = 19
    score = 0
    score2 = 0
    avg_score = []
    avg_score2 = []
    for t in range(iterations):
        for i in range(num_games):

            rendered_grid = ImprovedSetting(dim, mines)
            imp_agent = ImprovedAgent(rendered_grid)
            score += (imp_agent.gameStart() / mines)

            rendered_grid2 = ImprovedSetting(dim, mines)
            imp_agent2 = ImprovedAgent(rendered_grid2,1)
            score2 += (imp_agent2.gameStart() / mines)
        
        avg_score.append((score / num_games) * 100)
        avg_score2.append((score2 / num_games) * 100)
        mines += 5
        score = 0
        score2 = 0
    
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    x = np.arange(10, mines, 5)
    width = 1.0

    first_plot = ax.bar(x, avg_score, width, color = 'r')
    second_plot = ax.bar(x + width, avg_score2, width, color = 'g')

    ax.set_xlabel("# OF THE MINE (MINE DENSITY)")
    ax.set_ylabel("AVG SCORE PERCENTAGE (%)")
    plt.title("Plot Comparison btw Improved Agent and Agent with Num of Mines Given")
    plt.xticks(x)
    ax.legend( (first_plot[0], second_plot[0]), ('Improved Agent', 'Agent with num of mines given'))
    
    plt.show()

    #sns.set(style="whitegrid", color_codes=True)
    #plt.figure(figsize=(10,5))
    #plt.bar(x, avg_score, avg_score, width=0.5)

    #plt.xlabel("# OF THE MINE (MINE DENSITY)")
    #plt.ylabel("AVG COST PERCENTAGE (%)")
    #plt.title("MINIMIZING COST DISTRIBUTION PLOT FOR SLIGHTLY IMPROVED AGENT")
    #plt.xticks(x)
    
    #plt.show()

"""Please modify four arguments for score, num_mines, num_games, size as you want"""
if __name__ == "__main__":
    score = 0
    num_mines = 10
    num_games = 20
    size = 10
    
    for i in range(num_games):
        rendered_grid = ImprovedSetting(size, num_mines)
        imp_agent = ImprovedAgent(rendered_grid)
        score += (imp_agent.gameStart() / num_mines)
    print("The score rate is " + str((score/num_games) * 100) + "%.")
    
    #iterateImpAgent(num_games, num_mines, size)
    iterateForComparison(num_games, num_mines, size)