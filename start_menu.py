import pygame
import game_run

import pygame_widgets
from pygame_widgets.button import Button

money = 0
pygame.init()
screen = pygame.display.set_mode((750, 750))
pygame.display.set_caption('Tomb of the mask')
clock = pygame.time.Clock()
FPS = 50
counter = 1
score = 0


def start_screen():
    global counter

    fon = pygame.transform.scale(game_run.load_image('start_fon.png'), (750, 750))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('04B_19.TTF', 50)
    text_coord = 320
    screen.fill('yellow', (110, 300, 500, 150))
    string_rendered1 = font.render("Tomb of the mask", 1, pygame.Color('black'))
    intro_rect1 = string_rendered1.get_rect()
    intro_rect1.top = text_coord
    intro_rect1.x = 130
    screen.blit(string_rendered1, intro_rect1)

    text_coord2 = 380
    string_rendered2 = font.render("Tap to start", 1, pygame.Color('black'))
    intro_rect2 = string_rendered1.get_rect()
    intro_rect2.top = text_coord2
    intro_rect2.x = 190

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run.terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        if counter < 5:
            screen.blit(string_rendered2, intro_rect2)
            counter += 1
        else:
            screen.fill('yellow', (110, 370, 500, 80))
            counter = 1
        pygame.display.flip()
        clock.tick(4)


def main():
    win = pygame.display.set_mode((750, 750))
    pygame.mouse.set_visible(True)

    button1 = Button(win, 20, 80, 160, 80, text='1', fontSize=50, margin=20, inactiveColour='yellow',
                     hoverColour=(200, 200, 0), pressedColour=(255, 255, 255), radius=2,
                     onClick=lambda: game_run.start('map1.txt'))
    button2 = Button(win, 200, 80, 160, 80, text='2', fontSize=50, margin=20, inactiveColour='yellow',
                     hoverColour=(200, 200, 0), pressedColour=(255, 255, 255), radius=2,
                     onClick=lambda: game_run.start('map2.txt'))
    button3 = Button(win, 380, 80, 160, 80, text='3', fontSize=50, margin=20, inactiveColour='yellow',
                     hoverColour=(200, 200, 0), pressedColour=(255, 255, 255), radius=2,
                     onClick=lambda: game_run.start('map3.txt'))
    button4 = Button(win, 560, 80, 160, 80, text='4', fontSize=50, margin=20, inactiveColour='yellow',
                     hoverColour=(200, 200, 0), pressedColour=(255, 255, 255), radius=2,
                     onClick=lambda: game_run.start('map4.txt'))

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill('black')
        font = pygame.font.Font('04B_19.TTF', 30)
        string_rendered = font.render(f"score: {score}", 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 30
        intro_rect.x = 300
        screen.blit(string_rendered, intro_rect)

        pygame_widgets.update(events)
        pygame.display.flip()


if __name__ == '__main__':
    start_screen()
    main()
