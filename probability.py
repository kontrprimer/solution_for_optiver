from pyomo.environ import *
model = ConcreteModel()
n = 5
a = [
    [
        ((10*(i-n)-2.5)/30)**2 + ((10*(j-n)-2.5)/40)**2 < 1
        for j in range(2*n+1)
    ]
    for i in range(2*n+1)
]


def is_terminator(m, i, j):
    if a[i][j]:
        return 0, None
    return 0, 0


model.x = Var(list(range(2*n+1)),
              list(range(2*n+1)),
              bounds=is_terminator)
model.eq = ConstraintList()
for i in range(2*n+1):
    for j in range(2*n+1):
        if a[i][j]:
            model.eq.add(
                4*(model.x[i, j] - 1) == model.x[i-1, j] + model.x[i+1, j] + model.x[i, j-1] + model.x[i, j+1]
            )
model.revenue = Objective(expr=sum([model.x[i, j] for i in range(2*n+1) for j in range(2*n+1)]), sense=maximize)
solver = SolverFactory('glpk')
status = solver.solve(model, tee=False)
print(model.x[n, n].value)
