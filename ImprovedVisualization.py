import tkinter as tk
from ImprovedGamesetting import *
from ImprovedAgent import *

"""This is the visualizatio for slightly improved agent and more improved agent"""
class Visual(tk.Frame):

    def __init__(self, oir_env, ag):
        tk.Frame.__init__(self)
        self.master.title("Minesweeper")
        # self.master.resizable(False, False)
        self.pack(expand=tk.NO, fill=tk.BOTH)
        self.label_matrix = []
        self.env = oir_env
        self.agent = ag
        self.init_step()
        self.identified_num = 0

    """click next function implemented for minesweeper GUI"""
    def click_next(self):
        self.env.nextStep()
        result = self.agent.inference_start()
        for i in range(self.env.dim):
            for j in range(self.env.dim):
                if self.env.hidden_grid[i][j] == 1:
                    cell_value = self.env.grid[i][j]
                    if cell_value == -1:
                        bg_str = "orange"
                    else:
                        bg_str = "white"
                    self.label_matrix[i][j].configure(text=str(cell_value),bg=bg_str)
                elif self.env.hidden_grid[i][j] == -1:
                    self.label_matrix[i][j].configure(text="M",bg="red")
                elif self.env.hidden_grid[i][j] == 2:
                    self.label_matrix[i][j].configure(text="C",bg="green")
        if result != -1:
            print(result)
        else:
            print("WINNER WINNER CHICKEN DINNER")


    def init_step(self):
        frame1 = tk.Frame(bg='black')
        for i in range(self.env.dim):
            label_list = []
            for j in range(self.env.dim):
                label_list.append(tk.Label(frame1, text="?", bg="grey", width=2, height=1, font=('Arial', 15)))
                label_list[j].grid(row=i, column=j, padx=1, pady=1)
            self.label_matrix.append(label_list)
        frame1.pack()
        frame2 = tk.Frame()
        self.next_button = tk.Button(frame2, text = 'next', width = 6, height = 1, command = self.click_next)
        self.next_button.pack()

        frame2.pack()

"""Choose the dimension size: (size, number of mines)"""
if __name__=='__main__':
    rendered_grid = ImprovedSetting(10, 30)
    imp_agent = ImprovedAgent(rendered_grid)
    #imp_agent = ImprovedAgent(rendered_grid,1)
    board = Visual(rendered_grid, imp_agent)
    board.mainloop()
