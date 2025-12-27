# Sheep Program by : Kamil P Szynklewski
# Student Number : 2409931

import aips.search as search
from aips.informed.search import BestFirstSearchProblem  # Importing A* base class for informed search

# Class to hold pen capacities and movement costs
class Settings:
    def __init__(self, a_max, b_max, cost_field_to_pen, cost_pen_to_pen, cost_pen_to_field):
        if not (isinstance(a_max, int) and a_max > 0):
            raise ValueError(f"A_max must be an integer > 0, got {a_max}")
        if not (isinstance(b_max, int) and b_max > 0):
            raise ValueError(f"B_max must be an integer > 0, got {b_max}")
        self.A_max = a_max
        self.B_max = b_max
        self.cost_field_to_pen = cost_field_to_pen
        self.cost_pen_to_pen = cost_pen_to_pen
        self.cost_pen_to_field = cost_pen_to_field

# Represents an action taken by the shepherd to move sheep
class ShepherdAction(search.Action):
    def __init__(self, description, cost):
        super().__init__()
        self.description = description
        self.cost = cost

    def __str__(self):
        return f"{self.description}. Cost: {self.cost}"

# Represents a state: how many sheep are in each pen (A, B)
# Validates state constraints against max pen sizes
class ShepherdState(search.State):
    def __init__(self, a, b, settings):
        if not (isinstance(a, int) and a >= 0):
            raise ValueError(f"State 'a' must be an integer >= 0, got {a}")
        if not (isinstance(b, int) and b >= 0):
            raise ValueError(f"State 'b' must be an integer >= 0, got {b}")
        if a > settings.A_max:
            raise ValueError(f"State 'a' ({a}) cannot exceed capacity A_max ({settings.A_max})")
        if b > settings.B_max:
            raise ValueError(f"State 'b' ({b}) cannot exceed capacity B_max ({settings.B_max})")

        self.a = a
        self.b = b
        self.settings = settings

    def __str__(self):
        return f"Pen A: {self.a} (max:{self.settings.A_max}) Pen B: {self.b} (max:{self.settings.B_max})"

    def __eq__(self, other):
        return isinstance(other, ShepherdState) and self.a == other.a and self.b == other.b

    def __hash__(self):
        return hash((self.a, self.b))

    # Defines all valid moves from this state
    def successor(self):
        successors = []

        # Move from field to Pen A (fill Pen A to its capacity)
        if self.a < self.settings.A_max:
            moved = self.settings.A_max - self.a
            cost = moved * self.settings.cost_field_to_pen
            action = ShepherdAction("Moving sheep from the field to Pen A", cost)
            next_state = ShepherdState(self.settings.A_max, self.b, self.settings)
            successors.append(search.ActionStatePair(action, next_state))

        # Move from field to Pen B (fill Pen B to its capacity)
        if self.b < self.settings.B_max:
            moved = self.settings.B_max - self.b
            cost = moved * self.settings.cost_field_to_pen
            action = ShepherdAction("Moving sheep from the field to Pen B", cost)
            next_state = ShepherdState(self.a, self.settings.B_max, self.settings)
            successors.append(search.ActionStatePair(action, next_state))

        # Empty Pen A back to field
        if self.a > 0:
            moved = self.a
            cost = moved * self.settings.cost_pen_to_field
            action = ShepherdAction("Moving sheep from Pen A to the field", cost)
            next_state = ShepherdState(0, self.b, self.settings)
            successors.append(search.ActionStatePair(action, next_state))

        # Empty Pen B back to field
        if self.b > 0:
            moved = self.b
            cost = moved * self.settings.cost_pen_to_field
            action = ShepherdAction("Moving sheep from Pen B to the field", cost)
            next_state = ShepherdState(self.a, 0, self.settings)
            successors.append(search.ActionStatePair(action, next_state))

        # Transfer sheep from Pen A to Pen B
        if self.a > 0 and self.b < self.settings.B_max:
            moved = min(self.a, self.settings.B_max - self.b)
            cost = moved * self.settings.cost_pen_to_pen
            action = ShepherdAction("Moving sheep from Pen A to Pen B", cost)
            next_state = ShepherdState(self.a - moved, self.b + moved, self.settings)
            successors.append(search.ActionStatePair(action, next_state))

        # Transfer sheep from Pen B to Pen A
        if self.b > 0 and self.a < self.settings.A_max:
            moved = min(self.b, self.settings.A_max - self.a)
            cost = moved * self.settings.cost_pen_to_pen
            action = ShepherdAction("Moving sheep from Pen B to Pen A", cost)
            next_state = ShepherdState(self.a + moved, self.b - moved, self.settings)
            successors.append(search.ActionStatePair(action, next_state))

        return successors

# Implements A* search logic
class ShepherdProblemAStar(BestFirstSearchProblem):
    def heuristic(self, state):
        # Heuristic estimate: total sheep not in the right pen * cheapest movement cost
        misplaced_sheep = abs(state.a - self.goalState.a) + abs(state.b - self.goalState.b)
        min_cost_per_sheep = self.startState.settings.cost_pen_to_field  # Lower bound for cost
        return misplaced_sheep * min_cost_per_sheep

    def evaluation(self, node):
        # A* evaluation function f(n) = g(n) + h(n)
        return node.getCost() + self.heuristic(node.state)

    def isGoal(self, state):
        return state == self.goalState

# Cleans up the solution into a presentable state
def print_solution(label, problem, solution_path):
    print(f"\n--- {label} ---")
    if solution_path is None:
        print("No solution found.")
    else:
        print(f"Nodes explored: {problem.nodeVisited} | Total Cost: {solution_path.cost}")
        print(solution_path.head)
        for action_state_pair in solution_path.list:
            print(action_state_pair.action)
            print(action_state_pair.state)

# Basic Problem
def run_basic_problem():
    settings = Settings(a_max=9, b_max=15, cost_field_to_pen=60.0, cost_pen_to_pen=30.0, cost_pen_to_field=5.0)
    initial = ShepherdState(0, 0, settings)
    goal = ShepherdState(0, 12, settings)
    problem = ShepherdProblemAStar(initial, goal)
    solution = problem.search()
    print_solution("Basic Problem", problem, solution)

# General Problem
def run_general_problem():
    settings = Settings(a_max=10, b_max=7, cost_field_to_pen=60.0, cost_pen_to_pen=30.0, cost_pen_to_field=5.0)
    initial = ShepherdState(0, 0, settings)
    goal = ShepherdState(0, 5, settings)
    problem = ShepherdProblemAStar(initial, goal)
    solution = problem.search()
    print_solution("General Problem", problem, solution)

# Additional test cases
def run_test_cases():
    # 1. Extreme test: very large pens
    settings = Settings(a_max=100, b_max=100, cost_field_to_pen=60.0, cost_pen_to_pen=30.0, cost_pen_to_field=5.0)
    initial = ShepherdState(0, 0, settings)
    goal = ShepherdState(50, 50, settings)
    problem = ShepherdProblemAStar(initial, goal)
    solution = problem.search()
    print_solution("Extreme Large Pens", problem, solution)

    # 2. No movement needed (already in goal state)
    settings = Settings(a_max=10, b_max=10, cost_field_to_pen=60.0, cost_pen_to_pen=30.0, cost_pen_to_field=5.0)
    initial = ShepherdState(3, 7, settings)
    goal = ShepherdState(3, 7, settings)
    problem_same = ShepherdProblemAStar(initial, goal)
    solution_same = problem_same.search()
    print_solution("No Movement Needed (Start == Goal)", problem_same, solution_same)

    # 3. Moving everything back to field from both pens
    settings = Settings(a_max=5, b_max=5, cost_field_to_pen=60.0, cost_pen_to_pen=30.0, cost_pen_to_field=5.0)
    initial_full = ShepherdState(5, 5, settings)
    goal = ShepherdState(0, 0, settings)
    problem = ShepherdProblemAStar(initial_full, goal)
    solution = problem.search()
    print_solution("Full to Empty", problem, solution)

    # 4. Transferring all sheep from Pen A to Pen B
    settings = Settings(a_max=10, b_max=15, cost_field_to_pen=60.0, cost_pen_to_pen=30.0, cost_pen_to_field=5.0)
    initial = ShepherdState(10, 0, settings)
    goal = ShepherdState(0, 10, settings)
    problem = ShepherdProblemAStar(initial, goal)
    solution = problem.search()
    print_solution("All Sheep from A to B", problem, solution)

# Runs entire program
if __name__ == "__main__":
    run_general_problem()
    run_basic_problem()
    run_test_cases()
