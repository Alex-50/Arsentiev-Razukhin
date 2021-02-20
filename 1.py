import os, time, pygame, sys

FPS = 100

def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename, x, y):
    filename = "data/" + filename
    text = open(filename, 'r').readlines()
    if text[y][x] == '2':
        return Interior(x, y, 'torch.png', interior_sprite)
    elif text[y][x] == '6':
        global white_knight
        white_knight = Knight('kind', x, y, knights)
    elif text[y][x] == '5':
        return Knight('evil', x, y, dark_knights)


def artificial_intelligence(x, y, arr):
    order = None
    if arr[1][0] < 0:
        if my_board.board[x - 1][y] == 2 or my_board.board[x - 1][y] == 5:
            if arr[1][1] < 0:
                order = 'up'
            else:
                order = 'down'
        else:
            order = 'left'
    elif arr[1][0] > 0:
        if my_board.board[x + 1][y] == 2 or my_board.board[x + 1][y] == 5:
            if arr[1][1] < 0:
                order = 'up'
            else:
                order = 'down'
        else:
            order = 'right'
    elif arr[1][1] < 0 and arr[1][0] == 0:
        if my_board.board[x][y - 1] == 2 or my_board.board[x][y - 1] == 5:
            if arr[1][0] < 0:
                order = 'left'
            else:
                order = 'right'
        else:
            order = 'up'
    elif arr[1][1] > 0 and arr[1][0] == 0:
        if my_board.board[x][y + 1] == 2 or my_board.board[x][y + 1] == 5:
            if arr[1][0] < 0:
                order = 'left'
            else:
                order = 'right'
        else:
            order = 'down'
    return order


class Font(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('fon.png')
        self.image = pygame.transform.scale(self.image, (1366, 768))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Interior(pygame.sprite.Sprite):
    def __init__(self, x, y, image, *group):
        super().__init__(*group)
        self.image = load_image(image, 'white')
        self.image = pygame.transform.scale(self.image, (SSR, SSR))
        my_board.change((x, y), 2)
        self.rect = self.image.get_rect()
        self.rect.x = x * SSR
        self.rect.y = y * SSR


class Knight(pygame.sprite.Sprite):
    def __init__(self, karma, x, y, *group):
        super().__init__(*group)
        self.start_x, self.start_y = x, y
        self.karma = karma
        if karma == 'kind':
            self.image = load_image('knight.png', 'white')
            my_board.change((x, y), 6)
        elif karma == 'evil':
            self.image = load_image('dark_knight.png', 'white')
            my_board.change((x, y), 5)
        self.image = pygame.transform.scale(self.image, (SSR, SSR))
        self.rect = self.image.get_rect()
        self.rect.x = x * SSR
        self.rect.y = y * SSR
        self.x, self.y = x, y
        self.health = 1
        self.kill = True

    def update(self, *args):
        if self.karma == 'kind':
            if self.health > 0:
                if args and args[0].type == pygame.KEYDOWN:
                    try:
                        if args[0].key == pygame.K_DOWN:
                            self.image_down = load_image('knight.png', 'white')
                            self.image_down = pygame.transform.scale(self.image_down, (SSR, SSR))
                            self.image = self.image_down
                            assert my_board.board[self.x][self.y + 1] == 0
                            my_board.change((self.x, self.y + 1), 6)
                            my_board.change((self.x, self.y), 0)
                            self.y += 1
                            self.rect = self.rect.move(0, SSR)
                        elif args[0].key == pygame.K_LEFT:
                            self.image_left = load_image('knight_left.png', 'white')
                            self.image_left = pygame.transform.scale(self.image_left, (SSR, SSR))
                            self.image = self.image_left
                            assert my_board.board[self.x - 1][self.y] == 0
                            assert self.x != 0
                            my_board.change((self.x - 1, self.y), 6)
                            my_board.change((self.x, self.y), 0)
                            self.x -= 1
                            self.rect = self.rect.move(-SSR, 0)
                        elif args[0].key == pygame.K_UP:
                            self.image_up = load_image('knight_go_up.png', 'white')
                            self.image_up = pygame.transform.scale(self.image_up, (SSR, SSR))
                            self.image = self.image_up
                            assert self.y != 0
                            assert my_board.board[self.x][self.y - 1] == 0
                            my_board.change((self.x, self.y - 1), 6)
                            my_board.change((self.x, self.y), 0)
                            self.y -= 1
                            self.rect = self.rect.move(0, -SSR)
                        elif args[0].key == pygame.K_RIGHT:
                            self.image_right = load_image('knight_right.png', 'white')
                            self.image_right = pygame.transform.scale(self.image_right, (SSR, SSR))
                            self.image = self.image_right
                            assert my_board.board[self.x + 1][self.y] == 0
                            my_board.change((self.x + 1, self.y), 6)
                            my_board.change((self.x, self.y), 0)
                            self.x += 1
                            self.rect = self.rect.move(SSR, 0)
                            # time.sleep(0.1)
                    except IndexError:
                        pass
                    except AssertionError:
                        pass
            else:
                if self.kill:
                    my_board.change((self.x, self.y), 0)
                    self.kill = False
                    self.image = load_image('dead_knight.png', 'white')
                    self.image = pygame.transform.scale(self.image, (SSR, SSR))
        elif self.karma == 'evil':
            if self.health > 0:
                self.order, arr = None, []
                for i in range(9):
                    for o in range(5):
                        if my_board.board[i][o] == 6 or my_board.board[i][o] == 1:
                            arr.append((abs(abs(self.y - o) + abs(self.x - i)),
                                        (i - self.x, o - self.y), my_board.board[i][o]))
                try:
                    arr = sorted(arr, key=lambda o: o[0])[0]
                except IndexError:
                    arr = (0, (self.start_x - self.x, self.start_y - self.y), 0)
                self.order = artificial_intelligence(self.x, self.y, arr)
                try:
                    if self.order == 'down':
                        self.image_down = load_image('dark_knight.png', 'white')
                        self.image_down = pygame.transform.scale(self.image_down, (SSR, SSR))
                        self.image = self.image_down
                        if my_board.board[self.x][self.y + 1] == 6:
                            for i in knights:
                                if i.x == self.x and i.y == self.y + 1:
                                    i.health -= 1
                        assert my_board.board[self.x][self.y + 1] == 0
                        my_board.change((self.x, self.y + 1), 5)
                        my_board.change((self.x, self.y), 0)
                        self.y += 1
                        self.rect = self.rect.move(0, SSR)
                    elif self.order == 'left':
                        self.image_left = load_image('dark_knight_left.png', 'white')
                        self.image_left = pygame.transform.scale(self.image_left, (SSR, SSR))
                        self.image = self.image_left
                        if my_board.board[self.x - 1][self.y] == 6:
                            for i in knights:
                                if i.x == self.x - 1 and i.y == self.y:
                                    i.health -= 1
                        assert my_board.board[self.x - 1][self.y] == 0
                        assert self.x != 0
                        my_board.change((self.x - 1, self.y), 5)
                        my_board.change((self.x, self.y), 0)
                        self.x -= 1
                        self.rect = self.rect.move(-SSR, 0)
                    elif self.order == 'up':
                        self.image_up = load_image('dark_knight_go_up.png', 'white')
                        self.image_up = pygame.transform.scale(self.image_up, (SSR, SSR))
                        self.image = self.image_up
                        if my_board.board[self.x][self.y - 1] == 6:
                            for i in knights:
                                if i.x == self.x and i.y == self.y - 1:
                                    i.health -= 1
                        assert self.y != 0
                        assert my_board.board[self.x][self.y - 1] == 0
                        my_board.change((self.x, self.y - 1), 5)
                        my_board.change((self.x, self.y), 0)
                        self.y -= 1
                        self.rect = self.rect.move(0, -SSR)
                        time.sleep(0.3)
                    elif self.order == 'right':
                        self.image_right = load_image('dark_knight_right.png', 'white')
                        self.image_right = pygame.transform.scale(self.image_right, (SSR, SSR))
                        self.image = self.image_right
                        if my_board.board[self.x + 1][self.y] == 6:
                            for i in knights:
                                if i.x == self.x + 1 and i.y == self.y:
                                    i.health -= 1
                        assert my_board.board[self.x + 1][self.y] == 0
                        my_board.change((self.x + 1, self.y), 5)
                        my_board.change((self.x, self.y), 0)
                        self.x += 1
                        self.rect = self.rect.move(SSR, 0)
                    time.sleep(0.2)
                except IndexError:
                    pass
                except AssertionError:
                    pass
            else:
                if self.kill:
                    my_board.change((self.x, self.y), 0)
                    self.kill = False
                    self.image = load_image('dead_dark_knight.png', 'white')
                    self.image = pygame.transform.scale(self.image, (SSR, SSR))


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(len(self.board)):
            for x in range(len(self.board[i])):
                pygame.draw.rect(screen, 'white', (self.cell_size * i + self.left, self.cell_size * x +
                                                   self.top, self.cell_size, self.cell_size), 1)
                if i == 8 and x == 4:
                    pygame.draw.rect(screen, (119, 221, 119), (self.cell_size * i + self.left, self.cell_size * x +
                                                               self.top, self.cell_size, self.cell_size), 0)

    def coor(self, c):
        x, y = (c[0] - self.left) // self.cell_size, (c[1] - self.top) // self.cell_size
        if x < 0 or y < 0 or x > self.height - 1 or y > self.width - 1:
            return None
        return ((c[0] - self.left) // self.cell_size, (c[1] - self.top) // self.cell_size)

    def change(self, cor, object):
        self.board[cor[0]][cor[1]] = object


class Start_wnd:
    def __init__(self):
        self.start_screen()

    def check(self, args):
        x, y = args
        if self.coords[0][0] <= x <= self.coords[0][1]:
            for i in range(3):
                if self.coords[1][i][0] <= y <= self.coords[1][i][1]:
                    return i
        return None

    def start_screen(self):
        global v, d
        self.screen = pygame.display.set_mode((width, height))
        r = 5
        d = 40
        v = height / 4 - d
        w = 226
        button_color = (255, 255, 255)
        self.coords = [[570, 570 + w],
                       [[4 * (v + d) // 2 - 18, 4 * (v + d) // 2 - 18 + d],
                        [5 * (v + d) // 2 - 18, 5 * (v + d) // 2 - 18 + d],
                        [6 * (v + d) // 2, 6 * (v + d) // 2 + d]]]
        while True:
            fon = pygame.transform.scale(load_image('fon.png'), (width, height))
            self.screen.blit(fon, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    result = self.check(event.pos)
                    if result == 1:
                        return None
                    elif result == 2:
                        terminate()
                elif event.type == pygame.MOUSEMOTION:
                    if self.check(event.pos) == 1:
                        self.screen.fill(button_color, (570 - r, 5 * (v + d) // 2 - 18 - r, w + 2 * r, d + 2 * r))
                    elif self.check(event.pos) == 2:
                        self.screen.fill(button_color, (570 - 2 * r, 6 * (v + d) // 2 - 18 - r, w + 5 * r, d + 2 * r))
                font = pygame.font.Font(None, 50)
                font1 = pygame.font.Font(None, 100)
                font_1 = font1.render("KNIGHTS", True, pygame.Color("green"))
                font_2 = font.render("Начать игру", True, pygame.Color("black"))
                font_3 = font.render("Выйти из игры", True, pygame.Color("black"))
                self.screen.blit(font_1, (530, 4 * (v + d) // 2 - 10))
                self.screen.blit(font_2, (590, 5 * (v + d) // 2 - 10))
                self.screen.blit(font_3, (560, 6 * (v + d) // 2 - 10))
                pygame.display.flip()


class End_wnd:
    def __init__(self, end):
        running = True
        pygame.init()
        self.font = pygame.font.Font(None, 200)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            self.size = width, height = 1366, 768
            self.screen = pygame.display.set_mode(self.size)
            pygame.mouse.set_visible(True)
            if end:
                self.good()
            else:
                self.bad()
            pygame.display.flip()

    def good(self):
        self.screen.fill((255, 165, 0))
        font_1 = self.font.render("YOU WIN!", True, pygame.Color("black"))
        self.screen.blit(font_1, (350, 300))

    def bad(self):
        self.screen.fill((0, 0, 0))
        font_1 = self.font.render("YOU LOSE", True, pygame.Color("red"))
        self.screen.blit(font_1, (350, 300))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('my game')
    size = width, height = 1366, 768
    window = pygame.display.set_mode((1366, 768))
    SSR = height // 5
    pygame.init()
    music = pygame.mixer.Sound('data/muse.mp3')
    music.play(loops=-1)
    screen = pygame.display.set_mode(size)
    running = True
    Start_wnd()
    clock = pygame.time.Clock()
    interior_sprite = pygame.sprite.Group()
    one_sprite = pygame.sprite.Group()
    knights = pygame.sprite.Group()
    dark_knights = pygame.sprite.Group()

    my_board = Board(5, 9)
    my_board.set_view(0, 0, SSR)

    my_mouse = pygame.sprite.Sprite(one_sprite)
    my_mouse.image = load_image('peak.png', 'white')
    my_mouse.rect = my_mouse.image.get_rect()

    for y in range(5):
        for x in range(9):
            load_level('lvl1.txt', x, y)

    screen = pygame.display.set_mode(size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                my_mouse.rect.x = event.pos[0]
                my_mouse.rect.y = event.pos[1]
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                start = True
                try:
                    if event.key == 27:
                        terminate()
                    screen.fill('#ffe14d')
                    interior_sprite.draw(screen)
                    my_board.render()
                    knights.update(event)
                except AttributeError:
                    if white_knight.health > 0:
                        for i in dark_knights:
                            if (i.x, i.y) == my_board.coor(event.pos):
                                if (abs(i.x - white_knight.x) + abs(i.y - white_knight.y)) == 1:
                                    i.health -= 1
                    else:
                        knights.update(event)
                for i in dark_knights:
                    i.update(event)
                    screen.fill('#ffe14d')
                    interior_sprite.draw(screen)
                    my_board.render()
                    dark_knights.draw(screen)
                    knights.draw(screen)
                    pygame.display.flip()
                    clock.tick(FPS)
        screen.fill('#ffe14d')
        interior_sprite.draw(screen)
        my_board.render()
        knights.draw(screen)
        dark_knights.draw(screen)
        pygame.mouse.set_visible(False)
        one_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        if white_knight.x == 8 and white_knight.y == 4:
            time.sleep(0.5)
            End_wnd(True)
        if white_knight.health == 0:
            time.sleep(0.5)
            End_wnd(False)
terminate()
