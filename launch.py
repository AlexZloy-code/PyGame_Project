class Window:
    def get_coord(self, mouse_pos):
        return mouse_pos[0], mouse_pos[1]


class User:
    def __init__(self):
        self.name = None

    def set_info(self, name, count, id, url_icon):
        self.name = name
        self.count = count
        self.id = id
        self.url_icon = url_icon

    def __call__(self):
        if self.name:
            print(f'User_id: {self.id}\nUser_name: {self.name}\nUser_count: {self.count}')
        else:
            print('Данных о пользователе нету')


class Main(Window):
    def draw_window(self):
        screen.fill((153, 153, 255))

        all_sprites = pygame.sprite.Group()
        
        exit = pygame.sprite.Sprite()
        exit.image = pygame.transform.scale(pygame.image.load('static/image/exit.png'), (50, 50))
        exit.rect = exit.image.get_rect()
        exit.rect.x = 10
        exit.rect.y = 20

        profile = pygame.sprite.Sprite()
        profile.image = pygame.transform.scale(pygame.image.load('static/image/profile.png'), (50, 50))
        profile.rect = profile.image.get_rect()
        profile.rect.x = 70
        profile.rect.y = 20

        all_sprites.add(exit)
        all_sprites.add(profile)
        
        all_sprites.draw(screen)

        font = pygame.font.Font(None, 50)
        title_1 = font.render('Приветствую в игре', True, (0, 0, 0))
        screen.blit(title_1, (180, 90))

        try:
            all_sprites = pygame.sprite.Group()
            title = pygame.sprite.Sprite()
            title.image = pygame.transform.scale(pygame.image.load('static/image/Nonogram.png'), (400, 50))
            title.rect = title.image.get_rect()
            title.rect.x = 150
            title.rect.y = 150
            all_sprites.add(title)
            all_sprites.draw(screen)
        except Exception:
            font = pygame.font.Font(None, 50)
            title_2 = font.render('Nonogram', True, (255, 255, 255))
            screen.blit(title_2, (250, 150))
        
        font = pygame.font.Font(None, 50)
        games = font.render('Играть', True, (0, 0, 0))
        screen.blit(games, (290, 400))

        font = pygame.font.Font(None, 50)
        rules = font.render('Правила игры', True, (0, 0, 0))
        screen.blit(rules, (230, 500))
        
        pygame.display.flip()

    def open_new_window(self):
        global window
        if 10 < x < 60 and 20 < y < 70:
            pygame.quit()
            quit()
        elif 70 < x < 120 and 20 < y < 70:
            window = Profile()
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
        home.image = pygame.transform.scale(pygame.image.load('static/image/home.png'), (50, 50))
        home.rect = home.image.get_rect()
        home.rect.x = 20
        home.rect.y = 20
        all_sprites.add(home)
        

        if user.name:
            font = pygame.font.Font(None, 50)
            rules = font.render(user.name, True, (0, 0, 0))
            screen.blit(rules, (290, 100))

            icon = pygame.sprite.Sprite()
            icon.image = pygame.transform.scale(pygame.image.load(user.url_icon), (250, 250))
            icon.rect = icon.image.get_rect()
            icon.rect.x = 220
            icon.rect.y = 150
            all_sprites.add(icon)

            level_form = 'уровней' if user.count > 4 or user.count == 0 else 'уровня' if user.count > 1 else 'уровень'
            font = pygame.font.Font(None, 30)
            rules = font.render(f'Вы решили {user.count} {level_form}', True, (0, 0, 0))
            screen.blit(rules, (240, 420))

            font = pygame.font.Font(None, 30)
            rules = font.render(f'Вы решили больше Nonogram, чем {procent_ot_count(user.count)}% людей', True, (0, 0, 0))
            screen.blit(rules, (110, 500))

        else:
            font = pygame.font.Font(None, 50)
            rules = font.render('Вы не авторизированы', True, (0, 0, 0))
            screen.blit(rules, (145, 100))

            font = pygame.font.Font(None, 50)
            rules = font.render('Войти в акаунт', True, (0, 0, 0))
            screen.blit(rules, (220, 420))

            font = pygame.font.Font(None, 50)
            rules = font.render('Авторизироваться', True, (0, 0, 0))
            screen.blit(rules, (170, 500))
        
        all_sprites.draw(screen)
        pygame.display.flip()

    def open_new_window(self):
        global window
        if 20 < x < 70 and 20 < y < 70:
            window = Main()
            pygame.display.set_caption('Главная')
            window.draw_window()
        elif 240 < x < 480 and 450 < y < 540 and not user.name:
            class reg(QWidget):
                def __init__(self):
                    super().__init__()
                    name, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter name of account:')
                    if ok:
                        password, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter password of account:')
                        if ok:
                            con = sqlite3.connect('static/db/gamers.db')
                            cur = con.cursor()
                            res = cur.execute(f"""SELECT * FROM users
                                                           WHERE password = '{password}'
                                                           AND login = '{name}'""").fetchall()  # поиск аккаунта
                            if not res:  # Обработка результата
                                id_acc = [i[0] for i in cur.execute(f"""SELECT * FROM users""").fetchall()] + [-1]
                                cur.execute(f'''INSERT INTO Users('userid', 'login', 'password', 'result', 'url_icon')
                                                VALUES({max(id_acc) + 1}, '{name}', '{password}', 0, 'static/icons/Base.png')''')
                                con.commit()
                                sucsess = QMessageBox()
                                sucsess.setWindowTitle("Успешно")
                                sucsess.setText("Вы зарегистрировались")
                                sucsess.setIcon(QMessageBox.Icon.Information)
                                sucsess.setStandardButtons(
                                    QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
                                )
                                sucsess.exec()
                                user.set_info(name, 0, max(id_acc) + 1, 'static/icons/Base.png')
                            else:
                                user.set_info(res[1], res[3], res[4])

            app = QApplication(sys.argv)
            ex = reg()
            ex.show()
            window.draw_window()


class Games(Window):
    def draw_window(self):
        screen.fill((153, 153, 255))

        all_sprites = pygame.sprite.Group()
        home = pygame.sprite.Sprite()
        home.image = pygame.transform.scale(pygame.image.load('static/image/home.png'), (50, 50))
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
        home.image = pygame.transform.scale(pygame.image.load('static/image/home.png'), (50, 50))
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


def load_image(name):
    fullname = os.path.join('static/image', name)
    image = pygame.image.load(fullname)
    return image


def procent_ot_count(count):
    return 100


if __name__ == '__main__':
    import pygame
    import os
    from PyQt6.QtWidgets import QApplication, QWidget, QInputDialog, QMessageBox
    import sys
    import sqlite3

    user = User()

    con = sqlite3.connect('static/db/gamers.db')  # Создание базы данных
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            userid        INTEGER PRIMARY KEY,
            login         TEXT,
            password      TEXT,
            result        INTEGER,
            url_icon      TEXT
        )
    ''')
 
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