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

    def move_piece(self, start, end):
        # Convert algebraic notation to array indices
        start_col = ord(start[0].lower()) - ord('a')
        start_row = int(start[1]) - 1
        end_col = ord(end[0].lower()) - ord('a')
        end_row = int(end[1]) - 1

        # Validate move (very basic for now)
        piece = self.board[start_row][start_col]
        if piece:
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = None
            return True
        return False

def play_chess():
    board = ChessBoard()
    current_player = 'white'

    while True:
        board.display_board()
        print(f"{current_player.capitalize()}'s turn")
        
        start = input("Enter the piece to move (e.g., 'e2'): ")
        end = input("Enter the destination (e.g., 'e4'): ")

        if board.move_piece(start, end):
            # Switch players
            current_player = 'black' if current_player == 'white' else 'white'
        else:
            print("Invalid move. Try again.")

if __name__ == "__main__":
    play_chess()