def solve_sudoku_all(board, solutions, max_solutions=2):
    """
    Finds all solutions for a Sudoku board.
    :param board: List of integers representing the Sudoku board (0 for empty spaces)
    :param solutions: List to store all found solutions
    :param max_solutions: Stop searching after finding this many solutions
    :return: None
    """
    empty_cell = find_empty(board)
    if not empty_cell:
        # No empty cells left, solution found
        solutions.append(board[:])  # Add a copy of the current board
        return len(solutions) < max_solutions  # Stop if max_solutions reached

    row, col = empty_cell

    for num in range(1, 10):  # Try numbers 1 through 9
        if is_valid(board, row, col, num):
            board[row * 9 + col] = num  # Place the number
            if not solve_sudoku_all(board, solutions, max_solutions):
                return False  # Stop if max_solutions reached
            board[row * 9 + col] = 0  # Reset if not solvable

    return True


def is_valid(board, row, col, num):
    """
    Checks if placing num in board[row][col] is valid.
    """
    for c in range(9):
        if board[row * 9 + c] == num:
            return False
    for r in range(9):
        if board[r * 9 + col] == num:
            return False
    start_row = row // 3 * 3
    start_col = col // 3 * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r * 9 + c] == num:
                return False
    return True


def find_empty(board):
    """
    Finds an empty cell in the Sudoku board.
    """
    for i in range(81):
        if board[i] == 0:
            return divmod(i, 9)
    return None


def print_board(board):
    """
    Prints the Sudoku board in a 9x9 grid format.
    """
    for r in range(9):
        for c in range(9):
            print(board[r * 9 + c] if board[r * 9 + c] != 0 else '.', end=' ')
        print()


# Example usage:
if __name__ == "__main__":
    puzzle = [
        2, 0, 0, 0, 0, 0, 0, 0, 9,
        0, 0, 6, 8, 0, 7, 4, 0, 0,
        0, 4, 0, 0, 6, 0, 0, 2, 0,
        0, 5, 0, 0, 0, 0, 0, 3, 0,
        0, 0, 2, 0, 0, 0, 7, 0, 0,
        0, 7, 0, 0, 0, 0, 0, 8, 0,
        0, 9, 0, 0, 8, 0, 0, 6, 0,
        0, 0, 1, 7, 0, 2, 5, 0, 0,
        7, 0, 0, 0, 0, 0, 0, 0, 3,
    ]

    print("Original Sudoku:")
    print_board(puzzle)

    solutions = []
    solve_sudoku_all(puzzle, solutions, max_solutions=2)

    if len(solutions) == 0:
        print("\nNo solutions exist!")
    elif len(solutions) == 1:
        print("\nUnique solution:")
        print_board(solutions[0])
    else:
        print(f"\nMultiple solutions found ({len(solutions)}):")
        print("Solution 1:")
        print_board(solutions[0])
        print("\nSolution 2:")
        print_board(solutions[1])