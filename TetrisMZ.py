import random  # Импорт библиотеки для случайных событий
import sys
import time

import pygame as pg
from pygame.locals import *

pg.display.set_caption("aaa") 
icon = pg.image.load("aaa.jpg")
pg.display.set_icon(icon)

'''
Константы:
    FPS - Кадровая частота
    WINDOW_WIDTH - Ширина окна программы
    WINDOW_HEIGHT - Высота окна программы
    block - Размер заготовки для фигуры в пикселях
    GAME_AREA_HEIGHT - Высота игрового поля
    GAME_AREA_WIDTH - Ширина Игрового поля
    SIDE_FACTOR - Множитель ускорения при движении в сторону
    DOWN_FACTOR - Множитель ускорения при движении вниз
    GAME_AREA_MARGIN_RIGHT_LEFT - Расстояние справа и слева от окна программы для игрового поля (Отступ)
    GAME_AREA_MARGIN_RIGHT_LEFT - Расстояние сверху и снизу от окна программы для игрового поля (Отступ)
    COLORS - Кортеж цветов для фигур
    LIGHT_COLORS - Кортеж цветов для фигур (Более светлые цвета для создания псевдо 2.5D эффекта)
    WHITE - Белый цвет
    GRAY - Серый цвет
    BLACK - Чёрный цвет
    BRD_COLOR - Цвет рамки игрового поля
    BG_COLOR - Цвет фона
    TXT_COLOR - Цвет текста
    TITLE_COLOR - Цвет названия
    INFO_COLOR - Цвет для текста с информацией
    FIG_W - Ширина заготовки в квадратах ( 1 квадрат - 4 пикселя)
    FIG_H - Высота заготовки в квадратах ( 1 квадрат - 4 пикселя)
    EMPTY - Символ для обозначения пустоты в фигуре ( на месте этого пикселя ничего нет)
    FIGURES - Все возможные варианты поворотов фигур 
Функции:
    
'''
FPS = 100  # Кадровая частота
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 500  # Высота и ширина окна программы
block, GAME_AREA_HEIGHT, GAME_AREA_WIDTH = 20, 20, 10  # Размер заготвоки для фигур в пикселях, высота и ширина игрового поля

SIDE_FACTOR, DOWN_FACTOR = 0.15, 0.1  # Множитель ускорения для передвижения в сторону и вниз

GAME_AREA_MARGIN_RIGHT_LEFT = int(
    (WINDOW_WIDTH - GAME_AREA_WIDTH * block) / 2)  # Расстояние справа и слева от окна программы для игрового поля
GAME_AREA_MARGIN_TOP_DOWN = WINDOW_HEIGHT - (
        GAME_AREA_HEIGHT * block) - 5  # Расстояние сверху и вниз от окна программы для игрового поля

COLORS = (
    (0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))  # Цвета для падающих блоков: синий, зеленый, красный, желтый
LIGHT_COLORS = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (
    255, 255,
    30))  # Более светлые цвета для падающих блоков: светло-синий, светло-зеленый, светло-красный, светло-желтый

WHITE, GRAY, BLACK = (255, 255, 255), (185, 185, 185), (0, 0, 0)  # Белый, серый и чёрный цвета
BRD_COLOR, BG_COLOR, TXT_COLOR, TITLE_COLOR, INFO_COLOR = WHITE, (36,22,49), WHITE, (139, 0, 255), (255,86,59)  # Константы для обозначения цвета рамки игрового поля, цвета фона окна, цвета текста, цвет надписи, цвет информации

FIG_W, FIG_H = 5, 5  # Размер заготовки в квадратах: ширина и высота соответственно ( 1 квадрат - 4 пикселя)
EMPTY = 'o'  # Символ для обозначения пустоты в фигуре ( на месте этого пикселя ничего нет)

FIGURES = {'S': [['ooooo',
                  'ooooo',
                  'ooxxo',
                  'oxxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxxo',
                  'oooxo',
                  'ooooo']],
           'Z': [['ooooo',
                  'ooooo',
                  'oxxoo',
                  'ooxxo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'oxxoo',
                  'oxooo',
                  'ooooo']],
           'J': [['ooooo',
                  'oxooo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxxo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'oooxo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxoo',
                  'oxxoo',
                  'ooooo']],
           'L': [['ooooo',
                  'oooxo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxoo',
                  'ooxxo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'oxooo',
                  'ooooo'],
                 ['ooooo',
                  'oxxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo']],
           'I': [['ooxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'xxxxo',
                  'ooooo',
                  'ooooo']],
           'O': [['ooooo',
                  'ooooo',
                  'oxxoo',
                  'oxxoo',
                  'ooooo']],
           'T': [['ooooo',
                  'ooxoo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxxo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'oxxoo',
                  'ooxoo',
                  'ooooo']]}
# Все возможные варианты поворотов фигур


'''
Функция для вызова паузы в игре (Полупрозрачная заставка):
    Создание дополнительной поверхности с попиксельным альфа-смешением,
    Эаливка экрана паузы цветом
    Наложение доп поверхности на поверхность окна игры
'''


def showPauseScreen():
    pause = pg.Surface((600, 500), pg.SRCALPHA)  # Создание дополнительной поверхности с попиксельным альфа-смешением
    pause.fill((255,86,59, 80))  # Эаливка экрана паузы цветом
    display_surf.blit(pause, (0, 0))  # Наложение на поверхность окна игры


'''
Точка входа программы:
    Ввод дополонительных констант,
    Рендериг окна
    Запуск игры
'''


def main():
    global fps_clock, display_surf, FONT, LARGE_FONT
    pg.init()  # Инициализация модуля, отрисовка стартового окна
    fps_clock = pg.time.Clock()  #
    display_surf = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Отрисовка стартового окна
    display_surf.fill(BG_COLOR)
    FONT = pg.font.SysFont('arial', 20)  # Шрифт
    LARGE_FONT = pg.font.SysFont('verdana', 45)  # Шрифт
    pg.display.set_caption('MonaZhiga\'s Tetris')  # Название
    showText('MonaZhiga\'s Tetris')  # Отрисовка текста

    while True:  # Основная логика
        runTetris()
        showPauseScreen()  # Если программа дошла до этой строки, то игра закончена, отобразить паузу
        showText('GAME OVER')  # Отрисовка текста


'''
Точка входа программы:
    Ввод дополонительных констант,
    Рендериг окна
    Запуск игры
'''


def runTetris():
    area = getEmptyArea()  # Инициализация пустого игрового поля
    last_move_down = time.time()
    last_side_move = time.time()
    last_fall = time.time()

    # Состояние нашей фигуры:
    going_down = False  # Движется ли фигура вниз
    going_left = False  # Движется ли фигура влево
    going_right = False  # Движется ли фигура вправо
    points = 0  # Очки

    level, fall_speed = calcSpeed(points)  # Вычисление скорости движения фигуры, основываясь на очках
    fallingFig = getNewFig()  # Получение падающей фигуры
    nextFig = getNewFig()  # Получение следующей фигуры (Для обозначения справа от игрового поля)

    while True:
        if fallingFig == None:
            # если в игре нет падающих фигурок
            fallingFig = nextFig  # Следующай фигура, становится падающей
            nextFig = getNewFig()  # Создается новая фигура, которая будет следующей
            last_fall = time.time()

            if not checkPos(area, fallingFig):
                return  # если на игровом поле нет свободного места - игра закончена

        checkIsGameOver()  # Проверка, завершена ли игра

        # Если пользователь взаимодействует с программой:
        for event in pg.event.get():
            if event.type == KEYUP:  # Если клавиша отжата ( Клавиша вернулась в исходное состояние после нажатия)
                if event.key == K_SPACE:  # Если пользователь нажал на пробел
                    showPauseScreen()  # Ставим игру на паузу
                    showText('Пауза')  # Рендеринг текста
                    last_fall = time.time()
                    last_move_down = time.time()
                    last_side_move = time.time()
                elif event.key == K_LEFT:  # Если клавиша вернулась в исходное состояние, и этта клавиша движение влево
                    going_left = False  # Фигура больше не двигается влево
                elif event.key == K_RIGHT:  # Аналогично для движения вправо
                    going_right = False
                elif event.key == K_DOWN:  # Аналогично для движения вниз
                    going_down = False

            elif event.type == KEYDOWN:  # Если клавиша была нажата, и еще не вернулась в исходное состояние
                if event.key == K_LEFT and checkPos(area, fallingFig,
                                                    adjX=-1):  # Если фигура движется влево (нажата клавиша движения влево), и слева фигуры есть место
                    fallingFig['x'] -= 1  # Изменяем координату х на 1 , сдвиг влево
                    going_left = True  # Выставляем статус фигуры, что она движется влево
                    going_right = False
                    last_side_move = time.time()

                elif event.key == K_RIGHT and checkPos(area, fallingFig,
                                                       adjX=1):  # Если фигура движется вправо и справа есть место
                    fallingFig['x'] += 1  # Сдвиг вправо
                    going_right = True  # Фигура движется вправо
                    going_left = False
                    last_side_move = time.time()


                elif event.key == K_UP:  # Если нажата стрелка вверх
                    fallingFig['rotation'] = (fallingFig['rotation'] + 1) % len(
                        FIGURES[fallingFig['shape']])  # Поворт фигуры на 90 градусов.
                    if not checkPos(area,
                                    fallingFig):  # Если места для поворота нету, возвращаем в предыдущее состояние
                        fallingFig['rotation'] = (fallingFig['rotation'] - 1) % len(FIGURES[fallingFig['shape']])

                # Ускорение падения фигуры
                elif event.key == K_DOWN:  # Если нажата стрелка вниз
                    going_down = True  # Выставляем состояние, что фигура падает вниз с ускорением
                    if checkPos(area, fallingFig, adjY=1):  # если есть место, куда падать
                        fallingFig['y'] += 1  # Меняем координату фигуры на 1
                    last_move_down = time.time()

                # Мгновенный сброс фигуры
                elif event.key == K_RETURN:  # Если нажата клавиша Enter
                    going_down = False
                    going_left = False
                    going_right = False

                    # Определяем координату i, отвечающая за высоту, где нет пустот, т.е высота (координата у), на которой находится фигура или конец игрового поля
                    for i in range(1, GAME_AREA_HEIGHT):
                        if not checkPos(area, fallingFig, adjY=i):
                            break  # Как только определили эту координату, выходим из цикла
                    fallingFig[
                        'y'] += i - 1  # Наша фигура будет выше пола/фигуры, соотв. вычисляем один из координаты i

        # Удержание клавиш
        if (
                going_left or going_right) and time.time() - last_side_move > SIDE_FACTOR:  # Если мы движемся влево или вправо и удерживаем клавишу, больше чем то время, которое нужно для перемещния фигуры в сторону
            if going_left and checkPos(area, fallingFig, adjX=-1):  # Если движемся влево и слева есть место
                fallingFig['x'] -= 1  # Уменьшаем координату, сдвиг влево
            elif going_right and checkPos(area, fallingFig, adjX=1):  # Если движемся вправо и справа есть место
                fallingFig['x'] += 1  # Увеличиваем координату, сдвиг вправо
            last_side_move = time.time()  # Обновляем время, когда мы подвинулись в сторону (для расчета условий в 288 строке)

        if going_down and time.time() - last_move_down > DOWN_FACTOR and checkPos(area, fallingFig,
                                                                                  adjY=1):  # Аналогично для движения вниз
            fallingFig['y'] += 1
            last_move_down = time.time()

        if time.time() - last_fall > fall_speed:  # Если прошло время, за которое фигура должна была упасть на единицу пути
            if not checkPos(area, fallingFig, adjY=1):  # Если фигура приземлилась
                addToGameArea(area, fallingFig)  # Добавляем фигуру как статичный объект на поле игры
                points += clearCompleted(area)  # Добавляем очки, основываясь  на том, сколько было удалено линий
                level, fall_speed = calcSpeed(points)  # Производим перерасчёт уровня и скорости с новым кол-вом очков
                fallingFig = None  # Убираем падающую фигуру, т.к она упала
            else:  # Если фигура еще не приземлилась
                fallingFig['y'] += 1  # Увеличиваем координату
                last_fall = time.time()  # Обновляем время, чтобы заново рассчитать по формуле

        # Рендеринг окна игры, надписей и т.д
        display_surf.fill(BG_COLOR)  # Установить фон для игры
        drawTitle()  # Отображение названия
        drawGameArea(area)  # Отображение игрового поля
        drawInfo(points, level) # Отображение информации
        drawnextFig(nextFig) # Отрисовка превью след. фигуры
        if fallingFig != None: # Если фигуры нет,
            drawFig(fallingFig) # Отрисовать фигуру
        pg.display.update() # Отрисовываем все заново, с учетом фпс
        fps_clock.tick(FPS)


def txtObjects(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

# Останавливаем игру
def stopGame():
    pg.quit()
    sys.exit()

# Функция, проверяющая была ли нажата какая-то клавиша (в начале игры)
def checkKeys():
    checkIsGameOver() # Если игра окончена, то выходим

    for event in pg.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN: # Есла клавиша не отжата - не вернулась в исходное положение, после того, как её нажали
            continue
        return event.key # Нажата - возвращаем клавишу, которая была нажата
    return None # Не нажата

# Показ текста
def showText(text):
    titleSurf, titleRect = txtObjects(text, LARGE_FONT, TITLE_COLOR) # Текст
    titleRect.center = (int(WINDOW_WIDTH / 2) - 3, int(WINDOW_HEIGHT / 2) - 3) # Центрирование текста
    display_surf.blit(titleSurf, titleRect) # Отрисовка

    pressKeySurf, pressKeyRect = txtObjects('Нажмите любую клавишу, чтобы начать игру', FONT, WHITE) # Текст
    pressKeyRect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2) + 100) # Центрирование текста
    display_surf.blit(pressKeySurf, pressKeyRect) # Отрисовка

    while checkKeys() == None: # Пока ничего не нажато ( начало игры), ждёмс
        pg.display.update()
        fps_clock.tick()


# Функция, отвечающая за выход из игры
def checkIsGameOver():
    for event in pg.event.get(QUIT):  # проверка всех событий, приводящих к выходу из игры
        stopGame() # Останавливаем игру
    for event in pg.event.get(KEYUP): # Если нажата клавиша остановки игры
        if event.key == K_ESCAPE:
            stopGame() # Останавливаем игру
        pg.event.post(event)


# Функция, вычисляющая скорость, основываясь на заработанных очках
def calcSpeed(points):
    level = int(
        points / 10) + 1  # Условный уровень сложности, увеличивающийся с каждым десятком очков: 1 уровень для 0-9, 2 уровень для 10-19 и т.д.
    fall_speed = 0.27 - (level * 0.02)  # Скорость, с которой падает фигура, вычисляемая на основе уровня
    return level, fall_speed


# Функция, отвечающая за появление новой фигуры в игре
def getNewFig():
    # Новая фигура со случайным цветом и углом поворота
    shape = random.choice(list(FIGURES.keys()))  # Случайная фигура
    newFigure = {'shape': shape,
                 'rotation': random.randint(0, len(FIGURES[shape]) - 1),  # Случайная позиция фигуры (её поворот)
                 'x': int(GAME_AREA_WIDTH / 2) - int(FIG_W / 2),  # Координата х появляющейся фигуры
                 'y': -2,  # Координата у появляющейся фигуры (фиксированная)
                 'color': random.randint(0, len(COLORS) - 1)}  # Случайный цвет
    return newFigure

# Добавляем в игровую область фигуру
def addToGameArea(area, fig):
    for x in range(FIG_W):
        for y in range(FIG_H):
            if FIGURES[fig['shape']][fig['rotation']][y][x] != EMPTY: # Если не пустота
                area[x + fig['x']][y + fig['y']] = fig['color'] # Обозначем фигуру


'''
Функция, возвращающая пустую игровую область для начала игры 
'''
def getEmptyArea():
    area = []
    for i in range(GAME_AREA_WIDTH):
        area.append([EMPTY] * GAME_AREA_HEIGHT)  # Заполняем всю игровую область невидимыми символами (пустотой)
    return area


# Находится ли указанная точка (х, у) внутри игровой области
def isInArea(x, y):
    return 0 <= x < GAME_AREA_WIDTH and y < GAME_AREA_HEIGHT


# Функция, проверяющая, находится ли фигура в границах игрового поля, не сталкиваясь с другими фигурами
def checkPos(area, fig, adjX=0, adjY=0):
    for x in range(FIG_W):
        for y in range(FIG_H):
            abovearea = y + fig['y'] + adjY < 0
            if abovearea or FIGURES[fig['shape']][fig['rotation']][y][
                x] == EMPTY:  # Если фигура над игровой областью ( только заспавнилась) или в провер. позиции фигуры нет как таковой (пустота)
                continue  # Просто продолжаем
            if not isInArea(x + fig['x'] + adjX, y + fig[
                'y'] + adjY):  # Если фигура не находится внутри игровой области (кроме верха игровой области, его не считаем, т.к там спавнится фигура)
                return False  # Возвращаем False - нет, фигура не в игровой области
            if area[x + fig['x'] + adjX][
                y + fig['y'] + adjY] != EMPTY:  # Если в позиции, которую мы проверяем, есть что-то кроме пустоты
                return False  # Возвращаем False - нет, фигура сталкивается с чем-то
    return True


# Функция, проверяющая наличие полностью заполненных рядов
def isCompleted(area, y):
    for x in range(GAME_AREA_WIDTH):
        if area[x][y] == EMPTY:
            return False  # Если найдётся хоть одна пустота, то возвращаем False - ряд не завершён
    return True  # Если пустот нет, возращаем True - ряд завершён


# Если есть заполненные ряды удалить их, и вернуть кол-во удалленых рядов
def clearCompleted(area):
    removed_lines = 0  # Сколько было удалено рядов
    y = GAME_AREA_HEIGHT - 1
    while y >= 0:  # Пока, мы не дошли до конца поля
        if isCompleted(area, y):  # Если данный ряд с данной координатой завершен (нету пустоты), то
            for pushDownY in range(y, 0, -1):  # Все блоки, наход. сверху, сдвигаем вниз на 1
                for x in range(GAME_AREA_WIDTH):
                    area[x][pushDownY] = area[x][pushDownY - 1]
            for x in range(GAME_AREA_WIDTH):
                area[x][0] = EMPTY  # Заполняем самую верхную строку пустотой
            removed_lines += 1  # Увелеченик кол-ва удаленных рядов
        else:
            y -= 1
    return removed_lines


# Функция для конвертирования координат
def convertCoords(block_x, block_y):
    return (GAME_AREA_MARGIN_RIGHT_LEFT + (block_x * block)), (GAME_AREA_MARGIN_TOP_DOWN + (block_y * block))


# Отрисовка квадратных блоков, из которых состоят фигуры
def drawBlock(block_x, block_y, color, pixelx=None, pixely=None):
    if color == EMPTY:  # Если цвета нет, то ничего не отрисовываем
        return
    if pixelx is None and pixely is None:  # Если в параметрах не даны пиксели, конвертируем их на основе писелей, заложенных в самой фигуре
        pixelx, pixely = convertCoords(block_x, block_y)
    pg.draw.rect(display_surf, COLORS[color], (pixelx + 1, pixely + 1, block - 1, block - 1), 0,
                 3)  # Отрисовываем основной блок
    pg.draw.rect(display_surf, LIGHT_COLORS[color], (pixelx + 1, pixely + 1, block - 4, block - 4), 0,
                 3)  # Отрисовываем еле видимый квадрат внутри блока, для эффекта 2.5 D
    pg.draw.circle(display_surf, COLORS[color], (pixelx + block / 2, pixely + block / 2),
                   5)  # Отрисовываем круг внутри фигуры для эффекта 2.5 D


# Отрисовка игрового поля
def drawGameArea(area):
    # граница игрового поля
    pg.draw.rect(display_surf, BRD_COLOR, (
        GAME_AREA_MARGIN_RIGHT_LEFT - 4, GAME_AREA_MARGIN_TOP_DOWN - 4, (GAME_AREA_WIDTH * block) + 8,
        (GAME_AREA_HEIGHT * block) + 8),
                 5)

    # Отрисовка фона игрового поля
    pg.draw.rect(display_surf, BG_COLOR, (
        GAME_AREA_MARGIN_RIGHT_LEFT, GAME_AREA_MARGIN_TOP_DOWN, block * GAME_AREA_WIDTH, block * GAME_AREA_HEIGHT))

    # Отрисовка блоков внутри игрового поля
    for x in range(GAME_AREA_WIDTH):
        for y in range(GAME_AREA_HEIGHT):
            drawBlock(x, y, area[x][y])


# Функция для отрисовки названия игры
def drawTitle():
    titleSurf = LARGE_FONT.render(' MZ\'s Tetris', True, TITLE_COLOR)  # Создаем надпись
    titleRect = titleSurf.get_rect()  # Прямоугольник вокруг надписи, устанавливаем соотв. отступы, чтобы выглядело красиво
    titleRect.topleft = (WINDOW_WIDTH - 425, 20)
    titleRect.topleft = (WINDOW_WIDTH - 425, 20)
    display_surf.blit(titleSurf, titleRect)  # Отрисовка


# Функция для отрисовки информации об игре
def drawInfo(points, level):
    pointsSurf = FONT.render(f'Очков: {points}', True, TXT_COLOR)  # Создаем надпись
    pointsRect = pointsSurf.get_rect()  # Прямоугольник вокруг надписи, устанавлиаем соотв. отсутпы
    pointsRect.topleft = (WINDOW_WIDTH - 550, 180)
    display_surf.blit(pointsSurf, pointsRect)  # Отрисовка

    levelSurf = FONT.render(f'Уровень: {level}', True, TXT_COLOR)  # Создаем надпись
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOW_WIDTH - 550, 250)  # Прямоугольник вокруг надписи, устанавлиаем соотв. отсутпы
    display_surf.blit(levelSurf, levelRect)  # Отрисовка

    pausebSurf = FONT.render('Пауза: пробел', True, INFO_COLOR)  # Создаем надпись
    pausebRect = pausebSurf.get_rect()
    pausebRect.topleft = (WINDOW_WIDTH - 550, 420)  # Прямоугольник вокруг надписи, устанавлиаем соотв. отсутпы
    display_surf.blit(pausebSurf, pausebRect)  # Отрисовка

    escbSurf = FONT.render('Выход: Esc', True, INFO_COLOR)  # Создаем надпись
    escbRect = escbSurf.get_rect()
    escbRect.topleft = (WINDOW_WIDTH - 550, 450)  # Прямоугольник вокруг надписи, устанавлиаем соотв. отсутпы
    display_surf.blit(escbSurf, escbRect)  # Отрисовка


# Функция для отрисовки фигуры
def drawFig(fig, pixelx=None, pixely=None):
    figToDraw = FIGURES[fig['shape']][fig['rotation']]  # Настройи фигуры: сама фигура и её поворот
    if pixelx is None and pixely is None:  # Если координаты фигуры не заданы в параметрах, используем координаты самой фигуры, заложенные внутри нее, конвертировав их
        pixelx, pixely = convertCoords(fig['x'], fig['y'])

    # отрисовка элементов фигур
    for x in range(FIG_W):
        for y in range(FIG_H):
            if figToDraw[y][x] != EMPTY:  # Если не пустота, а часть фигуры, то отрисовывем на экране
                drawBlock(None, None, fig['color'], pixelx + (x * block), pixely + (y * block))


# Функция, для отрисовки следующей фигуры (превью справа от зоны игры)
def drawnextFig(fig):  # превью следующей фигуры
    nextSurf = FONT.render('Следующая:', True, TXT_COLOR)  # Создаем надпись
    nextRect = nextSurf.get_rect()  # Прямоугольник вокруг надписи, устанавлиаем соотв. отсутпы
    nextRect.topleft = (WINDOW_WIDTH - 150, 180)
    display_surf.blit(nextSurf, nextRect)  # Отрисовка надписи
    drawFig(fig, pixelx=WINDOW_WIDTH - 150, pixely=230)  # Отрисовка превью фигуры


main()
