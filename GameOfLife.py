import random
import copy
class Game_of_life :
    def __init__(self , size = 30, initial_size = 0 , matrix = None):
        self.size = size
        self.initial_size = initial_size #number of living cells
        self.current_size = initial_size #number of living cells
        if matrix == None:
            self.matrix = self.init_grid(size)
        else :
            self.matrix = matrix
        self.initinal_state = self.matrix
        #self.num_of_generations = 0

    def get_live_cells(self , state):
        live_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == 1:
                    live_cells.append((i,j))
        return live_cells
    
    def init_grid(self , size) :
        matrix = [[0 for _ in range(size)] for _ in range(size)]
        probability = 0
        count = 0
        center = size // 2
        radius = size // 10
        num = center - radius, center + radius
        for i in range(center - radius, center + radius):
            for j in range(center - radius, center + radius):
                probability = random.random()
                if probability < 0.7 :
                    matrix[i][j] = 1
                    count += 1
        self.initial_size = count
        self.current_size = count
        return matrix       

    def new_generation(self):
        temp_matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                live_neighbors = self.num_of_neighbors_alive(i , j)
                if self.matrix[i][j] == 1:
                    if live_neighbors < 2 or live_neighbors > 3:
                        temp_matrix[i][j] = 0
                        self.current_size -= 1
                    if live_neighbors == 2 or live_neighbors ==3:
                        temp_matrix[i][j] = 1
                else: #dead cell
                    if live_neighbors == 3:
                        temp_matrix[i][j] = 1
                        self.current_size += 1
        self.matrix = copy.deepcopy(temp_matrix)

    def num_of_neighbors_alive(self , i , j):
        count = 0
        if i-1 >=0 and j-1 >= 0 and self.matrix[i-1][j-1] == 1:
            count += 1
        if i-1 >= 0 and self.matrix[i-1][j] == 1:
            count += 1
        if i-1 >= 0 and j+1 < self.size and self.matrix[i-1][j+1] == 1:
            count += 1
        if j-1 >= 0 and self.matrix[i][j-1] == 1:
            count += 1
        if j+1 < self.size and self.matrix[i][j+1] == 1:
            count += 1
        if i+1 < self.size and j-1 >=0 and self.matrix[i+1][j-1] == 1:
            count += 1
        if i+1 < self.size and self.matrix[i+1][j] == 1:
            count += 1
        if i+1 < self.size and j+1 < self.size and self.matrix[i+1][j+1] == 1:
            count += 1
        return count
    

class Simulation :
    def __init__(self,game):
        self.game = game
        self.game.matrix = self.game.initinal_state
        self.current_gen = 0
        self.total_generations = 400
        self.history = []
        self.max_size = self.game.current_size
        # The number of generation in which the game stabilized
        self.stabilized = -1
        self.start_simulation()
        

    def start_simulation(self):
        stable = False
        while self.current_gen <= self.total_generations and stable == False:
            self.current_gen += 1
            self.history.append(copy.deepcopy(self.game.get_live_cells(self.game.matrix)))
            self.game.new_generation()
            if self.max_size < self.game.current_size:
                self.max_size = self.game.current_size
            stable = self.is_stable()
            if stable == True:
                self.stabilized = self.current_gen 

    
    def is_stable(self):
        return self.game.get_live_cells(self.game.matrix) in self.history
