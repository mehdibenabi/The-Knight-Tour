import pygame
from random import random, randint

# Constants
width, height = 700, 700
square_size = width // 8

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Knight Tour")
clock = pygame.time.Clock()


class Knight:
    moves = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

    def __init__(self, chromosome=None):
        self.position = (0, 0)
        self.path = [self.position]
        self.chromosome = chromosome if chromosome is not None else Chromosome()
        self.fitness = 0

    def move_forward(self, direction):
        x, y = self.position
        dx, dy = Knight.moves[direction]
        new_position = (x + dx, y + dy)
        if (
            new_position[0] > -1
            and new_position[0] < 8
            and new_position[1] > -1
            and new_position[1] < 8
            and (new_position not in self.path)
        ):
            self.path.append(new_position)
            self.position = new_position
            return True
        return False

    def move_backward(self, direction, i):
        new_move = 0
        for x in range(1, 7):
            new_move = (direction + x) % 8
            if self.move_forward(new_move):
                self.chromosome.genes[i] = new_move
                return True
        return False

    def check_moves(self):
        for x in range(63):
            if not self.move_forward(self.chromosome.genes[x]):
                if not self.move_backward(self.chromosome.genes[x], x):
                    break

    def evaluate_fitness(self):
        self.fitness = len(self.path)
        return self.fitness


class Chromosome:
    mutation_rate = 0.01

    def __init__(self, genes=None):
        self.genes = genes if genes is not None else self.random_genes()

    def random_genes(self):
        genes = []
        for _ in range(64):
            genes.append(randint(0, 7))
        return genes

    def cross_over(self, parent):
        child1 = self.genes[0:32] + parent.genes[32:63]
        child2 = self.genes[32:63] + parent.genes[0:32]
        return Chromosome(child1), Chromosome(child2)

    def mutate(self):
        for i in range(63):
            mutation_proba = random()
            if mutation_proba < Chromosome.mutation_rate:
                self.genes[i] = randint(0, 7)


class Population:
    def __init__(self, population_size, generation=1):
        self.population_size = population_size
        self.generation = generation
        self.knights = [Knight() for _ in range(self.population_size)]

    def check_population(self):
        for knight in self.knights:
            knight.check_moves()

    def evaluate(self):
        best_knight = None
        max_fit = 0
        for knight in self.knights:
            fit = knight.evaluate_fitness()
            if fit > max_fit:
                max_fit = fit
                best_knight = knight
        return max_fit, best_knight

    def tournament_selection(self, size):
        tournament = []
        for _ in range(size):
            X = randint(0, self.population_size - 1)
            tournament.append(self.knights[X])
        parent1 = None
        parent2 = None
        for knight in tournament:
            if parent1 is None or parent1.fitness < knight.fitness:
                parent2 = parent1
                parent1 = knight
            elif parent2 is None or parent2.fitness < knight.fitness:
                parent2 = knight

        return parent1, parent2

    def create_new_generation(self):
        new_population = []
        tournament_size = 10
        for i in range(self.population_size // 2):
            parent1, parent2 = self.tournament_selection(tournament_size)
            child1, child2 = parent1.chromosome.cross_over(parent2.chromosome)
            child1.mutate()
            child2.mutate()
            new_population.append(Knight(child1))
            new_population.append(Knight(child2))
        for knight in new_population:
            knight.chromosome.mutate()
        self.knights = new_population


def convert_coordinates(position):
    x, y = position
    return y * square_size, x * square_size


def draw_board():
    for row in range(8):
        for col in range(8):
            color = (200, 200, 200, 200) if (row + col) % 2 == 0 else (30, 30, 30, 255)
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


population_size = 50
population = Population(population_size)
num_gen = 0
running = True
step = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    population.check_population()
    max_fit, best_knight = population.evaluate()

    if max_fit == 64:
        screen.fill((0, 0, 0, 255))
        draw_board()

        if best_knight is not None:
            for position in best_knight.path:
                x, y = convert_coordinates(position)
               
                transparent_surface = pygame.Surface(
                    (square_size, square_size), pygame.SRCALPHA
                )  
                transparency = 100  
                pygame.draw.rect(
                    transparent_surface,
                    (0, 0, 255, transparency),  
                    (0, 0, square_size, square_size),
                ) 
                screen.blit(transparent_surface, (x, y))
                pygame.display.update()
                clock.tick(10)

            
            draw_knight(best_knight.path[-1])
        break

    num_gen += 1
    population.create_new_generation()

pygame.quit()
