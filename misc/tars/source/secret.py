from dataclasses import dataclass
from typing import List, Optional, Set, Tuple, Dict, Generator
import random
from collections import deque


@dataclass(frozen=True)
class PuzzlePiece:
    """Represents a single jigsaw puzzle piece with indents/outdents on each side."""
    top: int
    right: int
    bottom: int
    left: int

    def to_list(self) -> List[int]:
        """Returns the piece's edges as a list in order [top, right, bottom, left]."""
        return [self.top, self.right, self.bottom, self.left]

    # def __eq__(self, other) -> bool:
    #     if not isinstance(other, PuzzlePiece):
    #         return NotImplemented
    #     return (self.top == other.top and 
    #             self.right == other.right and 
    #             self.bottom == other.bottom and 
    #             self.left == other.left)

    # def __hash__(self) -> int:
    #     return hash((self.top, self.right, self.bottom, self.left))

class Puzzle:
    def __init__(self, height: int, width: int, num_indent_types: Optional[int] = None):
        """Initialize an empty puzzle with given dimensions.
        If num_indent_types is provided, generates a complete random puzzle."""
        self.height = height
        self.width = width
        self.grid: List[List[Optional[PuzzlePiece]]] = [[None] * width for _ in range(height)]
        
        if num_indent_types is not None:
            self.num_indent_types = num_indent_types
            self._generate_puzzle()

    def _generate_puzzle(self) -> None:
        """Internal method to generate the puzzle pieces."""
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] is not None:
                    continue
                    
                top = bottom = left = right = 0
                
                if row == 0:
                    top = 0
                elif self.grid[row-1][col] is not None:
                    top = -self.grid[row-1][col].bottom
                else:
                    top = random.randint(1, self.num_indent_types) * random.choice([-1, 1])
                    
                if col == 0:
                    left = 0
                elif self.grid[row][col-1] is not None:
                    left = -self.grid[row][col-1].right
                else:
                    left = random.randint(1, self.num_indent_types) * random.choice([-1, 1])
                    
                if row == self.height - 1:
                    bottom = 0
                else:
                    bottom = random.randint(1, self.num_indent_types) * random.choice([-1, 1])
                    
                if col == self.width - 1:
                    right = 0
                else:
                    right = random.randint(1, self.num_indent_types) * random.choice([-1, 1])
                    
                self.grid[row][col] = PuzzlePiece(top, right, bottom, left)

    def add_piece(self, piece: PuzzlePiece, row: int, col: int) -> bool:
        """Add a piece to the specified position. Returns False if position is invalid or already occupied."""
        if not (0 <= row < self.height and 0 <= col < self.width):
            return False
        if self.grid[row][col] is not None:
            return False
        
        # Check if piece fits with neighbors
        if row > 0 and self.grid[row-1][col] is not None:  # Check top
            if piece.top != -self.grid[row-1][col].bottom:
                return False
        if col > 0 and self.grid[row][col-1] is not None:  # Check left
            if piece.left != -self.grid[row][col-1].right:
                return False
        if row < self.height-1 and self.grid[row+1][col] is not None:  # Check bottom
            if piece.bottom != -self.grid[row+1][col].top:
                return False
        if col < self.width-1 and self.grid[row][col+1] is not None:  # Check right
            if piece.right != -self.grid[row][col+1].left:
                return False
        
        if row == 0 and piece.top != 0:
            return False
        if col == 0 and piece.left != 0:
            return False
        if row == self.height-1 and piece.bottom != 0:
            return False
        if col == self.width-1 and piece.right != 0:
            return False

        self.grid[row][col] = piece
        return True
    
    def remove_piece(self, row: int, col: int) -> bool:
        """Remove the piece at the specified position."""
        if not (0 <= row < self.height and 0 <= col < self.width):
            return False
        if self.grid[row][col] is None:
            return False
        self.grid[row][col] = None
        return True
    
    def get_piece(self, row: int, col: int) -> Optional[PuzzlePiece]:
        """Get the piece at the specified position."""
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col]
        return None

    def __eq__(self, other: 'Puzzle') -> bool:
        """Check if two puzzles are identical (same size and same piece objects in same positions)."""
        if not isinstance(other, Puzzle):
            return NotImplemented
        if self.height != other.height or self.width != other.width:
            return False
        return all(
            self.grid[row][col] is other.grid[row][col]
            for row in range(self.height)
            for col in range(self.width)
        )

    def is_partial_match(self, other: 'Puzzle') -> bool:
        """Check if this puzzle matches another puzzle in all positions where both have pieces."""
        if not isinstance(other, Puzzle):
            return False
        if self.height != other.height or self.width != other.width:
            return False
            
        for row in range(self.height):
            for col in range(self.width):
                self_piece = self.grid[row][col]
                other_piece = other.grid[row][col]
                if self_piece is not None and other_piece is not None:
                    if self_piece is not other_piece:
                        return False
        return True


    def __str__(self) -> str:
        """Returns a string representation of the puzzle showing all pieces and their connections."""
        result = []
        for row in self.grid:
            row_data = [piece.to_list() if piece else [' ',' ',' ',' '] for piece in row]
            zipped = list(zip(*row_data))
            result.append(' '.join(str(x).center(8) for x in zipped[0]))
            side_edges = []
            for l, r in zip(zipped[3], zipped[1]):
                l = str(l).ljust(2)
                r = str(r).rjust(2)
                side_edges.append(f'{l}  {r}')
            result.append('   '.join(side_edges))
            result.append(' '.join(str(x).center(8) for x in zipped[2]))
            result.append('')
        return '\n'.join(result)
