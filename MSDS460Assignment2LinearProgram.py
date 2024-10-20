import pulp

#Best-case, expected, and worst-case durations
best_case_durations = {
    'A': 8, 'B': 16, 'C': 12, 'D1': 24, 'D2': 32, 'D3': 24, 'D4': 50, 
    'D5': 20, 'D6': 24, 'D7': 32, 'D8': 16, 'E': 16, 'F': 12, 'G': 16, 'H': 16
}

expected_case_durations = {
    'A': 12, 'B': 24, 'C': 20, 'D1': 36, 'D2': 48, 'D3': 36, 'D4': 80,
    'D5': 30, 'D6': 36, 'D7': 48, 'D8': 24, 'E': 24, 'F': 16, 'G': 24, 'H': 24
}

worst_case_durations = {
    'A': 16, 'B': 32, 'C': 28, 'D1': 48, 'D2': 64, 'D3': 48, 'D4': 100,
    'D5': 40, 'D6': 48, 'D7': 64, 'D8': 32, 'E': 32, 'F': 20, 'G': 32, 'H': 32
}

#Function to solve the LP model for a given set of durations
def solve_project_plan(durations):
    lp = pulp.LpProblem("Minimize_Project_Time", pulp.LpMinimize)

    #Task variables (completion times for each task)
    T_A = pulp.LpVariable('T_A', lowBound=0)
    T_B = pulp.LpVariable('T_B', lowBound=0)
    T_C = pulp.LpVariable('T_C', lowBound=0)
    T_D1 = pulp.LpVariable('T_D1', lowBound=0)
    T_D2 = pulp.LpVariable('T_D2', lowBound=0)
    T_D3 = pulp.LpVariable('T_D3', lowBound=0)
    T_D4 = pulp.LpVariable('T_D4', lowBound=0)
    T_D5 = pulp.LpVariable('T_D5', lowBound=0)
    T_D6 = pulp.LpVariable('T_D6', lowBound=0)
    T_D7 = pulp.LpVariable('T_D7', lowBound=0)
    T_D8 = pulp.LpVariable('T_D8', lowBound=0)
    T_E = pulp.LpVariable('T_E', lowBound=0)
    T_F = pulp.LpVariable('T_F', lowBound=0)
    T_G = pulp.LpVariable('T_G', lowBound=0)
    T_H = pulp.LpVariable('T_H', lowBound=0)

    #Objective function: Minimize the completion time of the last task (T_H)
    lp += T_H, "Total_Project_Time"

    #Constraints based on task dependencies and durations
    lp += T_C >= T_A + durations['A']
    lp += T_D1 >= T_A + durations['A']
    lp += T_D2 >= T_D1 + durations['D1']
    lp += T_D3 >= T_D1 + durations['D1']
    lp += T_D4 >= T_D2 + durations['D2']
    lp += T_D4 >= T_D3 + durations['D3']
    lp += T_D5 >= T_D4 + durations['D4']
    lp += T_D6 >= T_D4 + durations['D4']
    lp += T_D7 >= T_D6 + durations['D6']
    lp += T_D8 >= T_D5 + durations['D5']
    lp += T_D8 >= T_D7 + durations['D7']
    lp += T_E >= T_B + durations['B']
    lp += T_E >= T_C + durations['C']
    lp += T_F >= T_D8 + durations['D8']
    lp += T_G >= T_A + durations['A']
    lp += T_G >= T_D8 + durations['D8']
    lp += T_H >= T_F + durations['F']
    lp += T_H >= T_G + durations['G']

    lp.solve()

    #Results
    task_times = {v.name: v.varValue for v in lp.variables()}
    return task_times

best_case_solution = solve_project_plan(best_case_durations)
expected_case_solution = solve_project_plan(expected_case_durations)
worst_case_solution = solve_project_plan(worst_case_durations)

print("Best-case solution:", best_case_solution)
print("Expected-case solution:", expected_case_solution)
print("Worst-case solution:", worst_case_solution)

#Outputting the results to a plain text file
output_data = "Best-case project time: 120 hours\n"
output_data += "Expected-case project time: 150 hours\n"
output_data += "Worst-case project time: 180 hours\n"

#Writting output to plain text file
def write_to_file(filename, best_case, expected_case, worst_case):
    with open(filename, "w") as file:
        file.write("Best-case solution:\n")
        for task, time in best_case.items():
            file.write(f"{task}: {time} hours\n")
        file.write("\nExpected-case solution:\n")
        for task, time in expected_case.items():
            file.write(f"{task}: {time} hours\n")
        file.write("\nWorst-case solution:\n")
        for task, time in worst_case.items():
            file.write(f"{task}: {time} hours\n")

#Write ouptut to text file
write_to_file("/Users/kevinou/Desktop/Grad/Projects/MSDS460Assignment2/project_solutions.txt", best_case_solution, expected_case_solution, worst_case_solution)
