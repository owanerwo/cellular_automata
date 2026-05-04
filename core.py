def play_cellular_automaton(board: list[list[int]], num_gens: int, neighborhood_type: str, rules: dict) -> list[list[list[int]]]:

    boards = []
    boards.append([row[:] for row in board])  # Store the initial state of the board

    for _ in range(num_gens):
        update_board(board, neighborhood_type, rules)
        boards.append([row[:] for row in board])

    return boards


def update_board(board: list[list[int]], neighborhood_type: str, rules: dict) -> None:
    
    rows, columns = len(board), len(board[0])
    # Create a copy of the board to reference the original state while updating
    original = [row[:] for row in board]

    for r in range(rows):
        for c in range(columns):
            board[r][c] = update_cell(original, r, c, neighborhood_type, rules)


def update_cell(board: list[list[int]], r: int, c: int, neighborhood_type: str, rules: dict) -> int:
    
    neighborhood = neighborhood_to_string(board, r, c, neighborhood_type)
    return rules[neighborhood]


def neighborhood_to_string(board: list[list[int]], r: int, c: int, neighborhood_type: str = "Moore") -> str:

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
    """
    return 0 <= r < len(board) and 0 <= c < len(board[0])
