def play_cellular_automaton(board: list[list[int]], num_gens: int, neighborhood_type: str, rules: dict) -> list[list[list[int]]]:
    """
    Simulates a cellular automaton based on the provided board, number of generations, neighborhood type, and rules.
    
    Args:
        board: A 2D list representing the initial state of the cellular automaton.
        num_gens: The number of generations to simulate.
        neighborhood_type: The type of neighborhood to use ("Moore" or "vonNeumann").
        rules: A dictionary mapping neighborhood strings to the next state of the cell.

    Returns:
        A list of 2D lists representing the state of the cellular automaton at each generation.
    """

    boards = []
    boards.append([row[:] for row in board])  # Store the initial state of the board

    for _ in range(num_gens):
        update_board(board, neighborhood_type, rules)
        boards.append([row[:] for row in board])

    return boards


def update_board(board: list[list[int]], neighborhood_type: str, rules: dict) -> None:
    """
    Updates the board to the next generation based on the neighborhood type and rules.
    
    Args:
        board: A 2D list representing the current state of the cellular automaton.
        neighborhood_type: The type of neighborhood to use ("Moore" or "vonNeumann").
        rules: A dictionary mapping neighborhood strings to the next state of the cell.
    
    Returns:
        None. The board is updated in place.
    """
    
    rows, columns = len(board), len(board[0])
    # Create a copy of the board to reference the original state while updating
    original = [row[:] for row in board]

    for r in range(rows):
        for c in range(columns):
            board[r][c] = update_cell(original, r, c, neighborhood_type, rules)


def update_cell(board: list[list[int]], r: int, c: int, neighborhood_type: str, rules: dict) -> int:
    """
    Updates the state of a cell based on its neighborhood and the provided rules.
    
    Args:
        board: A 2D list representing the current state of the cellular automaton.
        r: The row index of the cell to update.
        c: The column index of the cell to update.
        neighborhood_type: The type of neighborhood to use ("Moore" or "vonNeumann").
        rules: A dictionary mapping neighborhood strings to the next state of the cell.

    Returns:
        The next state of the cell.
    """
    
    neighborhood = neighborhood_to_string(board, r, c, neighborhood_type)

    try:
        return rules[neighborhood]
    except(KeyError):
        return 0 # Default to 0 (dead cell) if the neighborhood configuration is not found in the rules


def neighborhood_to_string(board: list[list[int]], r: int, c: int, neighborhood_type: str = "Moore") -> str:
    """
    Converts the neighborhood of a cell into a string representation based on the specified neighborhood type.
    
    Args:
        board: A 2D list representing the current state of the cellular automaton.
        r: The row index of the cell whose neighborhood is to be converted.
        c: The column index of the cell whose neighborhood is to be converted.
        neighborhood_type: The type of neighborhood to use ("Moore" or "vonNeumann").

    Returns:
        A string representing the neighborhood of the cell.
    Raises:
        ValueError: If an unsupported neighborhood type is provided.
    """

    if neighborhood_type == "Moore":
        neighbors = []
        neighbors.append(str(board[r][c])) # Include the state of the cell itself in the neighborhood string

        for i, j in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]: # Clockwise order starting from top-left
            if in_field(board, r + i, c + j): # Check if the neighbor is within bounds
                neighbors.append(str(board[r + i][c + j]))
            else:
                neighbors.append("0") # Treat out-of-bounds neighbors as dead cells
        return "".join(neighbors)
    
    elif neighborhood_type == "vonNeumann":
        neighbors = []
        neighbors.append(str(board[r][c])) # Include the state of the cell itself in the neighborhood string

        for i, j in [(-1, 0), (0, 1), (1, 0), (0, -1)]: # Clockwise order: up, right, down, left
            if in_field(board, r + i, c + j):
                neighbors.append(str(board[r + i][c + j]))
            else:
                neighbors.append("0") # Treat out-of-bounds neighbors as dead cells
        return "".join(neighbors)
    
    else:
        raise ValueError(f"Unsupported neighborhood type: {neighborhood_type}")


def in_field(board: list[list[int]], r: int, c: int) -> bool:
    """
    Checks if the position (r, c) is within the bounds of the board.

    Args:
        board: A 2D list representing the current state of the cellular automaton.
        r: The row index to check.
        c: The column index to check.

    Returns:
        True if the position is within the bounds of the board, False otherwise.
    """

    return 0 <= r < len(board) and 0 <= c < len(board[0])
