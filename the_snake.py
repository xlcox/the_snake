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
ROTATIONS = {
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
DEFAULT_COLOR = (255, 255, 255)
SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

clock = pg.time.Clock()


class GameObject():
    """Класс, который является родительским для других классов."""

    def __init__(self, color=DEFAULT_COLOR):
        """Функция, отвечающая за инициализацию."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = color

    def fill_one_cell(self, position, color=None):
        """Функция, отвечающая за отрисовку одной ячейки."""
        color = color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self) -> None:
        """Функция, отвечающая за прорисовку объекта."""


class Apple(GameObject):
    """Класс, который описывает работу яблока."""

    def __init__(self, color=None, occ_positions=None):
        """Функция, отвечающая за инициализацию."""
        color = color or APPLE_COLOR
        super().__init__(color)
        self.randomize_position(occ_positions or [])
        self.draw()

    def draw(self) -> None:
        """Функция, отвечающая за отрисовку объекта."""
        self.fill_one_cell(self.position)

    def randomize_position(self, occ_positions) -> None:
        """Функция, отвечающая за изменение позиции."""
        while True:
            position = (choice(range(0, SCREEN_WIDTH, GRID_SIZE)),
                        choice(range(0, SCREEN_HEIGHT, GRID_SIZE)))
            if position not in occ_positions:
                self.position = position
                break


class Snake(GameObject):
    """Класс, который описывает работу змейки."""

    def __init__(self, color=None):
        """Функция, отвечающая за инициализацию."""
        color = color or SNAKE_COLOR
        super().__init__(color)
        self.reset()

    def update_direction(self, direction):
        """Функция, отвечающая за обновление направления."""
        self.direction = direction

    @property
    def head_position(self):
        """Функция, отвечающая за получение координат головы."""
        return self.positions[0]

    def draw(self):
        """Функция, отвечающая за отрисовку змейки и эффект движения."""
        self.fill_one_cell(self.head_position)
        if self.last:
            self.fill_one_cell(
                self.last,
                BOARD_BACKGROUND_COLOR
            )

    def move(self, grow=False):
        """Функция, отвечающая за движение змейки."""
        move_value_x = self.direction[0] * GRID_SIZE
        move_value_y = self.direction[1] * GRID_SIZE
        head_position_x, head_position_y = self.head_position

        new_head_position = (
            ((head_position_x + move_value_x) % SCREEN_WIDTH),
            ((head_position_y + move_value_y) % SCREEN_HEIGHT)
        )

        self.positions.insert(0, new_head_position)
        if not grow:
            self.last = self.positions.pop(-1)
        else:
            self.last = None

    def reset(self):
        """Функция, отвечающая за сброс позиции змейки."""
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None


def show_info(speed=SPEED, points=0):
    """Функция, отвечающая за изменение статистики окна."""
    text = f'Змейка | ESC для выхода | Cкорость: {speed} | Очки: {points}'
    pg.display.set_caption(text)


def handle_keys(game_object):
    """Функция, отвечающая за обработку состояния клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            new_direction = ROTATIONS.get((game_object.direction, event.key))
            if new_direction:
                game_object.update_direction(new_direction)
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main():
    """Главная функция для запуска программы."""
    pg.init()
    show_info()
    screen.fill(BOARD_BACKGROUND_COLOR)
    points = 0
    snake = Snake()
    apple = Apple(occ_positions=snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        grow = apple.position == snake.head_position
        snake.move(grow=grow)

        if grow:
            apple.randomize_position(snake.positions)
            apple.draw()
            points += 1
            show_info(points=points)
        elif snake.head_position in snake.positions[4::]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
            apple.draw()
            points = 0
            show_info()

        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
