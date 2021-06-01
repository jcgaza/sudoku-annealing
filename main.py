import os
import csv
from solution import Solution

# s = Solution(num_neighbors=0, reheat=40)
# print(s.start_algorithm("./difficulty-5/s05a.txt"))

s = Solution(num_neighbors=0, reheat=20, limit_seconds=600)
path = './'
for folder in sorted(os.listdir(path)):
# for folder in ['difficulty-4', 'difficulty-5']:
  if 'difficulty' in folder:
    for item in sorted(os.listdir(path+folder)):
      if "txt" in item and "generated" not in item:
        print("Reading " + item)
        filename = path+folder+"/"+item
        initial_cost, final_cost, num_iterations, num_reheat, final_time = s.start_algorithm(filename)
        with open('data.csv', 'a+') as write_obj:
          csv_writer = csv.writer(write_obj)
          csv_writer.writerow([filename,initial_cost, final_cost,num_iterations, num_reheat, final_time])

