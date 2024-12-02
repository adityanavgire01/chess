class ChessPiece:
    def __init__(self, color, type):
        self.color = color
        self.type = type
        self.has_moved = False

    def __repr__(self):
        return f"{self.color} {self.type}"

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self._initialize_board()
        self.current_player = 'white'

    def _initialize_board(self):
        # Set up pawns
        for col in range(8):
            self.board[1][col] = ChessPiece('white', 'pawn')
            self.board[6][col] = ChessPiece('black', 'pawn')
        
        # Set up rooks
        self.board[0][0] = ChessPiece('white', 'rook')
        self.board[0][7] = ChessPiece('white', 'rook')
        self.board[7][0] = ChessPiece('black', 'rook')
        self.board[7][7] = ChessPiece('black', 'rook')
        
        # Set up knights
        self.board[0][1] = ChessPiece('white', 'knight')
        self.board[0][6] = ChessPiece('white', 'knight')
        self.board[7][1] = ChessPiece('black', 'knight')
        self.board[7][6] = ChessPiece('black', 'knight')
        
        # Set up bishops
        self.board[0][2] = ChessPiece('white', 'bishop')
        self.board[0][5] = ChessPiece('white', 'bishop')
        self.board[7][2] = ChessPiece('black', 'bishop')
        self.board[7][5] = ChessPiece('black', 'bishop')
        
        # Set up queens
        self.board[0][3] = ChessPiece('white', 'queen')
        self.board[7][3] = ChessPiece('black', 'queen')
        
        # Set up kings
        self.board[0][4] = ChessPiece('white', 'king')
        self.board[7][4] = ChessPiece('black', 'king')

    def display_board(self):
        print("  a b c d e f g h")
        for i, row in enumerate(reversed(self.board), 1):
            print(f"{9-i}", end=" ")
            for piece in row:
                if piece:
                    print(self._get_piece_symbol(piece), end=" ")
                else:
                    print(".", end=" ")
            print(f"{9-i}")
        print("  a b c d e f g h")

    def _get_piece_symbol(self, piece):
        symbols = {
            'white': {'pawn': '♙', 'rook': '♖', 'knight': '♘', 'bishop': '♗', 'queen': '♕', 'king': '♔'},
            'black': {'pawn': '♟', 'rook': '♜', 'knight': '♞', 'bishop': '♝', 'queen': '♛', 'king': '♚'}
        }
        return symbols[piece.color][piece.type]

    def _find_king_position(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.type == 'king' and piece.color == color:
                    return row, col
        return None

    def is_in_check(self, color):
        king_pos = self._find_king_position(color)
        if not king_pos:
            return False

        opponent_color = 'black' if color == 'white' else 'white'
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == opponent_color:
                    # Check if this piece can attack the king
                    if self.is_valid_move(row, col, king_pos[0], king_pos[1]):
                        return True
        return False

    def is_checkmate(self, color):
        # If not in check, it's not a checkmate
        if not self.is_in_check(color):
            return False

        # Try all possible moves to see if any move gets out of check
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    for new_row in range(8):
                        for new_col in range(8):
                            if self.is_valid_move(row, col, new_row, new_col):
                                # Simulate the move
                                original_piece = self.board[new_row][new_col]
                                temp_piece = self.board[row][col]
                                self.board[new_row][new_col] = temp_piece
                                self.board[row][col] = None

                                # Check if this move resolves the check
                                still_in_check = self.is_in_check(color)

                                # Undo the move
                                self.board[row][col] = temp_piece
                                self.board[new_row][new_col] = original_piece

                                if not still_in_check:
                                    return False
        return True

    def _is_path_clear(self, start_row, start_col, end_row, end_col):
        # Check if the path between start and end is clear
        row_step = 0 if start_row == end_row else (1 if end_row > start_row else -1)
        col_step = 0 if start_col == end_col else (1 if end_col > start_col else -1)
        current_row, current_col = start_row + row_step, start_col + col_step
        while (current_row, current_col) != (end_row, end_col):
            if self.board[current_row][current_col] is not None:
                return False
            current_row += row_step
            current_col += col_step
        return True

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        destination = self.board[end_row][end_col]

        # Can't move to a square with a piece of the same color
        if destination and destination.color == piece.color:
            return False

        # Path blocking and basic piece-specific movement logic
        if piece.type == 'rook':
            # Rook moves in straight lines and path must be clear
            if start_row == end_row or start_col == end_col:
                return self._is_path_clear(start_row, start_col, end_row, end_col)

        elif piece.type == 'bishop':
            # Bishop moves diagonally and path must be clear
            if abs(start_row - end_row) == abs(start_col - end_col):
                return self._is_path_clear(start_row, start_col, end_row, end_col)

        elif piece.type == 'queen':
            # Queen moves in straight lines or diagonally and path must be clear
            if (start_row == end_row or 
                start_col == end_col or 
                abs(start_row - end_row) == abs(start_col - end_col)):
                return self._is_path_clear(start_row, start_col, end_row, end_col)

        elif piece.type == 'pawn':
            # White pawns move up, black pawns move down
            direction = 1 if piece.color == 'white' else -1
            
            # Standard one-square move
            if start_col == end_col and start_row + direction == end_row and not destination:
                return True
            
            # Initial two-square move
            if not piece.has_moved and start_col == end_col and start_row + 2*direction == end_row and not destination:
                return True
            
            # Diagonal capture
            if abs(start_col - end_col) == 1 and start_row + direction == end_row and destination:
                return True

        elif piece.type == 'knight':
            # Knight moves in L-shape
            row_diff = abs(start_row - end_row)
            col_diff = abs(start_col - end_col)
            return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

        elif piece.type == 'king':
            # King can move one square in any direction
            return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1

        return False

    def move_piece(self, start, end):
        # Convert algebraic notation to array indices
        start_col = ord(start[0].lower()) - ord('a')
        start_row = int(start[1]) - 1
        end_col = ord(end[0].lower()) - ord('a')
        end_row = int(end[1]) - 1

        # Validate move (considering check and current player)
        piece = self.board[start_row][start_col]
        if not piece or piece.color != self.current_player:
            print("Invalid move: Not your piece or not your turn.")
            return False

        if not self.is_valid_move(start_row, start_col, end_row, end_col):
            print("Invalid move for this piece.")
            return False

        # Simulate move to check if it resolves or causes check
        original_piece = self.board[end_row][end_col]
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = None

        # Mark piece as moved
        piece.has_moved = True

        # Check if move puts own king in check
        if self.is_in_check(self.current_player):
            # Undo move
            self.board[start_row][start_col] = piece
            self.board[end_row][end_col] = original_piece
            print("Invalid move: Cannot move into check.")
            return False

        # Check for checkmate
        opponent_color = 'black' if self.current_player == 'white' else 'white'
        if self.is_checkmate(opponent_color):
            print(f"CHECKMATE! {self.current_player.capitalize()} wins!")
            return "CHECKMATE"

        # Switch players
        self.current_player = opponent_color
        return True

def play_chess():
    board = ChessBoard()

    while True:
        board.display_board()
        print(f"{board.current_player.capitalize()}'s turn")
        
        start = input("Enter the piece to move (e.g., 'e2'): ")
        end = input("Enter the destination (e.g., 'e4'): ")

        result = board.move_piece(start, end)
        
        if result == "CHECKMATE":
            board.display_board()
            break
        elif not result:
            print("Invalid move. Try again.")

if __name__ == "__main__":
    play_chess()