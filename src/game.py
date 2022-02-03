import sys
import pygame 
import math

ROW_COUNT = 6
COLUMN_COUNT = 7


class Game:
    def __init__(self):
        self.board = [ [0] * COLUMN_COUNT for i in range(ROW_COUNT) ]  
        self.turn = 1
        self.moves = 0

    def is_valid_slot(self, col):
        if (self.board[ROW_COUNT - 1][col] == 0):
            return True

    def move(self, row, column):
        self.board[row][column] = self.turn
        self.turn = 3 - self.turn
        self.moves += 1
        
    def next_valid_row(self, column):
        for row in range(ROW_COUNT):
            if (self.board[row][column] == 0):
                return row

    def win(self, player):
        # winning horizontally
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if (self.board[r][c] == player and self.board[r][c + 1] == player 
                    and self.board[r][c + 2] == player and self.board[r][c + 3] == player):
                    return True

        # winning vertically
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if (self.board[r][c] == player and self.board[r + 1][c] == player 
                    and self.board[r + 2][c] == player and self.board[r + 3][c] == player):
                    return True

        # winning diagonally positive
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if (self.board[r][c] == player and self.board[r + 1][c + 1] == player 
                    and self.board[r + 2][c + 2] == player and self.board[r + 3][c + 3] == player):
                    return True
	
        # winning diagonally negative
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if (self.board[r][c] == player and self.board[r - 1][c+ 1] == player 
                    and self.board[r - 2][c + 2] == player and self.board[r - 3][c + 3] == player):
                    return True






BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)


class View:
	def __init__(self):
		self.game_over = False
		self.game = Game()
		self.width = COLUMN_COUNT * SQUARESIZE
		self.height = (ROW_COUNT + 1) * SQUARESIZE
		self.size = (self.width, self.height)
		pygame.init()
		self.screen = pygame.display.set_mode(self.size)
		self.game_font = pygame.font.SysFont("monospace", 75)


	def draw_board(self):
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT):
				pygame.draw.rect(self.screen, BLUE, 
								(c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
				pygame.draw.circle(self.screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), 
														int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
	
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT):		
				if self.game.board[r][c] == 1:
					pygame.draw.circle(self.screen, RED, (int(c * SQUARESIZE+SQUARESIZE / 2), 
											self.height - int(r * SQUARESIZE+SQUARESIZE / 2)), RADIUS)
				elif self.game.board[r][c] == 2: 
					pygame.draw.circle(self.screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), 
											self.height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

		pygame.display.update()

	
	def player_input(self, event, player):
		posx = event.pos[0]
		col = int(math.floor(posx / SQUARESIZE))

		if self.game.is_valid_slot(col):
			row = self.game.next_valid_row(col)
			self.game.move(row, col)

			if self.game.win(player):
				label = self.game_font.render(f'Player {player} wins!', 1, RED)
				self.screen.blit(label, (40,10))
				self.game_over = True

			if self.game.moves == 42:
				label = self.game_font.render("Draw!", 1, RED)
				self.screen.blit(label, (40,10))
			
				self.game_over = True
		

	def play_game(self):
		self.draw_board()
		pygame.display.update()

		while not self.game_over:
			for event in pygame.event.get():
	
				if event.type == pygame.QUIT:
					sys.exit()


				if event.type == pygame.MOUSEMOTION:

					pygame.draw.rect(self.screen, BLACK, (0,0, self.width, SQUARESIZE))
					posx = event.pos[0]
					if self.game.turn == 1:
						pygame.draw.circle(self.screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
					else: 
						pygame.draw.circle(self.screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
				pygame.display.update()


				if event.type == pygame.MOUSEBUTTONDOWN:

					pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE))
					# Player 1 Input
					if self.game.turn == 1:
						self.player_input(event, 1)

					# Player 2 Input
					else:		
						self.player_input(event, 2)

					self.draw_board()


					if self.game_over:
						pygame.time.wait(3000)
						

view = View()
view.play_game()