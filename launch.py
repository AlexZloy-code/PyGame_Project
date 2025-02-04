import pygame
import os
import shutil
from PyQt6.QtWidgets import QApplication, QWidget, QInputDialog, QMessageBox, QFileDialog
import sys
import sqlite3


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


class Main(Window):
    def draw_window(self):
        screen.fill((153, 153, 255))

        icons = [
            ['static/image/exit.png', (50, 50), (10, 20)],
            ['static/image/profile.png', (50, 50), (70, 20)]
        ]
        
        for elems in icons:
            blit_image(*elems)

        texts = [
            [50, 'Приветствую в игре', (180, 90)],
            [50, 'Играть', (290, 400)],
            [50, 'Правила игры', (230, 500)]
        ]

        for elems in texts:
            blit_text(*elems)

        try:
            blit_image('static/image/Nonogram.png', (400, 50), (150, 150))
        except Exception:
            blit_text(50, 'Nonogram', (250, 150))

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

        blit_image('static/image/home.png', (50, 50), (20, 20))

        if user.name:

            blit_image('static/image/change_profile.png', (50, 50), (90, 20))

            level_form = 'уровней' if user.count > 4 or user.count == 0 else 'уровня' if user.count > 1 else 'уровень'
            texts = [
                [50, user.name, (290, 100)],
                [30, f'Вы решили {user.count} {level_form}', (240, 420)],
                [30, f'Вы решили больше Nonogram, чем {rating(user.count)}% людей', (120, 500)]
            ]

            for elems in texts:
                blit_text(*elems)

            blit_image(user.url_icon, (250, 250), (220, 150))
        else:
            texts = [
                [50, 'Вы не авторизированы', (145, 100)],
                [50, 'Авторизироваться', (190, 500)]
            ]

            for elems in texts:
                blit_text(*elems)

        pygame.display.flip()

    def open_new_window(self):
        global window
        if 20 < x < 70 and 20 < y < 70:
            window = Main()
            pygame.display.set_caption('Главная')
            window.draw_window()
        elif 90 < x < 140 and 20 < y < 70:
            class reg(QWidget):
                def __init__(self):
                    super().__init__()
                    picture_name = QFileDialog.getOpenFileName(self, 'Выберите файл:', '', '*.jpg *.png *.bmp')[0]
                    try:
                        shutil.copy(picture_name, f'{os.path.dirname(os.path.abspath(__file__))}\static\icons')
                    except Exception:
                        pass
                    con = sqlite3.connect('static/db/gamers.db')
                    cur = con.cursor()  # поиск аккаунта
                    cur.execute(f"""UPDATE users SET url_icon = 'static/icons/{picture_name.split("/")[-1]}'
                                    WHERE userid = {user.id}""").fetchall()
                    con.commit()
                    user.set_info(user.name, user.count, user.id, f'static/icons/{picture_name.split("/")[-1]}')
                    sucsess = QMessageBox()
                    sucsess.setWindowTitle("Успешно")
                    sucsess.setText(f"Вы изменили фото профиля")
                    sucsess.setIcon(QMessageBox.Icon.Information)
                    sucsess.setStandardButtons(
                        QMessageBox.StandardButton.Ok
                    )
                    sucsess.exec()
            app = QApplication(sys.argv)
            ex = reg()
            ex.show()
            window.draw_window()
        elif 190 < x < 500 and 500 < y < 540 and not user.name:
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
                                    QMessageBox.StandardButton.Ok
                                )
                                sucsess.exec()
                                user.set_info(name, 0, max(id_acc) + 1, 'static/icons/Base.png')
                            else:
                                sucsess = QMessageBox()
                                sucsess.setWindowTitle("Успешно")
                                sucsess.setText(f"Вы вошли в аккаунт {name}")
                                sucsess.setIcon(QMessageBox.Icon.Information)
                                sucsess.setStandardButtons(
                                    QMessageBox.StandardButton.Ok
                                )
                                sucsess.exec()
                                user.set_info(res[0][1], res[0][3], res[0][0], res[0][4])
            app = QApplication(sys.argv)
            ex = reg()
            ex.show()
            window.draw_window()


class Games(Window):
    def nums_to_lines(self, answer):

        mas_for_return = []

        for a in range(len(answer)):
            nulls = [-1] + [i for i in range(len(answer[a])) if answer[a][i] != 1] + [len(answer[a])]
            nums = [str(nulls[i + 1] - nulls[i] - 1) for i in range(len(nulls) - 1) if nulls[i + 1] - nulls[i] > 1]
            mas_for_return.append(nums)
        

        answer = [[answer[i][j] for i in range(len(answer))] for j in range(len(answer[0]))]

        for a in range(len(answer)):
            nulls = [-1] + [i for i in range(len(answer[a])) if answer[a][i] != 1] + [len(answer[a])]
            nums = [str(nulls[i + 1] - nulls[i] - 1) for i in range(len(nulls) - 1) if nulls[i + 1] - nulls[i] > 1]
            mas_for_return.append(nums)
        
        return mas_for_return
            

    def draw_window(self, x=-1, y=0, touth=False):
        global window
        if x == -1:
            from levels import random_level, levels
            self.answer = levels[random_level()]
            self.otstup = 120
            self.row_count, self.column_count = len(self.answer), len(self.answer[0])
            self.size_rect = (700 - self.otstup) // max(self.row_count, self.column_count)
            self.mas = [[0 for _ in range(self.column_count)] for _ in range(self.row_count)]

        screen.fill((255, 153, 153))

        for a in range(self.row_count):
            nums = self.nums_to_lines(self.answer)[a]
            blit_text(self.size_rect // 2, ' '.join(nums), (20, self.otstup + a * self.size_rect))


        for a in range(self.row_count, self.row_count + self.column_count):
            nums = self.nums_to_lines(self.answer)[a]
            if len(nums) == 1:
                blit_text(self.size_rect // 2, ' '.join(nums), (self.otstup + (a - self.row_count) * self.size_rect, 10))
            elif len(nums) > 1:
                for i in range(len(nums)):
                    blit_text(self.size_rect // 3, nums[i], (self.otstup + (a - self.row_count) * self.size_rect, 10 + i * self.size_rect // 3))

        blit_image('static/image/home.png', (50, 50), (20, 20))
        
        coords = ((x - self.otstup) // self.size_rect, (y - self.otstup) // self.size_rect)

        for x in range(self.column_count):
            for y in range(self.row_count):
                rect_paint = (self.otstup + x * self.size_rect, self.otstup + y * self.size_rect, self.size_rect, self.size_rect)

                if coords[0] == x and coords[1] == y and touth and self.mas[y][x] in (0, 1):
                    self.mas[y][x] = 1 - self.mas[y][x]
                elif coords[0] == x and coords[1] == y and not touth and self.mas[y][x] in (0, 2):
                    self.mas[y][x] = 2 - self.mas[y][x]

                if not 2 >= self.mas[y][x] >= 0:
                    self.mas[y][x] = 0

                if self.mas[y][x] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), rect_paint, self.size_rect)
                elif self.mas[y][x] == 2:
                    pygame.draw.line(screen, (0, 0, 0), (self.otstup + x * self.size_rect + 2,
                                                         self.otstup + y * self.size_rect + 2),
                                                        (self.otstup + x * self.size_rect + self.size_rect - 2,
                                                         self.otstup + y * self.size_rect + self.size_rect - 2), 5)
                    pygame.draw.line(screen, (0, 0, 0), (self.otstup + x * self.size_rect + self.size_rect - 2,
                                                         self.otstup + y * self.size_rect + 2),
                                                        (self.otstup + x * self.size_rect + 2,
                                                         self.otstup + y * self.size_rect + self.size_rect - 2), 5)
                    pygame.draw.rect(screen, (0, 0, 0), rect_paint, 1)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), rect_paint, 1)

        pygame.display.flip()

        if self.nums_to_lines(self.answer) == self.nums_to_lines(self.mas):
            class win(QWidget):
                def __init__(self):
                    super().__init__()
                    
                    sucsess = QMessageBox()
                    sucsess.setWindowTitle("Победа")
                    sucsess.setText(f"Вы решили этот уровень")
                    sucsess.setIcon(QMessageBox.Icon.Information)
                    sucsess.setStandardButtons(
                        QMessageBox.StandardButton.Ok
                    )
                    sucsess.exec()
            app = QApplication(sys.argv)
            ex = win()
            ex.show()

            if user.name:
                user.count += 1

                con = sqlite3.connect('static/db/gamers.db')
                cur = con.cursor()
                res = cur.execute(f"""SELECT password FROM users
                                      WHERE userid == {user.id}""").fetchall()
                cur.execute(f"""UPDATE users SET result = {user.count}
                                WHERE userid = '{user.id}'""").fetchall()
                con.commit()

            window = Main()
            pygame.display.set_caption('Главная')
            window.draw_window()

    def open_new_window(self, touth):
        global window
        if 20 < x < 70 and 20 < y < 70:
            window = Main()
            pygame.display.set_caption('Главная')
            window.draw_window()
        else:
            self.draw_window(x, y, touth)     


class Rules(Window):
    paper = 1

    def draw_window(self):
        screen.fill((153, 153, 255))

        blit_image('static/image/home.png', (50, 50), (20, 20))

        texts = [
            [33, 'Nonograms - это логические головоломки изображения,', (10, 200)],
            [33, 'в которых ячейки в сетке должны быть окрашены', (10, 240)],
            [33, 'или оставлены пустыми в соответствии с числами,', (10, 280)],
            [33, 'указанными сбоку сетки, чтобы показать скрытую картинку. ',  (10, 320)],
            [31, 'В этом типе головоломки числа измеряют количество', (10, 400)],
            [31, 'непрерывных линий закрашенных квадратов в каждой', (10, 440)],
            [31, 'строке или столбце.', (10, 480)]
        ]

        for elems in texts:
            blit_text(*elems)

        blit_image('static/image/next.png', (50, 50), (620, 620))

        pygame.display.flip()

    def draw_window1(self, image):
        screen.fill((153, 153, 255))

        blit_image('static/image/home.png', (50, 50), (20, 20))

        blit_text(50, 'Например', (250, 90))

        icons = [
            [image, (400, 400), (150, 150)],
            ['static/image/next.png', (50, 50), (620, 620)]
        ]
        
        for elems in icons:
            blit_image(*elems)

        pygame.display.flip()

    def draw_window2(self):
        screen.fill((153, 153, 255))

        blit_image('static/image/home.png', (50, 50), (20, 20))

        blit_text(50, 'УРА!', (300, 90))
        blit_text(40, 'Мы разобрали теорию игры', (170, 140))

        pygame.display.flip()

    def open_new_window(self):
        global window
        if 20 < x < 70 and 20 < y < 70:
            window = Main()
            pygame.display.set_caption('Главная')
            window.draw_window()
        if 620 < x < 670 and 620 < y < 670:
            if self.paper < 8:
                window.draw_window1([f'static/image/primer/{i}.png' for i in range(8)][self.paper])
                self.paper += 1
            else:
                window.draw_window2()


def rating(count):
    con = sqlite3.connect('static/db/gamers.db')
    cur = con.cursor()
    res = cur.execute(f"""SELECT result FROM users""").fetchall()
    return round(len([1 for i in res if i[0] < count]) / (len(res) - 1) * 100, 1)


def blit_text(size, text, coords):
    font = pygame.font.Font(None, size)
    rules = font.render(text, True, (0, 0, 0))
    screen.blit(rules, coords)


def blit_image(path, size, coords):
    all_sprites = pygame.sprite.Group()

    image = pygame.sprite.Sprite()
    image.image = pygame.transform.scale(pygame.image.load(path), size)
    image.rect = image.image.get_rect()
    image.rect.x, image.rect.y = coords
    all_sprites.add(image)

    all_sprites.draw(screen)


if __name__ == '__main__':
    

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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = window.get_coord(event.pos)
                if window.__class__.__name__ == 'Games':
                    if event.button == 1:
                        window.open_new_window(touth=True)
                    elif event.button == 3:
                        window.open_new_window(touth=False)
                else:
                    window.open_new_window()