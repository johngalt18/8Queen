import math
import random


class Individual:
    def __init__(self, chromosome=None):
        self.queen_len = 3
        self.chromosome_len = 24
        self.queens_number = 8
        self.grey = {'000': 0, '001': 1, '011': 2, '010': 3, '110': 4, '111': 5, '101': 6, '100': 7}
        if chromosome is None:
            random.seed()
            self.chromosome = str()
            for queen in range(self.chromosome_len):
                self.chromosome += str(random.randint(0, 1))
        else:
            self.chromosome = str(chromosome)

    def get_chromosome(self):
        return self.chromosome

    def visualisation(self):
        solution = str()
        visual = str()
        for horizontal in range(0, self.chromosome_len, self.queen_len):
            queen = self.chromosome[horizontal:horizontal+self.queen_len]
            solution += str(self.grey[queen])
        for cell in range(self.queens_number * self.queens_number):
            if cell % 8 == 0:
                visual += '\n'
            if cell % 8 == int(solution[cell // 8]):
                visual += 'Q'
            else:
                visual += '+'
        return visual

    def fitness_function(self):
        fitness = 0
        for ver in range(0, self.chromosome_len, self.queen_len):
            first_queen = self.chromosome[ver: ver + self.queen_len]
            for hor in range(0, self.chromosome_len, self.queen_len):
                second_queen = self.chromosome[hor: hor + self.queen_len]
                if hor != ver and self.grey[first_queen] == self.grey[second_queen]:
                    fitness += 1.0
                if hor != ver and (math.fabs(self.grey[first_queen] - self.grey[second_queen]) ==
                                       math.fabs(hor/self.queen_len - ver/self.queen_len)):
                    fitness += 1.0
        fitness = 8.0 - fitness / 8.0
        return fitness


class Solver_8_Queens:
    def __init__(self, pop_size=200, tournament_size=4, cross_prob=0.7, mut_prob=0.7):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        self.tournament_size = tournament_size
        self.population = [Individual() for ind in range(pop_size)]
        self.fitness_list = list()
        for ind in self.population:
            self.fitness_list.append(ind.fitness_function())

    def tournament_selection(self):
        parent_pool = list()
        for tour in range(self.pop_size):
            tour_pairs = [random.randrange(self.pop_size) for individual in range(self.tournament_size)]
            fitness = [self.fitness_list[individual] for individual in tour_pairs]
            individual_tour_winner = max(enumerate(fitness, 0), key=lambda individual_index: individual_index[1])[0]
            parent_pool.append(self.population[tour_pairs[individual_tour_winner]])
        return parent_pool

    def reproduce(self, parents):
        chromosome_len = self.population[0].chromosome_len
        next_generation = list()
        while len(next_generation) < len(self.population):
            first_cross_point, second_cross_point = random.randrange(chromosome_len), random.randrange(chromosome_len)
            first_parent, second_parent = random.randrange(self.pop_size), random.randrange(self.pop_size)
            while first_cross_point is second_cross_point or first_parent is second_parent:
                second_cross_point, second_parent = random.randrange(chromosome_len), random.randrange(self.pop_size)
            points = [first_cross_point, second_cross_point]
            if random.random() <= self.cross_prob:
                first_child = Individual(parents[first_parent].get_chromosome()[0:min(points)] +
                                         parents[second_parent].get_chromosome()[min(points):max(points)] +
                                         parents[first_parent].get_chromosome()[max(points):chromosome_len])
                second_child = Individual(parents[second_parent].get_chromosome()[0:min(points)] +
                                          parents[first_parent].get_chromosome()[min(points):max(points)] +
                                          parents[second_parent].get_chromosome()[max(points):chromosome_len])
            else:
                first_child, second_child = parents[first_parent], parents[second_parent]
            next_generation.append(first_child)
            next_generation.append(second_child)
        return next_generation

    def mutation(self, next_generation):
        chromosome_len = self.population[0].chromosome_len
        for ind in range(len(next_generation)):
            if random.random() <= self.mut_prob:
                mutated_bit = random.randrange(chromosome_len)
                if next_generation[ind].get_chromosome()[mutated_bit] is '0':
                    mutation = '1'
                    next_generation[ind] = Individual(next_generation[ind].get_chromosome()[0:mutated_bit] + mutation +
                                                      next_generation[ind].get_chromosome()[
                                                      mutated_bit + 1:chromosome_len])
                else:
                    mutation = '0'
                    next_generation[ind] = Individual(next_generation[ind].get_chromosome()[0:mutated_bit] + mutation +
                                                      next_generation[ind].get_chromosome()[
                                                      mutated_bit + 1:chromosome_len])
        return next_generation

    def best_fitness(self):
        best_fitness = max(self.fitness_list)
        best_individual = self.fitness_list.index(best_fitness)
        return best_fitness, best_individual

    def proceed(self):
        parents = self.tournament_selection()
        next_generation = self.reproduce(parents)
        next_generation = self.mutation(next_generation)
        self.population = next_generation
        for ind in range(len(self.population)):
            self.fitness_list[ind] = self.population[ind].fitness_function()

    def solve(self, min_fitness=7.9, max_epochs=None):
        best_fitness, best_individual = self.best_fitness()
        epochs_num = int()
        while (min_fitness is None or best_fitness < min_fitness) and (max_epochs is None or epochs_num < max_epochs):
            self.proceed()
            best_fitness, best_individual = self.best_fitness()
            epochs_num += 1
        visual = self.population[best_individual].visualisation()
        return best_fitness, epochs_num, visual

    
