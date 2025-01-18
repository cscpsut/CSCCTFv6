from typing import List, Tuple, Optional, Dict
from collections import defaultdict
import copy

def solve_jigsaw(pieces: List[Tuple[int, int, int, int]], width: int = 10, height: int = 10, debug: bool = True) -> List[List[List[int]]]:
    attempts = 0
    all_solutions = []  # Store all valid solutions
    
    def categorize_pieces(pieces: List[Tuple[int, int, int, int]]) -> Dict[str, List[int]]:
        """Categorize pieces into corners, edges, and interior pieces using their indices."""
        categories = {
            'corners': [],
            'top_edge': [],
            'right_edge': [],
            'bottom_edge': [],
            'left_edge': [],
            'interior': []
        }
        
        for idx, piece in enumerate(pieces):
            zero_count = sum(1 for edge in piece if edge == 0)
            zero_positions = [i for i, edge in enumerate(piece) if edge == 0]
            
            if zero_count == 2:
                # Corner piece - check which corner based on zero positions
                if 0 in zero_positions and 3 in zero_positions:  # Top-left
                    categories['corners'].append(idx)
                elif 0 in zero_positions and 1 in zero_positions:  # Top-right
                    categories['corners'].append(idx)
                elif 1 in zero_positions and 2 in zero_positions:  # Bottom-right
                    categories['corners'].append(idx)
                elif 2 in zero_positions and 3 in zero_positions:  # Bottom-left
                    categories['corners'].append(idx)
            elif zero_count == 1:
                # Edge piece
                if piece[0] == 0:  # Top edge
                    categories['top_edge'].append(idx)
                elif piece[1] == 0:  # Right edge
                    categories['right_edge'].append(idx)
                elif piece[2] == 0:  # Bottom edge
                    categories['bottom_edge'].append(idx)
                elif piece[3] == 0:  # Left edge
                    categories['left_edge'].append(idx)
            else:
                # Interior piece
                categories['interior'].append(idx)
        
        if debug:
            print("\nPiece categorization:")
            for category, indices in categories.items():
                print(f"{category}: {len(indices)} pieces")
        
        return categories

    def is_valid_placement(grid: List[List[Optional[int]]], piece_idx: int, 
                          row: int, col: int) -> bool:
        """Check if a piece can be placed at the given position."""
        piece = pieces[piece_idx]
        
        # Check adjacent pieces
        if row > 0 and grid[row-1][col] is not None:  # Check top
            if pieces[grid[row-1][col]][2] + piece[0] != 0:
                return False
                
        if col < width-1 and grid[row][col+1] is not None:  # Check right
            if pieces[grid[row][col+1]][3] + piece[1] != 0:
                return False
                
        if row < height-1 and grid[row+1][col] is not None:  # Check bottom
            if pieces[grid[row+1][col]][0] + piece[2] != 0:
                return False
                
        if col > 0 and grid[row][col-1] is not None:  # Check left
            if pieces[grid[row][col-1]][1] + piece[3] != 0:
                return False
        
        return True

    def get_potential_pieces(row: int, col: int, remaining_pieces: Dict[str, List[int]], 
                           grid: List[List[Optional[int]]]) -> List[int]:
        """Get list of potential pieces for the current position."""
        potential_pieces = []
        
        # Determine position type
        is_corner = (row == 0 and col == 0) or (row == 0 and col == width-1) or \
                   (row == height-1 and col == 0) or (row == height-1 and col == width-1)
        is_edge = row == 0 or row == height-1 or col == 0 or col == width-1
        
        # Select appropriate piece category
        if is_corner:
            pieces_to_check = remaining_pieces['corners']
        elif is_edge:
            if row == 0:
                pieces_to_check = remaining_pieces['top_edge']
            elif row == height-1:
                pieces_to_check = remaining_pieces['bottom_edge']
            elif col == 0:
                pieces_to_check = remaining_pieces['left_edge']
            else:  # col == width-1
                pieces_to_check = remaining_pieces['right_edge']
        else:
            pieces_to_check = remaining_pieces['interior']
        
        # Check each piece in the appropriate category
        for piece_idx in pieces_to_check:
            if is_valid_placement(grid, piece_idx, row, col):
                potential_pieces.append(piece_idx)
        
        return potential_pieces

    def remove_piece(piece_idx: int, categories: Dict[str, List[int]]):
        """Remove a piece from its category."""
        for category in categories.values():
            if piece_idx in category:
                category.remove(piece_idx)
                return

    def add_piece(piece_idx: int, categories: Dict[str, List[int]]):
        """Add a piece back to its appropriate category."""
        piece = pieces[piece_idx]
        zero_count = sum(1 for edge in piece if edge == 0)
        zero_positions = [i for i, edge in enumerate(piece) if edge == 0]
        
        if zero_count == 2:
            categories['corners'].append(piece_idx)
        elif zero_count == 1:
            if piece[0] == 0:
                categories['top_edge'].append(piece_idx)
            elif piece[1] == 0:
                categories['right_edge'].append(piece_idx)
            elif piece[2] == 0:
                categories['bottom_edge'].append(piece_idx)
            else:  # piece[3] == 0
                categories['left_edge'].append(piece_idx)
        else:
            categories['interior'].append(piece_idx)

    def is_unique_solution(grid: List[List[int]]) -> bool:
        """Check if this solution is unique (not a rotation/reflection of existing solutions)."""
        current_solution = copy.deepcopy(grid)
        
        # Check against all existing solutions
        for existing_solution in all_solutions:
            # Check if solutions are identical
            if existing_solution == current_solution:
                return False
                
            # Check rotations (90, 180, 270 degrees)
            rotated = copy.deepcopy(current_solution)
            for _ in range(3):  # Check 3 rotations
                rotated = [list(x) for x in zip(*rotated[::-1])]  # Rotate 90 degrees
                if existing_solution == rotated:
                    return False
                    
            # Check reflections (horizontal and vertical)
            # Horizontal reflection
            reflected_h = [row[::-1] for row in current_solution]
            if existing_solution == reflected_h:
                return False
                
            # Vertical reflection
            reflected_v = current_solution[::-1]
            if existing_solution == reflected_v:
                return False
        
        return True

    def solve(grid: List[List[Optional[int]]], remaining_pieces: Dict[str, List[int]], 
             depth: int = 0) -> None:
        nonlocal attempts
        attempts += 1
        
        if attempts % 1000 == 0 and debug:
            print(f"Attempts: {attempts}, Depth: {depth}, Solutions found: {len(all_solutions)}")
            
        # Check if puzzle is complete
        if all(all(cell is not None for cell in row) for row in grid):
            if is_unique_solution(grid):
                all_solutions.append(copy.deepcopy(grid))
                if debug:
                    print(f"Found solution #{len(all_solutions)}!")
            return
            
        # Find next empty position
        row = col = 0
        found = False
        for i in range(height):
            for j in range(width):
                if grid[i][j] is None:
                    row, col = i, j
                    found = True
                    break
            if found:
                break
        
        # Get potential pieces for this position
        potential_pieces = get_potential_pieces(row, col, remaining_pieces, grid)
        
        if debug and depth == 0:
            print(f"Trying position ({row}, {col}), found {len(potential_pieces)} potential pieces")
        
        # Try each potential piece
        for piece_idx in potential_pieces:
            if debug and depth <= 1:
                print(f"Depth {depth}: Trying piece {piece_idx} at ({row}, {col})")
            
            # Place piece and recurse
            grid[row][col] = piece_idx
            remove_piece(piece_idx, remaining_pieces)
            
            solve(grid, remaining_pieces, depth + 1)
                
            # Backtrack
            grid[row][col] = None
            add_piece(piece_idx, remaining_pieces)

    # Initialize empty grid and categorize pieces
    grid = [[None for _ in range(width)] for _ in range(height)]
    piece_categories = categorize_pieces(pieces)
    
    if debug:
        print(f"Starting puzzle solver with {len(pieces)} pieces")
        
    solve(grid, piece_categories)
    
    if debug:
        print(f"\nSolver statistics:")
        print(f"Total attempts: {attempts}")
        print(f"Total solutions found: {len(all_solutions)}")
    
    return all_solutions

def print_puzzle(grid: List[List[int]], pieces: List[Tuple[int, int, int, int]]) -> None:
    if grid is None:
        print("No solution found!")
        return
        
    for row in grid:
        for piece_idx in row:
            print(f"{piece_idx}:{pieces[piece_idx]}", end=" ")
        print()

def print_all_solutions(solutions: List[List[List[int]]], pieces: List[Tuple[int, int, int, int]]) -> None:
    if not solutions:
        print("No solutions found!")
        return
        
    for i, solution in enumerate(solutions, 1):
        print(f"\nSolution {i}:")
        print_puzzle(solution, pieces)