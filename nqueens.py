import math
import random
import numpy


class Individual:
    def __init__(self, chrome=None):
        self.chromosome_len = 24
        self.queens_number = 8
        self.queen_len = 3
        if chrome is None:
            self.chromosome = ''
            for vertical in range(self.queens_number):
                for bit_number in range(self.queen_len):
                    bit = random.randint(0, 1)
                    self.chromosome += str(bit)
        else:
            self.chromosome = str(chrome)

    def get_chrome(self):
        return self.chromosome

    def fitness_function(self):
        fitness_sum = 0
        for ver in range(0, self.chromosome_len, self.queen_len):
            first_queen = self.chromosome[ver: ver + self.queen_len]
            for hor in range(0, self.chromosome_len, self.queen_len):
                second_queen = self.chromosome[hor: hor + self.queen_len]
                if first_queen == second_queen and ver != hor:
                    fitness_sum += 1
                if ver != hor and (math.fabs(int(first_queen, 2) - int(second_queen, 2)) ==
                                   math.fabs(hor / self.queen_len - ver / self.queen_len)):
                    fitness_sum += 1
        fitness_sum = 8 - fitness_sum / 8
        return fitness_sum

    def visualisation(self):
        solution = str()
        visual = str()
        for horizontal in range(0, self.chromosome_len, self.queen_len):
            queen = self.chromosome[horizontal:horizontal + self.queen_len]
            solution += str(int(queen, 2))
        for cell in range(self.queens_number * self.queens_number):
            if cell % 8 == 0:
                visual += '\n'
            if cell % 8 == int(solution[cell // 8]):
                visual += 'Q'
            else:
                visual += '+'
        return visual


class Solver_8_queens:
    def __init__(self, pop_size=100, cross_prob=0.7, mut_prob=0.25):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        self.population = [Individual() for i in range(pop_size)]
        self.fitness_list = list()
        for ind in self.population:
            self.fitness_list.append(ind.fitness_function())

    def roulette_wheel(self):
        probability = list()
        ind_position = [i for i in range(self.pop_size)]
        fitness_sum = float()
        parents = list()
        for ind in self.fitness_list:
            fitness_sum += ind

        for i in self.fitness_list:
            choose_chance = i / fitness_sum
            probability.append(choose_chance)

        selected_individuals = numpy.random.choice(ind_position, self.pop_size, True, probability)
        for ind in selected_individuals:
            parents.append(self.population[ind])
        return parents

    def reproduce(self, parents):
        chromosome_len = self.population[0].chromosome_len
        next_generation = list()
        for pair in range(len(parents)//2):
            first_parent, second_parent = random.randint(0, len(parents) - 1), random.randint(0, len(parents) - 1)
            while first_parent == second_parent:
                second_parent = random.randint(0, len(parents) - 1)
            cross_prob = random.random()
            if cross_prob <= self.cross_prob:
                cross_point = random.randrange(chromosome_len)
                first_child = Individual(parents[first_parent].get_chrome()[0:cross_point] +
                                         parents[second_parent].get_chrome()[cross_point:chromosome_len])
                second_child = Individual(parents[second_parent].get_chrome()[0:cross_point] +
                                          parents[first_parent].get_chrome()[cross_point:chromosome_len])
            else:
                first_child, second_child = parents[first_parent], parents[second_parent]
            next_generation.append(first_child)
            next_generation.append(second_child)
        return next_generation

    def mutation(self, next_generation):
        chromosome_len = self.population[0].chromosome_len
        for ind in range(len(next_generation)):
            if random.random() <= self.mut_prob:
                mutated = random.randrange(chromosome_len)
                mutation = '0'
                if next_generation[ind].get_chrome()[mutated] == '0':
                    mutation = '1'
                    next_generation[ind] = Individual(next_generation[ind].get_chrome()[0:mutated] + mutation +
                                                      next_generation[ind].get_chrome()[mutated + 1:chromosome_len])
                else:
                    next_generation[ind] = Individual(next_generation[ind].get_chrome()[0:mutated] + mutation +
                                                      next_generation[ind].get_chrome()[mutated + 1:chromosome_len])
        return next_generation

    def best_fitness(self):
        best_fitness = max(self.fitness_list)
        best_individual = self.fitness_list.index(best_fitness)
        return best_fitness, best_individual

    def proceed(self):
        parents = self.roulette_wheel()
        next_generation = self.reproduce(parents)
        next_generation = self.mutation(next_generation)
        self.population = next_generation
        for ind in range(len(self.population)):
            self.fitness_list[ind] = self.population[ind].fitness_function()

    def solve(self, min_fitness=7.9, max_epochs=3000):
        best_fitness, best_individual = self.best_fitness()
        epochs_num = int()
        while (min_fitness is None or best_fitness < min_fitness) and (max_epochs is None or epochs_num < max_epochs):
            self.proceed()
            best_fitness, best_individual = self.best_fitness()
            epochs_num += 1
        visual = self.population[best_individual].visualisation()
        return best_fitness, epochs_num, visual
