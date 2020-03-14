import sys
import random
import pygame  # imports the package with all available pygame modules
#from pygame_functions import *

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
BLUE = 0,72,186
AMBER = 255,191,0

# Graphical window constants
WIDTH = 500
HEIGHT = 500

TOP = 0
RIGHT = 0
# size of graphical window
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

# Graphical window caption
pygame.display.set_caption('Minesweeper Environment')

# loop flag
DONE = False

# create a Clock object to help track time
clock = pygame.time.Clock()

# create a Font object
font = pygame.font.Font("Arial", 50)

# mouse variables
mouse_Status = 0
mouse_x = 0
mouse_y = 0

# grid variables
dimension = 0
input_mines = 0

# game status
game_Status = -1

# number of mines hit
print_num_hit = 0
# number of mines flagged
print_num_flagged = 0
# safely identified percentage
print_safely_identified = 0
# constants for game
ROWS = COLUMNS = 5
MINES = 10

class Button(object):
    def __init__(self):
        self.textBoxes = {}

    def mousePress(self,x,y,width,height):
        global mouse_Status, mouse_x, mouse_y
        if mouse_Status == 1 and mouse_x >= x and mouse_x <= (x + width) and mouse_y >= y and mouse_y <= (y + height):
            return True

    def mouseRelease(self,x,y,width,height):
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
        if not self.mousePress(x,y,width,height) and not self.hovering(x,y,width,height):
            pygame.draw.rect(screen,normalColor,(x,y,width,height))
        elif self.hovering(x,y,width,height):
            pygame.draw.rect(screen,hoverColor,(x,y,width,height))
        if statusHolding == True and statusVar == status:
            pygame.draw.rect(screen,hoverColor,(x,y,width,height))

        buttonText = textFont.render(text, True, textColor)
        buttonText_x = buttonText.get_rect().width
        buttonText_y = buttonText.get_rect().height
        screen.blit(buttonText,(((x+(width/2)) - (buttonText_x/2)),((y+(height/2)) - (buttonText_y / 2))))
        if self.mousePress(x,y,width,height):
            return True


button = Button()


def infoBar():
    global game_Status
    pygame.draw.rect(screen,GREY,(TOP,RIGHT,WIDTH,100))
    pygame.draw.line(screen,BLACK,(0,100),(WIDTH,100),4)

    if game_Status == 0:
        text = font.render("MINES: " + str(game.total_mines),True,BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((150 - (text_x / 2)), (50 - (text_y / 2))))
        text = font.render("FLAGS: " + str(game.num_flagged),True,BLACK) #MODIFIED
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((350 - (text_x / 2)), (50 - (text_y / 2))))
    elif game_Status == 1:
        text = font.render("Completed!: ", True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((150 - (text_x / 2)), (25 - (text_y / 2))))
        text = font.render("Number of Mines hit: " + str(print_num_hit), True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((150 - (text_x / 2)), (50 - (text_y / 2))))
        text = font.render("Number of Mines Flagged: " + str(print_num_flagged), True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((150 - (text_x / 2)), (75 - (text_y / 2))))

    if game_Status == 1:
        if button.buttonPress((WIDTH/2)+120, 25, 150, 50, BLUE, AMBER, font, "RESET", BLACK):
            game_Status = -1
            game.reset(0,0,0)

def resultBar():
    global game_Status
    pygame.draw.rect(screen, GREY, (TOP,RIGHT+WIDTH-50,WIDTH,100))
    pygame.draw.line(screen, BLACK, (0,HEIGHT-50), (WIDTH,HEIGHT-50), 4)

    if game_Status == 1:
        text = font.render("Safely Identified: " + str(print_safely_identified), True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, (((WIDTH/2 - (text_x / 2))), (HEIGHT - (text_y / 2))-25))


def menu():
    global game_Status
    screen.fill(GREY)
    text = font.render("Mine Sweeper",True,BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, (((WIDTH/2)-(text_x / 2)),(((HEIGHT-50)/2) -(text_y / 2))))

    if button.buttonPress(((WIDTH/2)-50),((HEIGHT/2)),100,50,BLUE,AMBER,font,"BEGIN",BLACK):
        game_Status = -2

#working on fix for this
def userInput():
    global dimension,input_mines,game_Status
    screen.fill(GREY)
    text = font.render("Dimension: " + str(dimension),True,BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, (((WIDTH/2)-(text_x/2)), (HEIGHT/2-125) - (text_y / 2)))
    if button.buttonPress(((WIDTH/2+100)),((HEIGHT/2)-150),20,20,BLUE,AMBER,font,"U", BLACK):
        if dimension < 10000:
            dimension += 1
    if button.buttonPress(((WIDTH/2)+100),((HEIGHT/2)-115),20,20,BLUE,AMBER,font,"D",BLACK):
        if dimension > 0:
            dimension -= 1
    text = font.render("Mines: " + str(input_mines),True,BLACK)
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text, (((WIDTH/2+15)-(text_x/2)), ((HEIGHT/2-25) - (text_y / 2))))
    if button.buttonPress(((WIDTH/2+100)),((HEIGHT/2)-50), 20, 20, BLUE, AMBER, font, " U ", BLACK):
        if input_mines < 100 and input_mines < (dimension * dimension):
            input_mines += 1
    if button.buttonPress(((WIDTH/2+100)),((HEIGHT/2)-15), 20, 20, BLUE, AMBER, font, " D ", BLACK):
        if input_mines > 0:
            input_mines -= 1
    if button.buttonPress(300, 390, 100, 60, BLUE, AMBER,font,"Start",BLACK):
        game.reset(dimension, dimension, input_mines)
        game_Status = 0


class Tile(object):
    def __init__(self, x, y, columns, rows):
        self.columns = columns
        self.rows = rows
        self.x = (x * (size[0]/self.columns))
        self.y = (y * ((size[1]-150)/self.rows))+100
        self.mine = False
        self.neighbors = 0
        self.visible = False
        self.flag = False
        self.all_Visible = False

    def update(self):
        global game_Status, num_hit

        if game_Status == 0:
            if mouse_Status == 1 and mouse_x >= self.x and mouse_x <= (self.x + (size[0]/self.columns)) and mouse_y >= self.y and mouse_y <= (self.y +((size[1]-100)/self.rows)):
                self.visible = True
                self.flag = False
            if mouse_Status == 3 and mouse_x >= self.x and mouse_x <= (self.x + (size[0]/self.columns)) and mouse_y >= self.y and mouse_y <= (self.y + ((size[1]-100)/self.rows)):
                if self.flag == False:
                    self.flag = True
                elif self.flag == True:
                    self.flag = False
            #MODIFIED
            if self.all_Visible == True:
                game_Status = 1

    def show(self):
        if self.flag == True:
            pygame.draw.rect(screen,YELLOW,(self.x, self.y,(size[0]/self.columns),((size[1]-150)/self.rows)))
        if self.visible == True:
            if self.mine == False:
                pygame.draw.rect(screen,GREY,(self.x, self.y, (size[0] / self.columns), ((size[1]-150) / self.rows)))
                if self.neighbors >= 0:
                    text = font.render(str(self.neighbors),True,BLACK)
                    text_x = text.get_rect().width
                    text_y = text.get_rect().height
                    screen.blit(text,((self.x + ((size[0] / self.columns) / 2) - (text_x / 2)),
                                       (self.y + (((size[1] - 200) / self.rows) / 2) - (text_y / 2))))

            elif self.mine == True:
                pygame.draw.rect(screen,RED,(self.x, self.y, (size[0] / self.columns), ((size[1]-150) / self.rows)))
        pygame.draw.rect(screen,BLACK,(self.x, self.y,(size[0] / self.columns),((size[1]-150) / self.rows)), 2)


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
        self.num_visited = 0
        self.found_mines = 0
        self.num_hit = 0

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
        global game_Status, print_num_hit, print_num_flagged, print_safely_identified
        self.num_flagged = 0
        self.num_visited = 0
        self.found_mines = 0
        self.num_hit = 0
        for y in range(self.rows):
            for x in range(self.columns):
                self.board[y][x].update()
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
                    self.num_visited += 1
                #MODIFIED
                if self.board[y][x].visible == True and self.board[y][x].mine == True:
                    self.num_hit += 1

        for mine in self.mines:
            if self.board[mine[1]][mine[0]].flag == True:
                self.found_mines += 1

        for y in range(self.rows):
            for x in range(self.columns):
                if self.board[y][x].visible == True and self.num_visited == (self.rows * self.columns):
                    self.board[y][x].all_Visible = True
        #MODIFIED
        if self.board[y][x].all_Visible or (self.num_flagged == self.total_mines and self.found_mines == self.total_mines and self.num_visited == ((self.columns * self.rows) - self.total_mines)):
            print_num_flagged = self.num_flagged
            self.num_hit = self.total_mines - print_num_flagged
            print_num_hit = self.num_hit
            print_safely_identified = (self.num_flagged/self.total_mines)
            game_Status = 1
        elif (self.num_flagged + self.num_hit) == (self.total_mines) and self.num_flagged == self.found_mines:
            print_num_flagged = self.num_flagged
            self.num_hit = self.total_mines - print_num_flagged
            print_num_hit = self.num_hit
            print_safely_identified = (self.num_flagged / self.total_mines)
            game_Status = 1
        elif self.board[y][x].all_Visible:
            print_num_flagged = self.num_flagged
            self.num_hit = self.total_mines - print_num_flagged
            print_num_hit = self.num_hit
            print_safely_identified = (self.num_flagged / self.total_mines)
            game_Status = 1

        if game_Status == 1 or game_Status == 2 or game_Status == 9:
            for y in range(self.rows):
                for x in range(self.columns):
                    self.board[y][x].visible = True

    def render(self):
        for y in range(self.rows):
            for x in range(self.columns):
                self.board[y][x].show()

    def reset(self, columns, rows, mines):
        global print_num_hit
        print_num_hit = 0
        if columns != 0 and rows != 0 and mines != 0:
            self.columns = columns
            self.rows = rows
            self.total_mines = mines
        self.board = []
        self.mines = []
        self.mine_num = len(self.mines)
        self.neighbnum = 0
        self.num_flagged = 0
        self.num_visited = 0
        self.found_mines = 0

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
                    if self.board[y-1][x-1].mine == True:
                        self.neighbnum += 1
                if y > 0:
                    if self.board[y-1][x].mine == True:
                        self.neighbnum += 1
                if y > 0 and x < (self.columns - 1):
                    if self.board[y-1][x+1].mine == True:
                        self.neighbnum += 1
                if x > 0:
                    if self.board[y][x-1].mine == True:
                        self.neighbnum += 1
                if x < (self.columns-1):
                    if self.board[y][x+1].mine == True:
                        self.neighbnum += 1
                if x > 0 and y < (self.rows-1):
                    if self.board[y+1][x-1].mine == True:
                        self.neighbnum += 1
                if y < (self.rows-1):
                    if self.board[y+1][x].mine == True:
                        self.neighbnum += 1
                if x < (self.columns-1) and y < (self.rows - 1):
                    if self.board[y+1][x+1].mine == True:
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
        userInput()
    #MODIFIED
    elif game_Status >= 0 and game_Status <= 1:
        infoBar()
        resultBar()

        game.update()
        game.render()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
