import pygame
import sys
import os
import start_menu
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением {fullname} не найден")
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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def start(l_map):
    # CONST
    WIDTH = 750
    HEIGHT = 750
    STEP = 10
    FPS = 50

    a = 1
    # INIT GAME
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    score = 0

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    entity_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    clock = pygame.time.Clock()

    # BASE METHODS

    wall_images = {
        'wall': load_image('wall.png')
    }
    entity_images = {
        'finish': load_image('finish.png')
    }
    enemy_images = {
        'en_wall': load_image('enemy.png'),
        'fly': load_image('fly.png')
    }

    player_image = load_image('player.png')

    wall_width = wall_height = 40

    # GAME

    def pause():

        text = "Tap to play"
        screen.blit(load_image('pause_fon.png'), (150, 150))
        font = pygame.font.Font("04B_19.TTF", 50)
        string_rendered = font.render(text, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        intro_rect.y = 490
        intro_rect.x = 230
        screen.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            if pygame.time.get_ticks()//1000 % 2 == 0:
                pl = load_image('player2.png')
                #print(clock.get_time())
            else:
                pl = load_image('player.png')
            screen.blit(pl, (360, 190))
            pygame.display.flip()
            clock.tick(FPS)

    def win_end_screen():
        pygame.mouse.set_visible(True)
        counter = 1
        fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
        star_group = pygame.sprite.Group()
        star_image = load_image('star.png', colorkey=-1)

        for i in range(20):
            star = pygame.sprite.Sprite(star_group)
            star.image = star_image
            star.rect = star.image.get_rect()
            star_mask = pygame.mask.from_surface(star.image)

            x = random.randrange(50, 660, 10)
            y = random.randrange(50, 660, 10)
            while 200 <= x <= 400 and 200 <= y <= 400 or\
                    200 <= x <= 500 and y >= 460:
                x = random.randrange(50, 660, 10)
                y = random.randrange(50, 660, 10)
            star.rect.x = x
            star.rect.y = y

        screen.blit(fon, (0, 0))
        star_group.draw(screen)

        intro_text = ["You're the winner", "      +100",
                      "     the End",]
        e_text = "tap to exit"

        font = pygame.font.Font('04B_19.TTF', 35)
        text_coord = 250
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord += 15
            intro_rect.top = text_coord
            intro_rect.x = 200
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        ex_text = font.render(e_text, 1, pygame.Color('yellow'))
        ex_text_r = ex_text.get_rect()
        ex_text_r.top = 600
        ex_text_r.x = 250

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            if counter < 4:
                screen.blit(ex_text, ex_text_r)
                counter += 1
            else:
                screen.fill('black', (250, 600, 200, 60))
                counter = 1


            pygame.display.flip()
            clock.tick(3)

    def lose_end_screen():
        pygame.mouse.set_visible(True)
        counter = 10
        string_text = ["    You lost", "     Exit in", "", "", "Tap to restart"]

        fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font('04B_19.TTF', 50)
        text_coord = 220
        for line in string_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            text_coord += intro_rect.height
            text_coord += 15
            intro_rect.x = 200
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    start(l_map)
            if counter > 0:
                if counter % 2 == 0:
                    font2 = pygame.font.Font('04B_19.TTF', 80)
                    string_rendered2 = font2.render(str(counter // 2), 1, pygame.Color('red'))
                    intro_rect2 = string_rendered2.get_rect()
                    intro_rect2.top = 370
                    intro_rect2.x = 360
                    screen.blit(string_rendered2, intro_rect2)
                else:
                    screen.fill('black', (360, 375, 60, 70))
                counter -= 1
            else:
                return
            pygame.display.flip()
            clock.tick(2)

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.image = player_image
            self.rect = self.image.get_rect().move(
                wall_width * pos_x, wall_height * pos_y)

    class Wall(pygame.sprite.Sprite):
        def __init__(self, wall_type, pos_x, pos_y):
            super().__init__(walls_group, all_sprites)
            self.image = wall_images[wall_type]
            self.rect = self.image.get_rect().move(
                wall_width * pos_x, wall_height * pos_y)

    class Entity(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(entity_group, all_sprites)
            self.image = entity_images[tile_type]
            self.rect = self.image.get_rect().move(
                wall_width * pos_x, wall_height * pos_y)

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(enemy_group, all_sprites)
            self.image = enemy_images[tile_type]
            self.rect = self.image.get_rect().move(
                wall_width * pos_x, wall_height * pos_y)

    def generate_level(level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    pass
                elif level[y][x] == '#':
                    Wall('wall', x, y)
                elif level[y][x] == '=':
                    Entity('finish', x, y)
                elif level[y][x] == '%':
                    Enemy('en_wall', x, y)
                elif level[y][x] == '@':
                    new_player = Player(x, y)
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y

    def collideP(group):
        if not pygame.sprite.groupcollide(player_group, group, False, False):
            return False
        else:
            return True

    class Camera:
        # зададим начальный сдвиг камеры
        def __init__(self):
            self.dx = 0
            self.dy = 0

        # сдвинуть объект obj на смещение камеры
        def apply(self, obj):
            obj.rect.x += self.dx
            obj.rect.y += self.dy

        # позиционировать камеру на объекте target
        def update(self, target):
            self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
            self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)

    def main(lvl_map):

        # start_screen()
        running = True
        game_ov = None
        player, level_x, level_y = generate_level(load_level(lvl_map))
        camera = Camera()
        counter = 1

        pygame.mouse.set_visible(False)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_ov = 'Lose'
                    running = False

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                pygame.mouse.set_visible(True)
                pause()
                pygame.mouse.set_visible(False)

            if key[pygame.K_DOWN]:
                while not collideP(walls_group) and not collideP(enemy_group):
                    player.rect.top += STEP
                if collideP(enemy_group):
                    game_ov = 'Lose'
                    running = False
                else:
                    player.rect.top -= STEP
                player.image = player_image
            elif key[pygame.K_UP]:
                while not collideP(walls_group) and not collideP(enemy_group):
                    player.rect.top -= STEP
                if collideP(enemy_group):
                    game_ov = 'Lose'
                    running = False
                else:
                    player.rect.top += STEP
                player.image = pygame.transform.rotate(player_image, 180)
            elif key[pygame.K_RIGHT]:
                while not collideP(walls_group) and not collideP(enemy_group):
                    player.rect.left += STEP
                if collideP(enemy_group):
                    game_ov = 'Lose'
                    running = False
                else:
                    player.rect.left -= STEP
                player.image = pygame.transform.rotate(player_image, 90)
            elif key[pygame.K_LEFT]:
                while not collideP(walls_group) and not collideP(enemy_group):
                    player.rect.left -= STEP
                if collideP(enemy_group):
                    game_ov = 'Lose'
                    running = False
                else:
                    player.rect.left += STEP
                player.image = pygame.transform.rotate(player_image, -90)

            if collideP(entity_group):
                game_ov = 'Win'
                running = False

            # изменяем ракурс камеры
            camera.update(player)


            # обновляем положение всех спрайтов
            for sprite in all_sprites:
                camera.apply(sprite)

            screen.fill((0, 0, 0))
            enemy_group.draw(screen)
            entity_group.draw(screen)
            player_group.draw(screen)
            walls_group.draw(screen)
            clock.tick(FPS)

            pygame.display.flip()

        if game_ov == 'Win':
            win_end_screen()
            start_menu.score += 100
            start_menu.main()
        else:
            lose_end_screen()
            start_menu.main()

        pygame.quit()

    main(l_map)
