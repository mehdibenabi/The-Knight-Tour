import pygame
import time


width, height = 700, 700
square_size = width // 8


pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Knight's Tour ")
clock = pygame.time.Clock()


class Knight:
    moves = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

    def __init__(self):
        self.position = (0, 0)  
        self.assignment = []  
        self.path = [self.position]  

    def move_forward(self, direction):
        x, y = self.position
        dx, dy = Knight.moves[direction - 1]
        new_position = (x + dx, y + dy)
        self.position = new_position
        self.path.append(new_position)

    def move_backward(self, direction):
        x, y = self.position
        dx, dy = Knight.moves[direction - 1]
        new_position = (x - dx, y - dy)
        self.position = new_position
        self.path.pop()

    def consistent(self, direction):
        x, y = self.position
        dx, dy = Knight.moves[direction - 1]
        new_position = (x + dx, y + dy)
        return (
            0 <= new_position[0] < 8 and
            0 <= new_position[1] < 8 and
            new_position not in self.path
        )

    def addMove(self, direction):
        if self.consistent(direction):
            self.assignment.append(direction)
            self.move_forward(direction)
            return True
        return False

    def removeMove(self):
        if self.assignment:
            direction = self.assignment.pop()
            self.move_backward(direction)
            return True
        return False

    def complete(self):
        return len(self.assignment) == 63  


def backtracking(knight):
    if knight.complete(): 
        return knight

    for direction in range(1, 9):  
        if knight.addMove(direction):
            result = backtracking(knight)  
            if result:  
                return result
            knight.removeMove()  

    return None  


def convert_coordinates(position):
    x, y = position
    return y * square_size, x * square_size


def draw_board():
    for row in range(8):
        for col in range(8):
            color = (200, 200, 200) if (row + col) % 2 == 0 else (30, 30, 30)
            pygame.draw.rect(
                screen,
                color,
                (col * square_size, row * square_size, square_size, square_size),
            )


def draw_knight(position):
    x, y = convert_coordinates(position)
    knight_image = pygame.image.load("knight.png")
    knight_image = pygame.transform.scale(knight_image, (square_size, square_size))
    knight_rect = knight_image.get_rect(
        center=(x + square_size // 2, y + square_size // 2)
    )
    screen.blit(knight_image, knight_rect)


def draw_step(path):
    for step, position in enumerate(path):
        draw_board()

        for past_position in path[:step]:
            x, y = convert_coordinates(past_position)
            pygame.draw.circle(
                screen,
                (0, 255, 0),
                (x + square_size // 2, y + square_size // 2),
                square_size // 4,
            )


        draw_knight(position)

        pygame.display.update()
        time.sleep(0.5)


if __name__ == "__main__":
    knight = Knight()

    knight_solution = backtracking(knight)

    if knight_solution:
        solution_path = knight_solution.path

        draw_step(solution_path)
    else:
        print("Aucune solution trouvée.")

    pygame.quit()
