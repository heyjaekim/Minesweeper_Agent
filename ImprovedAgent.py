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

    def __init__(self, env):
        self.env = env
        self.dim = self.env.dim
        self.board = [[9 for x in range(self.dim)] for y in range(self.dim)]
        self.cell_to_inference = Q.Queue()
        self.cell_unresolved = Q.Queue()
        self.identified_num = 0
        self.finished_num = 0
        self.isHypothesis = False
        self.final_hidden_num = []     # for hypothesis
        self.final_num_mines = []       # for hypothesis
        self.score = 0

    def isValid(self, x, y):
        if(0 <= x < self.dim) and (0 <= y < self.dim):
            return True
        else:
            return False   
    
    def gameStart(self):
        score = 0
        #else is when we are solving the mineweeper with improved agent.
        while self.identified_num < self.dim * self.dim:
            score = self.inference_start()
            '''
            t = ""
            for x in range(self.dim):
                for y in range(self.dim):
                    
                    if self.env.hidden_grid[x][y] == -1:
                        t += "M "
                    elif self.env.hidden_grid[x][y] == 2:
                        t += "C "
                    elif self.env.hidden_grid[x][y] == 1:
                        if self.env.grid[x][y] == -1:
                            t += "B "
                        else:
                            t += str(self.env.grid[x][y])+" "
                    else:
                        t += "X "

                t += "\n"
            print(t + "----------------------")
            '''
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
                    #print("baseline")
                    inf_state = 1
                    break
                else:
                    self.cell_unresolved.put((x,y))
            
            if inf_state == 0:
                if self.equation_inference():
                    #print("equation")
                    while self.cell_unresolved.qsize():
                        self.cell_to_inference.put(self.cell_unresolved.get())
                    inf_state = 1
    
            if inf_state == 0:
                self.checkRandomQuery()
                while self.cell_unresolved.qsize():
                    self.cell_to_inference.put(self.cell_unresolved.get())
                pass
            
        else:
            return -1

        return self.score


    #baseline inference is about to get true or false depending on the completion of the observing tile and its adj tiles
    def baseline_inference(self, x, y):
        if self.board[x][y] == -2:     # hypothetical_inference, cell will not be in any queue
            return
        num_mines = self.board[x][y]
        identified_mines, clear_tiles, hidden_num, adj_tiles = self.get_adj_tiles_info(x, y)
        
        if hidden_num == 0: #when every tiles were uncovered
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
                        else:
                            self.board[x + i][y + j] = self.env.processQuery(x + i, y + j, True)
                            self.cell_to_inference.put((x + i, y + j))
                            while self.cell_unresolved.qsize():
                                self.cell_to_inference.put(self.cell_unresolved.get())
                        self.identified_num += 1
            return True
        else:
            return False


    def equation_inference(self):
        equation_dic = {}
        tempQ = Q.Queue()
        while self.cell_unresolved.qsize():
            (x, y) = self.cell_unresolved.get()
            tempQ.put((x, y))
            reveal_num_mines = 0
            equation_left = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if self.isValid(x+i, y+j) and (i != 0 or j != 0):
                        if self.board[x + i][y + j] == -1:
                            reveal_num_mines += 1
                        elif self.board[x + i][y + j] == 9:
                            equation_left.append((x + i, y + j))
            equation_right = self.board[x][y] - reveal_num_mines
            equation_dic[(x, y)] = (equation_left, equation_right)  # left = hidden_cells, right = num_hidden_mines
        while tempQ.qsize():
            self.cell_unresolved.put(tempQ.get())
        safe_nodes = []
        mine_nodes = []
        equation_keylist = list(equation_dic.keys())
        if len(equation_keylist) > 1:
            for i in range(len(equation_keylist) - 1):
                for j in range(i + 1, len(equation_keylist)):
                    (x1, y1) = equation_keylist[i]
                    (x2, y2) = equation_keylist[j]
                    if abs(x2 - x1) < 3 and abs(y2 - y1) < 3:   # for all cell pairs having mutual influence
                        (equation_left1, equation_right1) = deepcopy(equation_dic[(x1, y1)])
                        (equation_left2, equation_right2) = deepcopy(equation_dic[(x2, y2)])
                        remove_list = []
                        for point in equation_left1:   # remove same neighbors
                            if point in equation_left2:
                                remove_list.append(point)
                        for point in remove_list:
                            equation_left1.remove(point)
                            equation_left2.remove(point)
                        if equation_right2 > equation_right1:
                            if len(equation_left2) == equation_right2 - equation_right1:    # after removing common neighbors, hidden cells of 2 = hidden mines of 2 - 1, 
                                for item in equation_left2:                             #hidden cells of 2 are all mines and hidden cells of 1 are all safe. (A + B) - (B + C) = len(A)
                                    mine_nodes.append(item)
                                for item in equation_left1:
                                    safe_nodes.append(item)
                            if len(equation_left1) == equation_right2 - equation_right1 == 0:   # (A + B) - B = 0
                                for item in equation_left2:
                                    safe_nodes.append(item)
                        if equation_right2 <= equation_right1:
                            if len(equation_left1) == equation_right1 - equation_right2:
                                for item in equation_left1:
                                    mine_nodes.append(item)
                                for item in equation_left2:
                                    safe_nodes.append(item)
                            if len(equation_left2) == equation_right1 - equation_right2 == 0:
                                for item in equation_left1:
                                    safe_nodes.append(item)
        safe_nodes = list(set(safe_nodes))
        mine_nodes = list(set(mine_nodes))
        if len(safe_nodes) != 0 or len(mine_nodes) != 0:
            for nodes in safe_nodes:
                (x, y) = nodes
                if self.isHypothesis:
                    self.board[x][y] = -2
                else:
                    self.board[x][y] = self.env.processQuery(x, y, False)
                    self.cell_unresolved.put(nodes)
                self.identified_num += 1
            for nodes in mine_nodes:
                (x, y) = nodes
                self.board[x][y] = -1
                self.env.mark_mine((x, y))
                self.identified_num += 1
                self.score += 1
            return True
        return False


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

    def probability_inference(self, x, y):
        min_p = 1
        (aim_x, aim_y) = (0, 0)
        for i in range(-1, 2):
            for j in range(-1, 2):
                (neighbor_x, neighbor_y) = (x+i, y+j)
                if self.isValid(neighbor_x, neighbor_y) and self.board[neighbor_x][neighbor_y] == 9 and (i != 0 or j != 0):
                    p = 0
                    cnt = 0
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            (adj_x, adj_y) = (neighbor_x + k, neighbor_y + l)
                            if self.isValid(adj_x, adj_y) and 0 <= self.board[adj_x][adj_y] < 9 and (k != 0 or l != 0):
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
                                    p = 9
                                p += tmp_p
                                cnt += 1
                    if cnt != 0 and p / cnt <= min_p:
                        min_p = p / cnt
                        #(aim_x, aim_y) = (x1, y1)
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


    def checkRandomQuery(self):
        possible_mines = []
        tempQ = Q.Queue()

        while self.cell_unresolved.qsize():
            (x, y) = self.cell_unresolved.get()
            tempQ.put((x, y))
            num_mines = self.board[x][y]
            identified_mines, clear_tiles, hidden_num, adj_tiles = self.get_adj_tiles_info(x, y)
            possible_mines.append(((num_mines - identified_mines) / hidden_num, (x, y)))
        
        possible_mines.sort()
        while tempQ.qsize():
            self.cell_unresolved.put(tempQ.get())

        if len(possible_mines) != 0:
            (mine_p, (x, y)) = possible_mines[0]
            if mine_p <= ( 1 - (self.count_global_mines() / self.env.num_mines)):
                #print("random nearby")
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

def iterateAgent(num_games, num_mines, dim):
    mines = num_mines
    iterations = 8
    score = 0
    avg_score = 0
    for t in range(iterations):
        avg_score = 0
        score = 0
        for i in range(num_games):
            rendered_grid = ImprovedSetting(dim, mines)
            imp_agent = ImprovedAgent(rendered_grid)
            score += (imp_agent.gameStart() / mines)
        
        avg_score = (score / num_games) * 100
        mines += 5
        score = 0
    
    sns.set(style="whitegrid", color_codes=True)
    plt.figure(figsize=(10,5))
    x = np.arange(10, mines)

    sns.lineplot(x,avg_score)
    plt.xlabel("# OF THE MINE")
    plt.ylabel("AVG SCORE PERCENTAGE (%)")
    plt.title("AVG SCORE DISTRIBUTION PLOT FOR IMPROVED AGENT")
    
    plt.show()

if __name__ == "__main__":
    score = 0
    num_mines = 20
    num_games = 10
    size = 10
    
    for i in range(num_games):
        rendered_grid = ImprovedSetting(size, num_mines)
        imp_agent = ImprovedAgent(rendered_grid)
        score += (imp_agent.gameStart() / num_mines)
    print("The score rate is " + str((score/num_games) * 100) + "%.")
    
    iterateAgent(num_games, num_mines, size)
