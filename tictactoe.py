import copy
import random
import sys
import pygame
import numpy as np

from constants import *

# PYGAME Boilerplate
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TIC TAC TOE VS JORDAN AT 1% POWER')
screen.fill( BG_COLOR)

class Board:
    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqrs = self.squares # [sqaures]
        self.marked_sqrs = 0

    def final_state(self, show = False):
        '''
            @returns 0 if there is no win yet (does not mean there is a draw)
            @reutnrs 1 if player 1 wins
            @returns 2 if player 2 wins
        '''

        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]
            
        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]
        
        # desc diagonal
        if self.squares[0][0] == self.squares [1][1] == self.squares[2][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                    iPos = (20, 20)
                    fPos = (HEIGHT - 20, WIDTH - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][0]
        
        # asc diagonal
        if self.squares[2][0] == self.squares [1][1] == self.squares[0][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                    iPos = (20, HEIGHT - 20)
                    fPos = (WIDTH - 20, 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[2][0]
        # no win yet
        return 0

    def mark_sq(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sq(row, col):
                    empty_sqrs.append( (row, col) )
        return empty_sqrs
    
    def empty_sq(self,row,col):
        return self.squares[row][col] == 0
    def isFull(self):
        return self.marked_sqrs == 9
    def isEmpty(self):
        return self.marked_sqrs == 0


class AI:
    def __init__(self, level = 1, player = 2): # use level 0 for randomness (annie on 100% brainpower)
        self.level = level
        self.player = player




    def random(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[idx] # return some row, col
    
    def minimax(self, board, maximizing):
        # checking terminal cases
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # Eval, move
        # player 2 wins
        if case == 2:
            return -1, None
        # draw
        elif board.isFull():
            return 0, None
        
        if maximizing:
            max_eval = -100 # can be any number greater than 1
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sq(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move
        elif not maximizing:
            min_eval = 100 # can be any number greater than 1
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sq(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move


    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.random(main_board)
        else:
            # minmax algo choice
            eval, move = self.minimax(main_board, False)
    
        print(f'Jordan at 1% power has chosen to mark the square in pos{move} with an evaluation of {eval}')



        return move # row, col
class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 # X player = 1, O player = 2
        self.gamemode = 'ai' # pvp or ai
        self.running = True
        self.show_lines()
    
    def make_move(self, row, col):
        self.board.mark_sq(row,col,self.player)
        self.draw_fig(row, col,self.player)
        self.next_turn()

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'



    def show_lines(self):
        # BG FILL
        screen.fill( BG_COLOR )
        # vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH-SQSIZE, HEIGHT), LINE_WIDTH)
        # horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)


    def draw_fig(self, row, col, player):
        if player == 1:
            # Draw an X
            # descending line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # ascending line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif player == 2:
            # Draw an O
            center = (col * SQSIZE + SQSIZE//2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)
    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isFull()
    def next_turn(self):
        self.player = self.player % 2 + 1
    def reset(self):
        self.__init__()
    



def main():
    # object
    game = Game()
    board = game.board
    ai = game.ai

    while True:
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # g key changes gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()
                # 0- random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                # 1- ai powered moves
                if event.key == pygame.K_1:
                    ai.level = 1    
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                if board.empty_sq(row,col):
                    game.make_move(row,col)

                    if game.isover():
                        game.running = False


        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            pygame.display.update()

            # methods

            row, col = ai.eval(board)

            game.make_move(row,col)
            if game.isover():
                game.running = False

        pygame.display.update()


main()