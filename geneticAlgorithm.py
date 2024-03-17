import random

from GameOfLife import Game_of_life
from GameOfLife import Simulation

class Genetic_algorithm :

    def __init__(self):
        self.N = 10 # population_size
        self.population = [] # each element is in the form of [chromosome,fitness]
        self.time_effect = 0.7
        self.mutation_probability = 0.2
        self.create_population()
        self.num_of_gen = 1
        self.total_gen = 40
        self.fittnes_over_gen = [[fitness for _, fitness in self.population]] # fittnes through the generations
        self.fittest_chromosome = None  # [chromosome,fitness]
        self.best_solutions = [] # The successful Methuselahs
        self.update_fittest_chromosome()

        self.run_algo()

    def get_best_solutions(self):
        return self.best_solutions
        
    def run_algo(self):
        while self.num_of_gen < self.total_gen:
            self.num_of_gen += 1
            self.reproduction()
            self.evaluate()
            self.fittnes_over_gen += [fitness for _, fitness in self.population]
            self.update_fittest_chromosome()
        print(self.fittnes_over_gen)

    def update_fittest_chromosome(self):
        for chromosome in self.population:
            if self.fittest_chromosome == None:
                self.fittest_chromosome =chromosome
                game = chromosome[0]
                sim = Simulation(game)
                self.best_solutions.append([game.get_live_cells(game.initinal_state),chromosome[1],sim.max_size,sim.stabilized])
            else:
                if chromosome[1] > self.fittest_chromosome[1]:
                    self.fittest_chromosome = chromosome
                    game = chromosome[0]
                    sim = Simulation(game)
                    self.best_solutions.append([game.get_live_cells(game.initinal_state),chromosome[1],sim.max_size,sim.stabilized])


    def evaluate(self):
        for i in range(self.N):
            game = self.population[i][0]
            sim = Simulation(game)
            if sim.stabilized == -1 : # The model did not stabilize
                fitness = 0 
            else : # fitness is contingent upon two pivotal factors. Firstly, it hinges on the evolutionary trajectory of a configuration,
                 # which undergoes a protracted period of refinement before attaining stability. Secondly, the degree of success 
                 #is intricately tied to the configuration's developmental zenith,
                 #specifically the maximum size it achieves during its maturation process.
                fitness = (sim.max_size - game.initial_size) + sim.stabilized * self.time_effect
            self.population[i][1] = fitness

    # step 1 :INITIALIZE create a population of population_size elements , each with randomaly generated DNA
    def create_population(self):
        for _ in range(self.N):
            game = Game_of_life()
            sim = Simulation(game)
            # step 2 : evaluate the fitness of each element of the population
            if sim.stabilized == -1 : # The model did not stabilize
                fitness = 0 
            else : # fitness is contingent upon two pivotal factors. Firstly, it hinges on the evolutionary trajectory of a configuration,
                 # which undergoes a protracted period of refinement before attaining stability. Secondly, the degree of success 
                 #is intricately tied to the configuration's developmental zenith,
                 #specifically the maximum size it achieves during its maturation process.
                fitness = int((sim.max_size - game.initial_size) + sim.stabilized * self.time_effect)

            self.population.append([game,fitness])


    #step 3 : Reproduction 
    def reproduction(self):
        new_population = []
        total_f = sum(f for _ , f in self.population) 
        probabilities = [fitness / total_f if total_f != 0 else 0 for _, fitness in self.population]

        # repeat N times
        for i in range(self.N):
            # a -> picking two parents with probability according to relative fitness
            mom = random.choices(self.population, weights=probabilities, k=1)[0][0]
            dad = random.choices(self.population, weights=probabilities, k=1)[0][0]

            # Crossover - create a child by combinig the DNA of these two parents
            if random.random() <= 0.4:
                child = self.crossover(mom , dad)
            else :
                child = Game_of_life(mom.size ,mom.initial_size,mom.initinal_state)
            
            # Mutate the child's DNA based on a probability mutation_probability
            child = self.mutate(child)
   
            # Add the new child to a new populotion 
            new_population.append(child)

        # Replacing the old population with the new population 
        self.population = [[solution , 0] for solution in new_population]

    def crossover(self , mom , dad):

        grid_size = max(mom.size , dad.size)
        child_matrix = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

        mom_live_cells = mom.get_live_cells(mom.initinal_state)
        dad_live_cells = dad.get_live_cells(dad.initinal_state)
            
        selected_cells = random.sample(dad_live_cells, k = dad.initial_size //2)
        selected_cells += random.sample(mom_live_cells, k = mom.initial_size //2)

        child_initinal_size = 0
        for i , j in selected_cells :
            if child_matrix[i][j] == 0:
                child_matrix[i][j] = 1
                child_initinal_size += 1
            
        return Game_of_life(grid_size ,child_initinal_size,child_matrix)
            
    def mutate(self , child):

        if random.random() <= self.mutation_probability :
            i = random.randint(0, child.size-1) # Each cell in the chromosome has an equal chance of flipping
            j = random.randint(0, child.size-1)

            # flipping the state 
            if child.matrix[i][j] == 1 :
                child.matrix[i][j] = 0
            else: child.matrix[i][j] = 1  
            
        return child

