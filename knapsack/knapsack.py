from ortools.algorithms.pywrapknapsack_solver import KnapsackSolver


def knapsack(weights, values, capacities):
    assert(len(weights) == len(values))
    items = list(range(len(weights)))
    bins = list(range(len(capacities)))

    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    x = {}
    for i in items:
        for b in bins:
            x[i, b] = solver.IntVar(lb=0, ub=1, name=f'x_{i}_{b}')
    
    # Constraints
    for i in items:
        solver.Add(sum(x[i, b] for b in bins) <= 1)
    for b in bins:
        solver.Add(sum(x[i, b] * weights[i] for i in items) <= capacities[b])
    
    # Objective
    objective = solver.Objective()
    for i in items:
        for b in bins:
            objective.SetCoefficient(x[i, b], values[i])
    objective.SetMaximization()

    # Solve
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        raise ValueError('This problem does not have an optimal solution')

    return [
        [i for i in items if x[i, b].solution_value() > 0]
        for b in bins
    ]


if __name__ == '__main__':
    weights = [23, 26, 20, 18, 32, 27, 29, 26, 30, 27]
    values = [505, 352, 458, 220, 354, 414, 498, 545, 473, 543]

    print(knapsack(weights, values, capacities=[67]))
    # [[0, 3, 7]]

    print(knapsack(weights, values, capacities=[67, 123]))
    # [[6, 8], [0, 2, 5, 7, 9]]
