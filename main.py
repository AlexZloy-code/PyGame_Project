import pygame
import os


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


class User:
    def __init__(self):
        self.name = 'undefinded'

    def set_info(self, name, count, id):
        self.name = name
        self.count = count
        self.id = id

    def __call__(self):
        if self.name != 'undefinded':
            print(f'User_id: {self.id}\nUser_name: {self.name}\nUser_count: {self.count}')
        else:
            print('Данных о пользователе нету')


class Window:
    def get_coord(self, mouse_pos):
        return mouse_pos[0], mouse_pos[1]


class Main(Window):
    def draw_window(self):
        screen.fill((153, 153, 255))

        all_sprites = pygame.sprite.Group()
        
        exit = pygame.sprite.Sprite()
        exit.image = pygame.transform.scale(load_image('exit.png'), (50, 50))
        exit.rect = exit.image.get_rect()
        exit.rect.x = 10
        exit.rect.y = 20

        profile = pygame.sprite.Sprite()
        profile.image = pygame.transform.scale(load_image('profile.png'), (50, 50))
        profile.rect = profile.image.get_rect()
        profile.rect.x = 70
        profile.rect.y = 20

        all_sprites.add(exit)
        all_sprites.add(profile)
        
        all_sprites.draw(screen)

        font = pygame.font.Font(None, 50)
        rules = font.render('Приветсвую в игре', True, (0, 0, 0))
        screen.blit(rules, (180, 50))

        font = pygame.font.Font(None, 50)
        rules = font.render('Nonogram', True, (255, 255, 255))
        screen.blit(rules, (250, 100))
        
        font = pygame.font.Font(None, 50)
        games = font.render('Играть', True, (0, 0, 0))
        screen.blit(games, (295, 400))

        font = pygame.font.Font(None, 50)
        rules = font.render('Правила игры', True, (0, 0, 0))
        screen.blit(rules, (240, 500))
        
        pygame.display.flip()

    def open_new_window(self):
        global window
        if 10 < x < 60 and 20 < y < 70:
            pygame.quit()
            quit()
        elif 70 < x < 120 and 20 < y < 70:
            window = Rules()
            pygame.display.set_caption('Профиль')
            window.draw_window()
        elif 295 < x < 420 and 400 < y < 440:
            window = Games()
            pygame.display.set_caption('Играть')
            window.draw_window()
        elif 240 < x < 480 and 500 < y < 540:
            window = Rules()
            pygame.display.set_caption('Правила игры')
            window.draw_window()


class Profile(Window):
    def draw_window(self):
        screen.fill((153, 153, 255))

        all_sprites = pygame.sprite.Group()
        home = pygame.sprite.Sprite()
        home.image = pygame.transform.scale(load_image('home.png'), (50, 50))
        home.rect = home.image.get_rect()
        home.rect.x = 20
        home.rect.y = 20
        all_sprites.add(home)
        all_sprites.draw(screen)
        
        pygame.display.flip()

    def open_new_window(self):
        global window
        if 20 < x < 70 and 20 < y < 70:
            window = Main()
            pygame.display.set_caption('Главная')
            window.draw_window()


class Games(Window):
    def draw_window(self):
        screen.fill((153, 153, 255))

        all_sprites = pygame.sprite.Group()
        home = pygame.sprite.Sprite()
        home.image = pygame.transform.scale(load_image('home.png'), (50, 50))
        home.rect = home.image.get_rect()
        home.rect.x = 20
        home.rect.y = 20
        all_sprites.add(home)
        all_sprites.draw(screen)
        
        pygame.display.flip()

    def open_new_window(self):
        global window
        if 20 < x < 70 and 20 < y < 70:
            window = Main()
            pygame.display.set_caption('Главная')
            window.draw_window()


class Rules(Window):
    def draw_window(self):
        screen.fill((153, 153, 255))

        all_sprites = pygame.sprite.Group()
        home = pygame.sprite.Sprite()
        home.image = pygame.transform.scale(load_image('home.png'), (50, 50))
        home.rect = home.image.get_rect()
        home.rect.x = 20
        home.rect.y = 20
        all_sprites.add(home)
        all_sprites.draw(screen)
        
        pygame.display.flip()

    def open_new_window(self):
        global window
        if 20 < x < 70 and 20 < y < 70:
            window = Main()
            pygame.display.set_caption('Главная')
            window.draw_window()



if __name__ == '__main__':
    user = User()
    pygame.init()
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Главная')
    pygame.display.flip()

    window = Main()
    window.draw_window()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = window.get_coord(event.pos)
                window.open_new_window()
    pygame.quit()