import numpy as np
import matplotlib.pyplot as plt
import random
import sympy as sp
from scipy.optimize import minimize
from itertools import permutations, combinations
from multiprocessing import Pool

# First thing to do is create a 6x6 box
chessboard = [
    ["A", "B", "B", "C", "C", "C"],
    ["A", "B", "B", "C", "C", "C"],
    ["A", "A", "B", "B", "C", "C"],
    ["A", "A", "B", "B", "C", "C"],
    ["A", "A", "A", "B", "B", "C"],
    ["A", "A", "A", "B", "B", "C"]
]
size = len(chessboard)


# Define the possible moves within the chessboard
def horse_move(pos: tuple):
    i = pos[0]
    j = pos[1]
    possible_moves = [(i + 1, j + 2), (i + 1, j - 2), (i - 1, j + 2), (i - 1, j - 2), (i + 2, j + 1), (i + 2, j - 1),
                      (i - 2, j + 1), (i - 2, j - 1)]
    possible_moves = [tup for tup in possible_moves if 0 <= tup[0] <= size - 1 and 0 <= tup[1] <= size - 1]
    return possible_moves


# Remove a point already visited
def remove_already_visited(possible_moves, forbidden_moves):
    return [i for i in possible_moves if i not in forbidden_moves]


# Define the jumper
def random_selector(lista):
    if len(lista) == 0:
        return []
    else:
        return random.choice(lista)


# Define the path generator
def path_generator(start: tuple, end: tuple):
    position = start
    forbidden_moves = []
    path = []
    path.append(start)
    forbidden_moves.append(start)
    while position != end:
        possible_moves = horse_move(position)
        possible_moves = remove_already_visited(possible_moves, forbidden_moves)
        position = random_selector(possible_moves)
        if not position:
            position = start
            forbidden_moves = []
            path = []
            path.append(start)
            forbidden_moves.append(start)
        else:
            forbidden_moves.append(position)
            path.append(position)
    return path


# Define the scorer for a given path:
def path_to_list(path, grid=None):
    if grid is None:
        grid = chessboard
    elements = [grid[i][j] for i, j in path]
    return elements


# Define a scoring function
def calculate_symbolic_score(elements):
    # Create symbolic variables
    A = sp.symbols('A')
    B = sp.symbols('B')
    C = sp.symbols('C')

    # Initialize the score
    score = sp.symbols(elements[0])

    # Iterate through the list
    for i in range(len(elements) - 1):
        current_value = elements[i]
        next_value = elements[i + 1]

        if current_value != next_value:
            # Move to a different value: multiply
            score *= sp.Symbol(next_value)
        else:
            # Move to the same value: increment
            score += sp.Symbol(next_value)

    return score


def calculate_actual_score(elements, a, b, c):
    # Create symbolic variables
    dictionary = {'A': a, 'B': b, 'C': c}
    numbers = [dictionary[letter] for letter in elements]
    # Initialize the score
    score = numbers[0]

    # Iterate through the list
    for i in range(len(elements) - 1):
        current_value = numbers[i]
        next_value = numbers[i + 1]

        if current_value != next_value:
            # Move to a different value: multiply
            score *= next_value
        else:
            # Move to the same value: increment
            score += next_value

    return score

def minimizer(letteral_poly):
    target_value = 2024
    solutions = []

    # Set the range for A, B, and C
    max_value = 7

    # Iterate over possible values of A, B, and C
    for a in range(1, max_value):
        for b in range(1, max_value):
            if b == a:
                continue
            for c in range(1, max_value):
                if c == b or c == a:
                    continue
                # Substitute values into the expression
                value = letteral_poly.subs({'A': a, 'B': b, 'C': c})

                # Check if the expression evaluates to the target value
                if value == target_value:
                    solutions.append((a, b, c))
                    total_a_b_c = a + b + c
                    return solutions

    return "I failed"


# Funzione per colorare la scacchiera coi numeri trovati
def replace_values(board, values):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "A":
                board[i][j] = values[0]
            elif board[i][j] == "B":
                board[i][j] = values[1]
            elif board[i][j] == "C":
                board[i][j] = values[2]
    return board


def il_grande_main():
    list_of_attempted_path = []
    check = "I failed"
    counter = 0
    while check == "I failed" and counter < 1000:
        counter += 1
        #while best_params is None and score_num > 50:
        first_path = path_generator((0, 0), (5, 5))
        list_of_attempted_path.append(first_path)
        list_of_letter_first = path_to_list(first_path)
        score_first = calculate_symbolic_score(list_of_letter_first)
        best_params_first = minimizer(score_first)
        check = best_params_first
        print(first_path)
        print(list_of_letter_first)
        print(score_first)
        print(best_params_first)
    if counter == 100:
        return "Diocane, more counters"
    numbers = best_params_first[0]
    # Esegui la sostituzione
    new_chessboard = np.array(replace_values(chessboard, numbers))

    total_sum = 0
    counter = 0
    while total_sum != 2024 and counter < 1000:
        counter += 1
        second_path = path_generator((0, 5), (5, 0))
        # Select the elements using the indices
        selected_elements = [new_chessboard[i, j] for i, j in second_path]
    #    Calculate the sum of the selected elements
        total_sum = sum(selected_elements)
        if total_sum != 2024:
            print("Nope, try again")
    if counter == 100:
        print("Diocane, more counters in second loop")
        return 0

    print('voila')
    print(first_path)
    print(second_path)
    print(numbers)
    return second_path, first_path

il_grande_main()

