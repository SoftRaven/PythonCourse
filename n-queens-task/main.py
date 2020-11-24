from random import *

from cell import *
from queen import *
from button import *
from numpy import *

WIDTH = 380
HEIGHT = 580
FPS = 30


class Game:

    def __init__(self):
        pygame.init()  # run pygame

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # set screen size
        pygame.display.set_caption("N-queens")  # set window caption
        self.clock = pygame.time.Clock()  # object for maintaining fixed frame frequency

        self.field = []  # initialize field matrix
        self.reset_field()  # fill field matrix with zero
        self.size = 8

        self.placed_queens_count = 0  # counter variable for right placed queens

        # create sprite groups
        self.game_field = pygame.sprite.Group()
        self.inventory_field = pygame.sprite.Group()
        self.queens = pygame.sprite.Group()

        # for entering menu
        self.intro = True

    # fill field matrix with zero
    def reset_field(self):
        self.field = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]

    # clear queens and start again
    def restart_game(self):
        self.reset_field()
        self.queens.empty()
        self.inventory_field.empty()
        self.game_field.empty()
        self.start()

    # quit game method
    @staticmethod
    def quit_game():
        pygame.quit()
        quit()

    # render text sprite
    @staticmethod
    def text_objects(text, font):
        text_surface = font.render(text, True, BLACK)
        return text_surface, text_surface.get_rect()

    # dragging logic
    def drag_figure(self, mouse):
        for queen in self.queens:
            if queen.clicked:
                queen.rect.x = mouse[0] - (queen.rect.width / 2)
                queen.rect.y = mouse[1] - (queen.rect.height / 2)

    # placing queen logic
    def place_queen(self, mouse, queen):
        queen.set_unclicked()
        # if queen is over some cell - stack it to this cell and mark this cell filled
        # for game field
        for cell in self.game_field:
            if cell.rect.collidepoint(mouse):
                if not cell.filled:
                    queen.rect.x = cell.rect.x
                    queen.rect.y = cell.rect.y
                    cell.set_filled()
                    i = cell.i
                    j = cell.j
                    # if wrong position mark this cell red
                    if not self.possible(i, j):
                        cell.set_red()
                    self.field[i][j] = 1
                else:
                    self.queen_to_inventory(queen)
        # for inventory field
        for cell in self.inventory_field:
            if cell.rect.collidepoint(mouse):
                if not cell.filled:
                    queen.rect.x = cell.rect.x
                    queen.rect.y = cell.rect.y
                    cell.set_filled()
                else:
                    self.queen_to_inventory(queen)

    # drop queen logic
    def drop_queen(self, mouse):
        for queen in self.queens:
            if queen.clicked:
                self.place_queen(mouse, queen)

    # select queen using mouse position and mark cell unfilled
    def pick_queen(self, mouse):
        # find necessary queen
        for queen in self.queens:
            if queen.rect.collidepoint(mouse):
                queen.set_clicked()

        # find necessary cell in game field
        for cell in self.game_field:
            i = cell.i
            j = cell.j

            if cell.rect.collidepoint(mouse):
                if cell.filled:
                    cell.set_unfilled()
                    cell.set_default_color()
                    self.field[i][j] = 0

            # check whether another queens now placed correctly and unmark their cells if necessary
            if self.field[i][j] == 1 and self.is_correct(i, j):
                cell.set_default_color()

        # find necessary cell in inventory field
        for cell in self.inventory_field:
            if cell.rect.collidepoint(mouse):
                if cell.filled:
                    cell.set_unfilled()

    # put queen to inventory
    def queen_to_inventory(self, queen):
        for cell in self.inventory_field:
            if not cell.filled:
                queen.rect.x = cell.rect.x
                queen.rect.y = cell.rect.y
                cell.set_filled()
                return

    # check whether it possible to place queen in given position
    def possible(self, y, x):
        # check for queens on row y
        for i in range(0, self.size):
            if self.field[y][i] == 1:
                return False

        # check for queens on column x
        for i in range(0, self.size):
            if self.field[i][x] == 1:
                return False

        # check for queens on a diagonals
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.field[i][j] == 1:  # if there is a queen
                    if abs(i - y) == abs(j - x):  # and if there is another on a diagonal
                        return False  # return false
        return True

    # generate game field with two-colored cells
    def generate_game_field(self, size, top, left, cell_size):
        for i in range(0, self.size):
            for j in range(0, self.size):
                if (i + j) % 2 == 0:
                    cell = Cell((top + cell_size * i), (left + cell_size * j), i, j, BLACK, cell_size)
                    self.game_field.add(cell)
                else:
                    cell = Cell((top + cell_size * i), (left + cell_size * j), i, j, BROWN, cell_size)
                    self.game_field.add(cell)

    # generate inventory field
    def generate_inventory_field(self, size, top, left, cell_size):
        for i in range(0, size):
            cell = Cell(top, (left + cell_size * i), i, 0, WHITE, cell_size)
            cell.set_filled()
            self.inventory_field.add(cell)

    # generate queens
    def generate_queens(self):
        for field in self.inventory_field:
            self.queens.add(Queen(field, (randint(0, 255), randint(0, 255), randint(0, 255))))

    # generate buttons on main game screen
    def generate_buttons(self):
        mouse_height = 40
        mouse_width = 150
        restart_button_x = 200
        restart_button_y = 450
        auto_generate_x = 200
        auto_generate_y = 500
        quit_button_x = 30
        quit_button_y = 450

        self.r_btn = Button(self.screen, "Restart game", GREEN_BUTTON, GREEN_BUTTON_HOVER, restart_button_x,
                            restart_button_y,
                            mouse_width, mouse_height, self.restart_game)
        self.q_btn = Button(self.screen, "Quit", RED_BUTTON, RED_BUTTON_HOVER, quit_button_x, quit_button_y,
                            mouse_width,
                            mouse_height, self.quit_game)
        self.ag_btn = Button(self.screen, "Auto generate", GREEN_BUTTON, GREEN_BUTTON_HOVER, auto_generate_x,
                             auto_generate_y,
                             mouse_width, mouse_height, self.auto_generate)

    # solving algorithm
    def solve(self):
        for y in range(self.size):
            for x in range(self.size):
                # we can place if there is no queen in given position
                if self.field[y][x] == 0:
                    # if empty, check if we can place a queen
                    if self.possible(y, x):
                        self.field[y][x] = 1  # if we can, then place it
                        self.solve()  # pass grid for recursive solution
                        # if we end up here, means we searched through all children branches
                        if sum(fromiter((sum(a) for a in self.field), dtype=int)) == self.size:  # if there are 8 queens
                            return self.field  # we are successful so return
                        self.field[y][x] = 0  # remove the previous placed queen

        return self.field  # means we searched the space, we can return our result

    # auto_generate button handler
    def auto_generate(self):
        # reset fields and put all placed queens to inventory
        self.reset_field()
        for queen in self.queens:
            self.queen_to_inventory(queen)
        for cell in self.game_field:
            cell.set_unfilled()
            cell.set_default_color()

        # handle button click
        self.ag_btn.set_up_text("Wait...")
        pygame.display.flip()
        # get the solution
        self.field = self.solve()
        self.ag_btn.set_up_text("Done!")
        pygame.display.flip()
        # place queens sprites
        self.auto_place_queens()

    def auto_place_queens(self):
        # mark all inventory unfilled
        for cell in self.inventory_field:
            cell.set_unfilled()

        # get a list of queens
        queens = [i for i in self.queens]

        # placing one by one queens
        k = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.field[i][j] == 1:
                    self.field[i][j] = 0
                    x_pos = 30 + 40 * j + 20
                    y_pos = 100 + 40 * i + 20
                    self.place_queen((x_pos, y_pos), queens[k])
                    k += 1

    # loop for entering menu
    def game_intro(self):
        while self.intro:
            for event in pygame.event.get():
                # quit event
                if event.type == pygame.QUIT:
                    self.quit_game()

            # fill background
            self.screen.fill(BACKGROUND)

            # create heading
            text = pygame.font.Font('fonts/Montserrat-Regular.ttf', 30)
            text_surf, text_rext = self.text_objects("N-Queens game", text)
            text_rext.center = (WIDTH / 2, 50)
            self.screen.blit(text_surf, text_rext)

            # buttons params
            mouse_height = 40
            mouse_width = 120
            start_button_x = 130
            start_button_y = 130
            quit_button_x = 130
            quit_button_y = 190

            # create buttons
            Button(self.screen, "Start game", GREEN_BUTTON, GREEN_BUTTON_HOVER, start_button_x, start_button_y,
                   mouse_width, mouse_height, self.start)
            Button(self.screen, "Quit", RED_BUTTON, RED_BUTTON_HOVER, quit_button_x, quit_button_y, mouse_width,
                   mouse_height, self.quit_game)

            # update display
            pygame.display.update()

    def start(self):
        self.intro = False

        # generate game field
        top = 110
        left = 30
        cell_size = 40
        self.generate_game_field(self.size, top, left, cell_size)

        # generate inventory field
        length = self.size
        top = 30
        left = 30
        self.generate_inventory_field(length, top, left, cell_size)

        # create and place eight queens
        self.generate_queens()

        # update display
        pygame.display.update()

        # run main loop
        self.game_loop()

    # counts how many queens are correctly placed
    def placed_queen_counter(self):
        self.placed_queens_count = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.field[i][j] == 1 and self.is_correct(i, j) is True:
                    self.placed_queens_count += 1

    # checks if queens is in a correct position
    def is_correct(self, i, j):
        self.field[i][j] = 0
        result = self.possible(i, j)
        self.field[i][j] = 1
        return result

    # shows a success banner
    def show_success_banner(self):
        text = pygame.font.Font('fonts/Montserrat-Regular.ttf', 24)
        text_surf, text_rext = self.text_objects("Congratulations! You win!", text)
        text_rext.center = (WIDTH / 2, 40)
        self.screen.blit(text_surf, text_rext)

    # main game loop
    def game_loop(self):
        running = True
        while running:
            # keep loop on right speed
            self.clock.tick(FPS)
            mouse = pygame.mouse.get_pos()

            # handling event
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    running = False
                # handle queens drag and drop
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pick_queen(mouse)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.drop_queen(mouse)

            # handling dragging queen
            self.drag_figure(mouse)

            self.placed_queen_counter()

            # rendering
            self.screen.fill(BACKGROUND)
            self.game_field.draw(self.screen)
            if self.placed_queens_count == self.size:
                self.show_success_banner()
            else:
                self.inventory_field.draw(self.screen)
            self.queens.draw(self.screen)
            self.generate_buttons()

            # after drawing flip screen
            pygame.display.flip()

        self.quit_game()


def main():
    game = Game()
    game.game_intro()


# if file is run directly, in case when it isn`t imported
if __name__ == '__main__':
    main()
