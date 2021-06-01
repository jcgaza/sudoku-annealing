import solution

s = solution.Solution()
solution, _ = s.generate_random("./difficulty-1/s01a.txt")
print(solution)
print(s.cost(solution))