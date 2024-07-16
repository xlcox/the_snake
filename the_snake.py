from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Класс, который является родительским для других классов."""

    def __init__(self):
        """Функция, отвечающая за инициализацию."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self) -> None:
        """Функция, отвечающая за прорисовку объекта."""
        pass


class Apple(GameObject):
    """Класс, который описывает работу яблока."""

    def __init__(self):
        """Функция, отвечающая за инициализацию."""
        super().__init__()
        self.body_color = APPLE_COLOR

    def draw(self) -> None:
        """Функция, отвечающая за отрисовку объекта."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self) -> None:
        """Функция, отвечающая за изменение позиции."""
        random_x = choice(range(0, SCREEN_WIDTH, GRID_SIZE))
        random_y = choice(range(0, SCREEN_HEIGHT, GRID_SIZE))
        self.position = (random_x, random_y)


class Snake(GameObject):
    """Класс, который описывает работу змейки."""

    def __init__(self):
        """Функция, отвечающая за инициализацию."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [self.position]
        self.direction = LEFT
        self.last = None
        self.next_direction = None

    def update_direction(self):
        """Функция, отвечающая за обновление направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    @property
    def get_head_position(self):
        """Функция, отвечающая за получение координат головы."""
        return self.positions[0]

    def draw(self):
        """Функция, отвечающая за отрисовку змейки и эффект движения."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Функция, отвечающая за движение змейки."""
        self.last = self.positions[-1]
        move_value_x = self.direction[0] * 20
        move_value_y = self.direction[1] * 20
        head_position = self.get_head_position
        if head_position[0] < 0:
            tail_cords = (SCREEN_WIDTH + move_value_x, head_position[1] + move_value_y)
            self.positions.insert(0, tail_cords)
        elif head_position[1] < 0:
            tail_cords = (head_position[0] + move_value_x, SCREEN_HEIGHT + move_value_y)
            self.positions.insert(0, tail_cords)
        elif head_position[0] > SCREEN_WIDTH:
            tail_cords = (0, head_position[1] + move_value_y)
            self.positions.insert(0, tail_cords)
        elif head_position[1] > SCREEN_HEIGHT:
            tail_cords = (head_position[0] + move_value_x, 0)
            self.positions.insert(0, tail_cords)
        else:
            tail_cords = (head_position[0] + move_value_x, head_position[1] + move_value_y)
            self.positions.insert(0, tail_cords)
        self.positions.pop(-1)

    def reset(self):
        """Функция, отвечающая за сброс позиции змейки."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.positions = [self.position]
        self.direction = LEFT
        self.last = None
        self.next_direction = None


def handle_keys(game_object):
    """Функция, отвечающая за обработку состояния клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            game_object.update_direction()


def main():
    """Главная функция для запуска программы."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        snake.move()
        handle_keys(snake)
        pygame.display.update()

        if apple.position == snake.positions[0]:
            apple.randomize_position()
            tail_x = snake.positions[-1][0] - snake.direction[0] * 20
            tail_y = snake.positions[-1][1] - snake.direction[1] * 20
            snake.positions.append((tail_x, tail_y))

        if snake.positions[0] in snake.positions[1::]:
            snake.reset()


if __name__ == '__main__':
    main()
