from geneticAlgorithm import Genetic_algorithm
import tkinter as tk
import copy
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
class Graphics:


    def __init__(self, size, grid, fitness, max_size, num_of_gen, stabilized, cell_size=20, speed=10):
        self.size = size
        self.cell_size = cell_size
        self.speed = speed
        self.grid = grid
        self.generation = 0
        self.num_of_gen = num_of_gen
        self.window = tk.Tk()
        self.matrix = [[0 for _ in range(size)] for _ in range(size)]
        self.fitness = fitness
        self.max_size = max_size
        self.stabilized = stabilized
        self.create_matrix(grid)
        label_text = (
            f'Fitness: {self.fitness} , Max Size: {self.max_size} , Stabilized from generation: {self.stabilized} \nGeneration: {self.generation}'
        )
        self.label = tk.Label(
            self.window, text=label_text, font=('Helvetica', 14, 'bold'), justify='center')
        self.label.pack(side=tk.TOP, pady=10)  # Place the label first

        self.canvas = tk.Canvas(self.window, width=self.size * self.cell_size,
                                height=self.size * self.cell_size, bg='white')
        self.canvas.pack()  # Pack the canvas after the label
       
        self.window.resizable(False, False)
        self.window.title("Simulation ")
        self.update_screen()
        # Schedule the new_generation method to run at regular intervals
        self.window.after(0, self.new_generation)
        self.window.mainloop()

    def create_matrix(self, grid):
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) in grid:
                    self.matrix[i][j] = 1

    def update_screen(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing
        #sleep(10)
        for r in range(self.size):
            for c in range(self.size):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if self.matrix[r][c] == 1:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill='mediumseagreen', outline='black')
                else:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill='white', outline='black')

    def new_generation(self):
        if self.generation < self.num_of_gen:
            temp_matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]
            for i in range(self.size):
                for j in range(self.size):
                    live_neighbors = self.num_of_neighbors_alive(i, j)
                    if self.matrix[i][j] == 1:
                        if live_neighbors < 2 or live_neighbors > 3:
                            temp_matrix[i][j] = 0
                        elif 2 <= live_neighbors <= 3:
                            temp_matrix[i][j] = 1
                    else:
                        if live_neighbors == 3:
                            temp_matrix[i][j] = 1
            self.matrix = copy.deepcopy(temp_matrix)

            self.update_screen()
            self.window.after(500 // self.speed, self.new_generation)
            self.generation += 1
            self.label.config(text=f'Fitness: {self.fitness} , Max Size: {self.max_size} , Stabilized from generation: {self.stabilized}  \nGeneration: {self.generation}')

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


if __name__ == '__main__':

    genetic_algo = Genetic_algorithm()

    average_fitness = [np.mean(generation) for generation in genetic_algo.fittnes_over_gen]
    plt.bar(range(1, len(average_fitness) + 1), average_fitness)
    plt.xlabel('Generation')
    plt.ylabel('Average Fitness')
    plt.title('Fitness Over Generations')
    plt.show()

    f = open('best_solutions.txt', 'w')
    for s in genetic_algo.get_best_solutions() : 
        f.write("{}\n".format(s))
    f.close()


    #C
    length = len(genetic_algo.best_solutions) - 1
    grid = genetic_algo.best_solutions[length][0]
    size = 30
    fitness = genetic_algo.best_solutions[length][1]
    max_size = genetic_algo.best_solutions[length][2]
    stabilized = genetic_algo.best_solutions[length][3]
    Graphics(size , grid , fitness , max_size ,400, stabilized)


    


