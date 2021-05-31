  # def generate_combinations(self, indices):
  #   print("Generating combinations...")
  #   c = []
  #   for grid in range(len(indices)):
  #     # Formula:
  #     # row = (num // 3) + ((grid // 3) * 3)
  #     # col = (num % 3) + ((grid % 3) * 3)
  #     # index = (row * 9) + col

  #     temp = [((((num // 3) + ((grid // 3) * 3)) * 9) + ((num % 3) + ((grid % 3) * 3))) for num in indices[grid]]
  #     c.extend(list(combinations(temp, 2)))
    
  #   return c
  
  # def generate_neighborhood(self, solution, indices):
  #   neighborhood = []

  #   for index in range(len(indices)-self.num_neighbors):
  #     currRow1 = indices[index][0] // 9
  #     currCol1 = indices[index][0] % 9

  #     currRow2 = indices[index][1] // 9
  #     currCol2 = indices[index][1] % 9

  #     copy = deepcopy(solution)

  #     copy[currRow1, currCol1], copy[currRow2, currCol2] = copy[currRow2, currCol2], copy[currRow1, currCol1]
  #     neighborhood.append(copy)
    
  #   return neighborhood