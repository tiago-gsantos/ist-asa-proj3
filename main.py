from pulp import *

n, p, maxProd = map(int, input().split())
varsNames, profits, toysCapacity = [], [], []
toysPackage = [[] for _ in range(n)]

for i in range(n):
  varsNames.append(f"X{i}")
  profit, capacity = map(int, input().split())
  profits.append(profit)
  toysCapacity.append(capacity)

for i in range(p):
  varsNames.append(f"Y{i}")
  toy1, toy2, toy3, profit = map(int, input().split())
  profits.append(profit)
  toysPackage[toy1-1].append(i)
  toysPackage[toy2-1].append(i)
  toysPackage[toy3-1].append(i)

prob = LpProblem("Bars_Problem", LpMaximize)

vars = [LpVariable(varsNames[i], 0, None, LpInteger) for i in range(n + p)]

prob += lpSum([vars[i] * profits[i] for i in range(n + p)]), "objective_function"

prob += lpSum([vars[i] for i in range(n)]) + lpSum([vars[i] * 3 for i in range(n, n + p)]) <= maxProd, "total_capacity_restriction"

for i in range(n):
  prob += vars[i] + lpSum(vars[toysPackage[i][k] + n] for k in range (len(toysPackage[i]))) <= toysCapacity[i], f"capacity_restriction_{i}"

prob.solve(GLPK(msg=0))

if LpStatus[prob.status] != "Optimal":
    print("Infeasible")
else:
    print(value(prob.objective))

#for v in prob.variables():
#  print(v.name, "=", v.varValue)