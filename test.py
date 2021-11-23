import gurobipy as gp


n = ["DC1", "DC2", "Node1", "Node2", "Node3", "Node4", "Node5"]



edges = [[0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0],
         [1, 0, 0, 1, 0, 1, 0],
         [1, 1, 1, 0, 1, 1, 1],
         [0, 1, 0, 1, 0, 0, 1],
         [0, 0, 1, 1, 0, 0, 1],
         [0, 0, 0, 1, 1, 1, 0]]


de = [[0, 10, 2, 1, 0, 0, 0],
        [10, 0, 0, 5, 1, 0, 0],
         [2, 0, 0, 10, 0, 1, 0],
         [1, 5, 10, 0, 10, 1, 1],
         [0, 1, 0, 10, 0, 0, 2],
         [0, 0, 1, 1, 0, 0, 1],
         [0, 0, 0, 1, 2, 1, 0]]


be = [[0, 9, 9, 1, 0, 0, 0],
             [9, 0, 0, 9, 9, 0, 0],
             [9, 0, 0, 9, 0, 9, 0],
             [1, 9, 10, 0, 9, 9, 9],
             [0, 9, 0, 9, 0, 0, 9],
             [0, 0, 9, 9, 0, 0, 9],
             [0, 0, 0, 9, 9, 9, 0]]
mapping = {"DC1": 0, "DC2": 1, "Node1": 2,
"Node2": 3, "Node3": 4, "Node4": 5, "Node5": 6}

model = gp.Model()
nodes = len(edges)
arcs = [(i, j) for i in range(nodes) for j in range(nodes)]
flow = model.addVars(arcs, vtype=gp.GRB.CONTINUOUS, name="flow")

model.ModelSense = gp.GRB.MINIMIZE
objective = gp.quicksum(flow[(i, j)] * de[i][j] for i in range(nodes) for j in range(nodes))

model.setObjective(objective)

model.addConstrs((flow[(i, j)] <= be[i][j] * edges[i][j] for i in range(nodes) for j in range(nodes)), "Bandwith Constraint")

model.addConstr((gp.quicksum(flow[2, i] for i in range(nodes)) == gp.quicksum(flow[i, 2] for i in range(nodes))+ 1) , name="Node1 flow conservation")
model.addConstr((gp.quicksum(flow[3, i] for i in range(nodes)) == gp.quicksum(flow[i, 3] for i in range(nodes))+ 1) , name="Node2 flow conservation")
model.addConstr((gp.quicksum(flow[4, i] for i in range(nodes)) == gp.quicksum(flow[i, 4] for i in range(nodes))+ 1) , name="Node3 flow conservation")
model.addConstr((gp.quicksum(flow[5, i] for i in range(nodes)) == gp.quicksum(flow[i, 5] for i in range(nodes)) + 1), name="Node4 flow conservation")
model.addConstr((gp.quicksum(flow[6, i] for i in range(nodes)) == gp.quicksum(flow[i, 6] for i in range(nodes))+ 1) , name="Node4 flow conservation")




model.addConstr((gp.quicksum(flow[i, 0] for i in range(2, nodes)) == 3
                  ), name="DC1 Capacity")

model.addConstr((gp.quicksum(flow[i, 1] for i in range(2, nodes)) == 2
                  ), name="DC2 Capacity")


model.optimize()
print(model.display())
print("Objective value: " + str(model.objVal))
for i in arcs:
    print(f"flows{i}: " + str(flow[i].X))


