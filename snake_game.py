
import pygame
import random

# Размер окна
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Размер клетки сетки
GRID_SIZE = 20

# Количество клеток по горизонтали и вертикали
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Направления движения змейки
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 body_color=(255, 255, 255)):
        """Инициализация базовых атрибутов."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод отрисовки (переопределяется в наследниках)."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Инициализация яблока со случайной позицией."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Задаёт случайную позицию яблоку в пределах поля."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self, surface):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self):
        """Инициализация начальных параметров змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения, если выбрано новое."""
        if self.next_direction:
            # запрещаем обратное движение
            opposite = (-self.direction[0], -self.direction[1])
            if self.next_direction != opposite:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в выбранном направлении."""
        cur_x, cur_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_pos = (
            (cur_x + (dir_x * GRID_SIZE)) % SCREEN_WIDTH,
            (cur_y + (dir_y * GRID_SIZE)) % SCREEN_HEIGHT,
        )

        # Проверка столкновения с собой
        if new_pos in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_pos)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку и очищает след."""
        if self.last:
            rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)
        for pos in self.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)

    def reset(self):
        """Сбрасывает состояние змейки до начального."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш игрока."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона 🐍')

    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    # Очистка экрана
    screen.fill(BOARD_BACKGROUND_COLOR)
    pygame.display.update()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка «съедания» яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

        clock.tick(20)  # скорость игры


if __name__ == '__main__':
    main()
