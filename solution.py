import numpy as np 
import time
import statistics
from math import exp
from copy import deepcopy
from itertools import combinations
from matplotlib import pyplot

class Solution:
  def __init__(self, reheat = 50, num_neighbors = 0, limit_seconds = 300, cooling_rate=0.99):
    self.num_neighbors = num_neighbors
    self.reheat = reheat
    self.cooling_rate = cooling_rate
    self.limit_seconds = limit_seconds

  def read_file(self, filename):
    print("Reading {}...".format(filename))
    return np.loadtxt("{}".format(filename))
  
  def generate_random(self, filename):
    print("Generating a random solution...")
    array = self.read_file(filename)
    nums = np.array([i for i in range(1,10)])
    indices = []

    for i in range(0,9,3):
      for j in range(0,9,3):
        flat = array[i:i+3, j:j+3].flatten()
        diff = np.setdiff1d(nums, flat)     # Get numbers that are not in the original

        a = 0
        self.num_neighbors += 9 - len(diff)
        np.random.shuffle(diff)

        temp = []
        for k in range(len(flat)):
          if flat[k] == 0:
            temp.append(k)
            flat[k] = diff[a]
            a += 1
        
        array[i:i+3, j:j+3] = flat.reshape(3,3)
        indices.append(temp)
    
    return array, indices
  
  def cost(self, array):
    # nums = np.array([i for i in range(1,10)])
    cost = 0

    for i in range(9):      # Get cost of repeating numbers
      print(9-len(np.unique(array[i])))
      cost += 9-len(np.unique(array[i]))
      print(9-len(np.unique(array[:,i])))
      cost += 9-len(np.unique(array[:,i]))
    
    return cost
  
  def stopping_criteria(self, solution_cost, start_time):
    if solution_cost == 0 or time.time() > start_time + self.limit_seconds:
      return False
    return True


  def generate_neighborhood1(self, solution, indices):
    neighborhood = []
    for i in range(len(indices)):
      startRow = (i // 3) * 3
      startCol = (i % 3) * 3

      for gen in list(combinations(indices[i], 2)):
        currRow1 = ((gen[0] // 3)) + startRow
        currCol1 = ((gen[0] % 3)) + startCol

        currRow2 = ((gen[1] // 3)) + startRow
        currCol2 = ((gen[1] % 3)) + startCol
        
        copy = deepcopy(solution)

        copy[currRow1, currCol1], copy[currRow2, currCol2] = copy[currRow2, currCol2], copy[currRow1, currCol1]
        neighborhood.append(copy)
    
    np.random.shuffle(neighborhood)

    return neighborhood[:self.num_neighbors]
  
  def start_algorithm(self, filename):
    solution, indices = self.generate_random(filename)
    solution_cost = self.cost(solution)
    initial_cost = solution_cost

    r_num = 0
    t0 = statistics.pstdev([self.cost(x) for x in self.generate_neighborhood1(solution, indices)][:10])
    temperature = t0

    start_time = time.time()
    x = [time.time() - start_time]
    y = [solution_cost]

    num_iterations = 0
    num_reheat = 0

    while self.stopping_criteria(solution_cost, start_time):
      neighborhood = self.generate_neighborhood1(solution, indices)
      print("Temperature:", temperature, "; Solution cost:", solution_cost)

      prev_cost = solution_cost
      for neighbor in neighborhood:
        new_cost = self.cost(neighbor)

        if new_cost < solution_cost:
          solution = deepcopy(neighbor)
          solution_cost = new_cost

        else:
          loss = abs(solution_cost - new_cost)
          probability = exp(-(loss / temperature))

          if np.random.uniform(1,0,1) <= probability:
            solution = deepcopy(neighbor)
            solution_cost = new_cost

      if r_num > self.reheat:
        temperature = t0
        r_num = 0
        num_reheat += 1
        
      elif prev_cost == solution_cost:
        r_num += 1

      else:
        r_num = 0

      x.append(time.time() - start_time)
      y.append(solution_cost)
      
      num_iterations += 1
      temperature *= self.cooling_rate
      np.savetxt(filename[:-4]+"-generated.txt", solution, fmt="%d")

    final_time = time.time() - start_time
    pyplot.figure()
    pyplot.subplot()
    pyplot.plot(x, y)
    pyplot.xlabel("Seconds")
    pyplot.ylabel("Cost")
    pyplot.title("Cost Progression for " + filename[2:-4])
    pyplot.savefig(filename[:-3]+"png", format="png")
    # pyplot.show()

    return initial_cost, solution_cost, num_iterations, num_reheat, final_time