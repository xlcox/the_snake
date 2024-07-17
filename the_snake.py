from random import choice
import pygame as pg


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTION_MAP = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}
BOARD_BACKGROUND_COLOR = (112, 112, 118)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill((112, 112, 118))
pg.display.set_caption('Змейка | Используйте ESC для выхода | Текущая скорость: ' + str(SPEED) + ' | Очки: 0')
clock = pg.time.Clock()


class GameObject():
    """Класс, который является родительским для других классов."""

    def __init__(self, color=None):
        """Функция, отвечающая за инициализацию."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = color

    def fill_one_cell(self, position, color=None, boarder_color=BORDER_COLOR):
        """Функция, отвечающая за отрисовку одной ячейки."""
        if color is None:
            color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, boarder_color, rect, 1)

    def draw(self) -> None:
        """Функция, отвечающая за прорисовку объекта."""


class Apple(GameObject):
    """Класс, который описывает работу яблока."""

    def __init__(self, color=APPLE_COLOR, occupied_pos=None):
        """Функция, отвечающая за инициализацию."""
        super().__init__(color)
        self.on_board = False

    def draw(self, occupied_pos=(320, 240)) -> None:
        """Функция, отвечающая за отрисовку объекта."""
        if not self.on_board:
            self.randomize_position(occupied_pos)
            self.fill_one_cell(self.position, self.body_color)
            self.on_board = True

    def randomize_position(self, occupied_pos) -> None:
        """Функция, отвечающая за изменение позиции."""
        while True:
            random_x = choice(range(0, SCREEN_WIDTH, GRID_SIZE))
            random_y = choice(range(0, SCREEN_HEIGHT, GRID_SIZE))
            if (random_x, random_y) not in occupied_pos:
                self.position = (random_x, random_y)
                break


class Snake(GameObject):
    """Класс, который описывает работу змейки."""

    def __init__(self, color=SNAKE_COLOR):
        """Функция, отвечающая за инициализацию."""
        super().__init__(color)
        self.reset()

    def update_direction(self, direction):
        """Функция, отвечающая за обновление направления."""
        self.direction = direction

    @property
    def get_head_position(self):
        """Функция, отвечающая за получение координат головы."""
        return self.positions[0]

    def draw(self):
        """Функция, отвечающая за отрисовку змейки и эффект движения."""
        self.fill_one_cell(self.get_head_position, self.body_color)
        if self.last:
            self.fill_one_cell(self.last, BOARD_BACKGROUND_COLOR, BOARD_BACKGROUND_COLOR)

    def move(self, increase=False):
        """Функция, отвечающая за движение змейки."""
        move_value_x = self.direction[0] * GRID_SIZE
        move_value_y = self.direction[1] * GRID_SIZE
        head_position_x, head_position_y = self.get_head_position
        new_head_position_x = (head_position_x + move_value_x) % SCREEN_WIDTH
        new_head_position_y = (head_position_y + move_value_y) % SCREEN_HEIGHT
        new_head_position = (new_head_position_x, new_head_position_y)
        self.positions.insert(0, new_head_position)
        self.last = self.positions[-1]
        self.positions.pop(-1)

    def increase_len(self):
        """Функция, отвечающая за увеличение длины змейки."""
        tail_x = self.positions[-1][0] - self.direction[0] * GRID_SIZE
        tail_y = self.positions[-1][1] - self.direction[1] * GRID_SIZE
        self.positions.append((tail_x, tail_y))

    def reset(self):
        """Функция, отвечающая за сброс позиции змейки."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.positions = [self.position]
        self.direction = LEFT
        self.last = None


def change_statistic(speed=SPEED, points=0):
    """Функция, отвечающая за изменение статистики окна."""
    pg.display.set_caption(
        'Змейка | Используйте ESC для выхода | Текущая скорость: ' +
        str(speed) +
        ' | Очки: ' +
        str(points)
    )


def handle_keys(game_object):
    """Функция, отвечающая за обработку состояния клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            current_direction = game_object.direction
            key_pressed = event.key
            if (current_direction, key_pressed) in DIRECTION_MAP:
                game_object.direction = DIRECTION_MAP[(current_direction, key_pressed)]
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main():
    """Главная функция для запуска программы."""
    points = 0
    pg.init()
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if apple.position == snake.get_head_position:
            apple.on_board = False
            snake.increase_len()
            points += 1
            change_statistic(points=points)

        if snake.get_head_position in snake.positions[4::]:
            apple.on_board = False
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            points = 0
            change_statistic()

        snake.draw()
        apple.draw(snake.positions)
        pg.display.update()


if __name__ == '__main__':
    main()
