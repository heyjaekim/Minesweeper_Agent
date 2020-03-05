import sys
import random
import pygame  # imports the package with all available pygame modules

# initialize each of modules imported above
pygame.init()

# colors to be used
BLACK = 0, 0, 0
GREY = 127, 127, 127
RED = 255, 0, 0
ORANGE = 255, 127, 0
YELLOW = 255, 255, 0
WHITE = 255, 255, 255
GREEN = 0, 255,0

# Graphical window constants
WIDTH = 500
HEIGHT = 500

# size of graphical window
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

# Graphical window caption
pygame.display.set_caption('Minesweeper')

# loop flag
DONE = False

# create a Clock object to help track time
clock = pygame.time.Clock()

# create a Font object
font = pygame.font.Font("COMICATE.ttf", 20)

# mouse variables
mouse_Status = 0
mouse_x = 0
mouse_y = 0

# grid variables
cColumns = 0
cRows = 0
cMines = 0

# game status
game_Status = -1

# constants for game
ROWS = COLUMNS = 10
MINES = 15

class Button(object):
    def __init__(self):
        self.textBoxes = {}

    def mousePress(self,x,y,width,height):
        global mouse_Status, mouse_x, mouse_y
        if mouse_Status == 1 and mouse_x >= x and mouse_x <= (x + width) and mouse_y >= y and mouse_y <= (y + height):
            return True

    def mouseRelease(self, x, y, width, height):
        global mouse_Status, mouse_x, mouse_y
        if mouse_Status == 1 and mouse_x < x or mouse_Status == 1 and x > (
            x + width) or mouse_Status == 1 and mouse_y < y or mouse_Status == 1 and mouse_y > (y + height):
            return True

    def hovering(self, x, y, width, height):
        global mouse_Status, mouse_x, mouse_y
        if mouse_Status == 0 and mouse_x >= x and mouse_x <= (x + width) and mouse_y >= y and mouse_y <= (y + height):
            return True

    def buttonPress(self,x,y,width,height,normalColor,hoverColor,textFont,text,textColor,statusHolding=False,
                    statusVar=0, status=1):
        if not self.mousePress(x, y, width, height) and not self.hovering(x, y, width, height):
            pygame.draw.rect(screen, normalColor, (x, y, width, height))
        elif self.hovering(x, y, width, height):
            pygame.draw.rect(screen, hoverColor, (x, y, width, height))
        if statusHolding == True and statusVar == status:
            pygame.draw.rect(screen, hoverColor, (x, y, width, height))

        buttonText = textFont.render(text, True, textColor)
        buttonText_x = buttonText.get_rect().width
        buttonText_y = buttonText.get_rect().height
        screen.blit(buttonText, (((x + (width / 2)) - (buttonText_x / 2)), ((y + (height / 2)) - (buttonText_y / 2))))
        if self.mousePress(x, y, width, height):
            return True


button = Button()


def infoBar():
    global game_Status
    pygame.draw.rect(screen,GREY,(0,0,500,100))
    pygame.draw.line(screen,BLACK,(0,100),(500,100),4)

    if game_Status == 0:
        text = font.render("Mines: " + str(game.total_mines),True,BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((150 - (text_x / 2)), (50 - (text_y / 2))))
        text = font.render("Flags: " + str(game.num_flagged),True,BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((350 - (text_x / 2)), (50 - (text_y / 2))))
    elif game_Status == 1:  # Winner
        text = font.render("Completed", True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((150 - (text_x / 2)), (50 - (text_y / 2))))
    elif game_Status == 2:  # Hit a mine
        text = font.render("Hit a Mine", True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text,((150 - (text_x / 2)),(50 - (text_y / 2))))

    if game_Status == 1 or game_Status == 2:
        if button.buttonPress(325, 25, 150, 50, RED, ORANGE, font, "RESET", BLACK):
            game_Status = 0
            game.reset(ROWS,COLUMNS,MINES)


def menu():
    global game_Status
    screen.fill(WHITE)
    text = font.render("Mine Sweeper",True,BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((250-(text_x / 2)),(100-(text_y / 2))))

    if button.buttonPress(200,250,100,50,RED,ORANGE,font,"BEGIN",BLACK):
        game_Status = 2

#working on fix for this
"""def custom():
    global cColumns, cRows, cMines, game_Status
    text = font.render("Columns: " + str(cColumns),True,BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((225 - (text_x / 2)), (180 - (text_y / 2))))
    if button.buttonPress(300, 160, 20, 20, RED, ORANGE, font, " /\ ", BLACK):
        if cColumns < 20:
            cColumns += 1
    if button.buttonPress(300, 180, 20, 20, RED, ORANGE, font, " \/ ", BLACK):
        if cColumns > 0:
            cColumns -= 1
    text = font.render("Rows: ", + str(cRows),True,BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((230 - (text_x / 2)), (260 - (text_y / 2))))
    if button.buttonPress(300, 240, 20, 20, RED, ORANGE, font, " /\ ", BLACK):
        if cRows < 20:
            cRows += 1
    if button.buttonPress(300, 260, 20, 20, RED, ORANGE, font, " \/ ", BLACK):
        if cRows > 0:
            cRows -= 1
    text = font.render("Mines: " + str(cMines),True,BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, ((230 - (text_x / 2)), (340 - (text_y / 2))))
    if button.buttonPress(300, 320, 20, 20, RED, ORANGE, font, " /\ ", BLACK):
        if cMines < 50 and cMines < (cColumns * cRows):
            cMines += 1
    if button.buttonPress(300, 340, 20, 20, RED, ORANGE, font, " \/ ", BLACK):
        if cMines > 0:
            cMines -= 1
    if button.buttonPress(300, 390, 100, 60, RED, ORANGE,font,"Start",BLACK):
        game.reset(cColumns, cRows, cMines)
        game_Status = 0
"""

class Tile(object):
    def __init__(self, x, y, columns, rows):
        self.columns = columns
        self.rows = rows
        self.x = (x * (size[0] / self.columns))
        self.y = (y * ((size[1] - 100) / self.rows)) + 100
        self.mine = False
        self.neighbors = 0
        self.visible = False
        self.flag = False

    def update(self):
        global game_Status
        if game_Status == 0:
            if mouse_Status == 1 and mouse_x >= self.x and mouse_x <= (self.x + (size[0]/self.columns)) and mouse_y >= self.y and mouse_y <= (self.y +((size[1]-100)/self.rows)):
                self.visible = True
                self.flag = False
            if mouse_Status == 3 and mouse_x >= self.x and mouse_x <= (self.x + (size[0]/self.columns)) and mouse_y >= self.y and mouse_y <= (self.y + ((size[1]-100)/self.rows)):
                if self.flag == False:
                    self.flag = True
                elif self.flag == True:
                    self.flag = False
                if self.visible == True and self.mine == True:
                    game_Status = 2

    def show(self):
        if self.flag == True:
            pygame.draw.rect(screen,YELLOW,(self.x, self.y,(size[0]/self.columns),((size[1]-100)/self.rows)))
        if self.visible == True:
            if self.mine == False:
                pygame.draw.rect(screen,GREY,(self.x, self.y, (size[0] / self.columns), ((size[1] - 100) / self.rows)))
                if self.neighbors > 0:
                    text = font.render(str(self.neighbors),True,BLACK)
                    text_x = text.get_rect().width
                    text_y = text.get_rect().height
                    screen.blit(text, ((self.x + ((size[0] / self.columns) / 2) - (text_x / 2)),
                                       (self.y + (((size[1] - 100) / self.rows) / 2) - (text_y / 2))))

            elif self.mine == True:
                pygame.draw.rect(screen,RED,(self.x, self.y, (size[0] / self.columns), ((size[1] - 100) / self.rows)))
        pygame.draw.rect(screen,BLACK,(self.x, self.y,(size[0] / self.columns),((size[1] - 100) / self.rows)), 2)


class Game(object):
    def __init__(self, columns, rows, mines):
        self.columns = columns
        self.rows = rows
        self.total_mines = mines
        self.board = []
        self.mines = []
        self.mine_num = len(self.mines)
        self.neighbnum = 0
        self.num_flagged = 0
        self.numvis = 0
        self.foundMines = 0

        # creating board
        for y in range(self.rows):
            self.board.append([])
            for x in range(self.columns):
                self.board[y].append(Tile(x,y,self.columns,self.rows))

        # placing mines
        while self.mine_num < self.total_mines:
            self.mineloc = [random.randrange(self.columns), random.randrange(self.rows)]
            if self.board[self.mineloc[1]][self.mineloc[0]].mine == False:
                self.mines.append(self.mineloc)
                self.board[self.mineloc[1]][self.mineloc[0]].mine = True
            self.mine_num = len(self.mines)

        # neighbors
        for y in range(self.rows):
            for x in range(self.columns):
                self.neighbnum = 0
                if y > 0 and x > 0:
                    if self.board[y - 1][x - 1].mine == True:
                        self.neighbnum += 1
                if y > 0:
                    if self.board[y - 1][x].mine == True:
                        self.neighbnum += 1
                if y > 0 and x < (self.columns - 1):
                    if self.board[y - 1][x + 1].mine == True:
                        self.neighbnum += 1
                if x > 0:
                    if self.board[y][x - 1].mine == True:
                        self.neighbnum += 1
                if x < (self.columns - 1):
                    if self.board[y][x + 1].mine == True:
                        self.neighbnum += 1
                if x > 0 and y < (self.rows - 1):
                    if self.board[y + 1][x - 1].mine == True:
                        self.neighbnum += 1
                if y < (self.rows - 1):
                    if self.board[y + 1][x].mine == True:
                        self.neighbnum += 1
                if x < (self.columns - 1) and y < (self.rows - 1):
                    if self.board[y + 1][x + 1].mine == True:
                        self.neighbnum += 1
                self.board[y][x].neighbors = self.neighbnum

    def update(self):
        global game_Status
        self.num_flagged = 0
        self.numvis = 0
        self.foundMines = 0
        for y in range(self.rows):
            for x in range(self.columns):
                self.board[x][y].update()
                if self.board[y][x] == 0 and self.board[y][x].visible == True:
                    if y > 0 and x > 0:
                        self.board[y - 1][x - 1].visible = True
                    if y > 0:
                        self.board[y - 1][x].visible = True
                    if y > 0 and x < (self.columns - 1):
                        self.board[y - 1][x + 1].visible = True
                    if x > 0:
                        self.board[y][x - 1].visible = True
                    if x < (self.columns - 1):
                        self.board[y][x + 1].visible = True
                    if x > 0 and y < (self.rows - 1):
                        self.board[y + 1][x - 1].visible = True
                    if y < (self.rows - 1):
                        self.board[y + 1][x].visible = True
                    if x < (self.columns - 1) and y < (self.rows - 1):
                        self.board[y + 1][x + 1].visible = True
                if self.board[y][x].flag == True:
                    self.num_flagged += 1
                if self.board[y][x].visible == True:
                    self.numvis += 1
            for mine in self.mines:
                if self.board[mine[1]][mine[0]].flag == True:
                    self.foundMines += 1
                if self.num_flagged == self.total_mines and self.foundMines == self.total_mines and self.numvis == (
                    (self.columns * self.rows) - self.total_mines):
                    game_Status = 1
                if game_Status == 1 or game_Status == 2:
                    for y in range(self.rows):
                        for x in range(self.columns):
                            self.board[y][x].visible = True

    def render(self):
        for y in range(self.rows):
            for x in range(self.columns):
                self.board[y][x].show()

    def reset(self, columns, rows, mines):
        if columns != 0 and rows != 0 and mines != 0:
            self.columns = columns
            self.rows = rows
            self.total_mines = mines
        self.board = []
        self.mines = []
        self.mine_num = len(self.mines)
        self.neighbnum = 0
        self.num_flagged = 0
        self.numvis = 0
        self.foundMines = 0

        # creating board
        for y in range(self.rows):
            self.board.append([])
            for x in range(self.columns):
                self.board[y].append(Tile(x,y,self.columns,self.rows))

        # placing mines
        while self.mine_num < self.total_mines:
            self.mineloc = [random.randrange(self.columns), random.randrange(self.rows)]
            if self.board[self.mineloc[1]][self.mineloc[0]].mine == False:
                self.mines.append(self.mineloc)
                self.board[self.mineloc[1]][self.mineloc[0]].mine = True
            self.mine_num = len(self.mines)

        # neighbors
        for y in range(self.rows):
            for x in range(self.columns):
                self.neighbnum = 0
                if y > 0 and x > 0:
                    if self.board[y - 1][x - 1].mine == True:
                        self.neighbnum += 1
                if y > 0:
                    if self.board[y - 1][x].mine == True:
                        self.neighbnum += 1
                if y > 0 and x < (self.columns - 1):
                    if self.board[y - 1][x + 1].mine == True:
                        self.neighbnum += 1
                if x > 0:
                    if self.board[y][x - 1].mine == True:
                        self.neighbnum += 1
                if x < (self.columns - 1):
                    if self.board[y][x + 1].mine == True:
                        self.neighbnum += 1
                if x > 0 and y < (self.rows - 1):
                    if self.board[y + 1][x - 1].mine == True:
                        self.neighbnum += 1
                if y < (self.rows - 1):
                    if self.board[y + 1][x].mine == True:
                        self.neighbnum += 1
                if x < (self.columns - 1) and y < (self.rows - 1):
                    if self.board[y + 1][x + 1].mine == True:
                        self.neighbnum += 1
                self.board[y][x].neighbors = self.neighbnum


game = Game(ROWS,COLUMNS,MINES)

# loop for running window
while DONE is not (True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_Status = event.button
            pygame.mouse.set_pos(mouse_x, mouse_y + 1)
        else:
            mouse_Status = 0

    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]

    screen.fill(WHITE)

    if game_Status == - 1:
        menu()
    elif game_Status == -2:
        custom()
    elif game_Status >= 0 and game_Status <= 2:
        infoBar()

        game.update()
        game.render()

        pygame.display.flip()

        clock.tick(60)
pygame.quit()
