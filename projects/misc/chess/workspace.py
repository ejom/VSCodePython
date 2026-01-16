import itertools
import copy

# Using simple characters to represent pieces for text-based display
PIECE_SYMBOLS = {
    'white': {'pawn': 'P', 'rook': 'R', 'knight': 'N', 'bishop': 'B', 'queen': 'Q', 'king': 'K'},
    'black': {'pawn': 'p', 'rook': 'r', 'knight': 'n', 'bishop': 'b', 'queen': 'q', 'king': 'k'}
}

class Piece:
    """Represents a single chess piece."""
    def __init__(self, piece_type, color):
        if color not in ['white', 'black']:
            raise ValueError("Invalid color for piece.")
        if piece_type not in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
            raise ValueError("Invalid piece type.")
            
        self.type = piece_type
        self.color = color
        self.symbol = PIECE_SYMBOLS[color][piece_type]

    def __str__(self):
        return self.symbol

class Chess4D:
    """Manages the state and rules of the 4D chess game."""

    def __init__(self):
        """Initializes the 4D board and sets up the pieces."""
        self.board = [[[[None for _ in range(8)] for _ in range(8)] for _ in range(2)] for _ in range(2)]
        self.turn = 'white'
        self._setup_board()
        self.king_pos = self._find_all_kings()

    def _setup_board(self):
        """Places all pieces on all 4 boards for the start of the game."""
        for bx in range(2):
            for by in range(2):
                # Setup black pieces
                self.board[bx][by][6] = [Piece('pawn', 'black') for _ in range(8)]
                self.board[bx][by][7][0] = Piece('rook', 'black')
                self.board[bx][by][7][7] = Piece('rook', 'black')
                self.board[bx][by][7][1] = Piece('knight', 'black')
                self.board[bx][by][7][6] = Piece('knight', 'black')
                self.board[bx][by][7][2] = Piece('bishop', 'black')
                self.board[bx][by][7][5] = Piece('bishop', 'black')
                self.board[bx][by][7][3] = Piece('queen', 'black')
                self.board[bx][by][7][4] = Piece('king', 'black')

                # Setup white pieces
                self.board[bx][by][1] = [Piece('pawn', 'white') for _ in range(8)]
                self.board[bx][by][0][0] = Piece('rook', 'white')
                self.board[bx][by][0][7] = Piece('rook', 'white')
                self.board[bx][by][0][1] = Piece('knight', 'white')
                self.board[bx][by][0][6] = Piece('knight', 'white')
                self.board[bx][by][0][2] = Piece('bishop', 'white')
                self.board[bx][by][0][5] = Piece('bishop', 'white')
                self.board[bx][by][0][3] = Piece('queen', 'white')
                self.board[bx][by][0][4] = Piece('king', 'white')
    
    def _find_all_kings(self):
        """Finds the initial positions of all kings on the board."""
        positions = {'white': [], 'black': []}
        for bx, by, r, f in itertools.product(range(2), range(2), range(8), range(8)):
            piece = self.get_piece((bx, by, r, f))
            if piece and piece.type == 'king':
                positions[piece.color].append((bx, by, r, f))
        return positions

    def display_board(self):
        """Prints the current state of all four boards."""
        print("\n" + "="*40)
        print(f"            TURN: {self.turn.upper()}")
        print("="*40)

        for by in range(1, -1, -1): # Print top boards (y=1) then bottom boards (y=0)
            print(f"\n----- BOARD LAYER Y = {by} -----")
            # Print header for two boards side-by-side
            print(f"   BOARD (0,{by})              BOARD (1,{by})")
            print("  a b c d e f g h          a b c d e f g h")
            print(" +-----------------+      +-----------------+")

            for r in range(7, -1, -1):
                # Print rank number for left board
                print(f"{r+1}|", end=" ")
                # Print pieces for left board (0, by)
                for f in range(8):
                    piece = self.board[0][by][r][f]
                    print(f"{piece.symbol if piece else '.'}", end=" ")
                print(f"|{r+1}", end="    ")
                
                # Print rank number for right board
                print(f"{r+1}|", end=" ")
                # Print pieces for right board (1, by)
                for f in range(8):
                    piece = self.board[1][by][r][f]
                    print(f"{piece.symbol if piece else '.'}", end=" ")
                print(f"|{r+1}")

            print(" +-----------------+      +-----------------+")
            print("  a b c d e f g h          a b c d e f g h")
        print("="*40 + "\n")

    def get_piece(self, pos):
        """Returns the piece at a given 4D position."""
        bx, by, r, f = pos
        return self.board[bx][by][r][f]

    def _is_in_bounds(self, pos):
        """Checks if a position is within the 2x2x8x8 board."""
        bx, by, r, f = pos
        return 0 <= bx <= 1 and 0 <= by <= 1 and 0 <= r <= 7 and 0 <= f <= 7

    def _get_pseudo_legal_moves(self, pos):
        """Generates all possible moves for a piece, not accounting for check."""
        piece = self.get_piece(pos)
        if not piece:
            return []
        
        moves = []
        # Dispatch to the correct move generation function based on piece type
        move_functions = {
            'pawn': self._get_pawn_moves, 'rook': self._get_rook_moves,
            'knight': self._get_knight_moves, 'bishop': self._get_bishop_moves,
            'queen': self._get_queen_moves, 'king': self._get_king_moves
        }
        return move_functions[piece.type](pos, piece.color)

    def get_legal_moves(self, pos):
        """Filters pseudo-legal moves to only include fully legal moves (those that don't result in check)."""
        piece = self.get_piece(pos)
        if not piece: return []
        
        pseudo_moves = self._get_pseudo_legal_moves(pos)
        legal_moves = []

        for move in pseudo_moves:
            # Simulate the move
            temp_game = copy.deepcopy(self)
            temp_game._execute_move(pos, move)
            
            # If the move does not put the current player's king in check, it's legal
            if not temp_game.is_in_check(piece.color):
                legal_moves.append(move)
        
        return legal_moves

    # --- Piece-Specific Move Generation ---
    
    def _get_sliding_moves(self, pos, color, directions):
        """Generic function for sliding pieces (Rook, Bishop, Queen)."""
        moves = []
        bx, by, r, f = pos
        for d in directions:
            dbx, dby, dr, df = d
            for i in range(1, 8):
                next_pos = (bx + i*dbx, by + i*dby, r + i*dr, f + i*df)
                if not self._is_in_bounds(next_pos):
                    break
                
                target_piece = self.get_piece(next_pos)
                if target_piece is None:
                    moves.append(next_pos)
                else:
                    if target_piece.color != color:
                        moves.append(next_pos) # Can capture
                    break # Blocked
        return moves

    def _get_rook_moves(self, pos, color):
        directions = [(1,0,0,0), (-1,0,0,0), (0,1,0,0), (0,-1,0,0),
                      (0,0,1,0), (0,0,-1,0), (0,0,0,1), (0,0,0,-1)]
        return self._get_sliding_moves(pos, color, directions)
    
    def _get_bishop_moves(self, pos, color):
        directions = []
        # Any combination of 2 dimensions
        for dims in itertools.combinations(range(4), 2):
            for signs in itertools.product([-1, 1], repeat=2):
                d = [0,0,0,0]
                d[dims[0]] = signs[0]
                d[dims[1]] = signs[1]
                directions.append(tuple(d))
        return self._get_sliding_moves(pos, color, directions)
        
    def _get_queen_moves(self, pos, color):
        directions = []
        # Any combination of 1, 2, 3, or 4 dimensions
        for i in range(1, 5):
            for dims in itertools.combinations(range(4), i):
                for signs in itertools.product([-1, 1], repeat=i):
                    d = [0,0,0,0]
                    for idx, dim in enumerate(dims):
                        d[dim] = signs[idx]
                    directions.append(tuple(d))
        return self._get_sliding_moves(pos, color, directions)

    def _get_knight_moves(self, pos, color):
        moves = []
        bx, by, r, f = pos
        # Iterate through all pairs of dimensions
        for d1, d2 in itertools.combinations(range(4), 2):
            for s1, s2 in itertools.product([-1, 1], repeat=2):
                # Hop of 2 in one dim, 1 in the other
                for hop in [(1, 2), (2, 1)]:
                    d = [0,0,0,0]
                    d[d1], d[d2] = hop[0] * s1, hop[1] * s2
                    
                    # Knight moves using a board axis must use it for the 1-step
                    if (d1 < 2 and hop[0] == 2) or (d2 < 2 and hop[1] == 2):
                        continue
                        
                    next_pos = (bx+d[0], by+d[1], r+d[2], f+d[3])
                    
                    if self._is_in_bounds(next_pos):
                        target = self.get_piece(next_pos)
                        if target is None or target.color != color:
                            moves.append(next_pos)
        return moves

    def _get_king_moves(self, pos, color):
        moves = []
        _, _, r, f = pos # Kings cannot change boards
        # All adjacent squares on the same board
        for dr, df in itertools.product([-1, 0, 1], repeat=2):
            if dr == 0 and df == 0: continue
            
            next_pos = (pos[0], pos[1], r + dr, f + df)
            
            if self._is_in_bounds(next_pos):
                target = self.get_piece(next_pos)
                if target is None or target.color != color:
                    moves.append(next_pos)
        return moves

    def _get_pawn_moves(self, pos, color):
        moves = []
        bx, by, r, f = pos
        
        # Determine forward direction based on color
        forward_r = 1 if color == 'white' else -1
        start_rank = 1 if color == 'white' else 6
        
        # 1. Standard forward move (1D, on same board)
        one_step = (bx, by, r + forward_r, f)
        if self._is_in_bounds(one_step) and self.get_piece(one_step) is None:
            moves.append(one_step)
            # 2. Double forward move from start
            if r == start_rank:
                two_steps = (bx, by, r + 2 * forward_r, f)
                if self._is_in_bounds(two_steps) and self.get_piece(two_steps) is None:
                    moves.append(two_steps)

        # 3. Standard diagonal capture (2D, on same board)
        for df in [-1, 1]:
            capture_pos = (bx, by, r + forward_r, f + df)
            if self._is_in_bounds(capture_pos):
                target = self.get_piece(capture_pos)
                if target and target.color != color:
                    moves.append(capture_pos)
        
        # 4. Special 4D Moves (as per prompt)
        # 4a. Move "up a board" (1D move in 'by' dimension)
        # Let's define "up" as positive 'by' for white, negative for black
        forward_by = 1 if color == 'white' else -1
        up_pos = (bx, by + forward_by, r, f)
        if self._is_in_bounds(up_pos) and self.get_piece(up_pos) is None:
             moves.append(up_pos)

        # 4b. Capture forward in rank and "up" a board (2D capture)
        capture_up_r = (bx, by + forward_by, r + forward_r, f)
        if self._is_in_bounds(capture_up_r):
            target = self.get_piece(capture_up_r)
            if target and target.color != color:
                moves.append(capture_up_r)
        
        # 4c. Capture on same r/f but diagonal board (2D capture)
        for dbx, dby in itertools.product([-1, 1], repeat=2):
            capture_diag_board = (bx + dbx, by + dby, r, f)
            if self._is_in_bounds(capture_diag_board):
                target = self.get_piece(capture_diag_board)
                if target and target.color != color:
                    moves.append(capture_diag_board)
        
        return moves

    def is_square_attacked(self, pos, attacker_color):
        """Checks if a given square is under attack by the opposing color."""
        # Check for attacks from all piece types
        # This is like asking: "can any enemy piece move to this square?"
        
        # Pawn attacks
        pawn_dir_r = 1 if attacker_color == 'black' else -1
        pawn_dir_by = 1 if attacker_color == 'black' else -1
        # Standard attacks
        for df in [-1, 1]:
            attacker_pos = (pos[0], pos[1], pos[2] + pawn_dir_r, pos[3] + df)
            if self._is_in_bounds(attacker_pos):
                p = self.get_piece(attacker_pos)
                if p and p.type == 'pawn' and p.color == attacker_color: return True
        # 4D attacks
        attacker_pos_4d_1 = (pos[0], pos[1] + pawn_dir_by, pos[2] + pawn_dir_r, pos[3])
        if self._is_in_bounds(attacker_pos_4d_1):
            p = self.get_piece(attacker_pos_4d_1)
            if p and p.type == 'pawn' and p.color == attacker_color: return True
        for dbx, dby in itertools.product([-1, 1], repeat=2):
            attacker_pos_4d_2 = (pos[0] + dbx, pos[1] + dby, pos[2], pos[3])
            if self._is_in_bounds(attacker_pos_4d_2):
                p = self.get_piece(attacker_pos_4d_2)
                if p and p.type == 'pawn' and p.color == attacker_color: return True

        # Knight attacks
        for k_move in self._get_knight_moves(pos, 'white'): # color doesn't matter for geometry
             p = self.get_piece(k_move)
             if p and p.type == 'knight' and p.color == attacker_color: return True

        # King attacks
        for ki_move in self._get_king_moves(pos, 'white'):
             p = self.get_piece(ki_move)
             if p and p.type == 'king' and p.color == attacker_color: return True
             
        # Sliding piece attacks (Rook, Bishop, Queen)
        rook_like_attackers = self._get_rook_moves(pos, 'white')
        bishop_like_attackers = self._get_bishop_moves(pos, 'white')

        for move in rook_like_attackers:
            p = self.get_piece(move)
            if p and p.color == attacker_color and (p.type == 'rook' or p.type == 'queen'):
                return True
        for move in bishop_like_attackers:
            p = self.get_piece(move)
            if p and p.color == attacker_color and (p.type == 'bishop' or p.type == 'queen'):
                return True
        
        return False

    def is_in_check(self, color):
        """Checks if any king of the given color is currently in check."""
        opponent = 'black' if color == 'white' else 'white'
        for king_pos in self.king_pos[color]:
            if self.is_square_attacked(king_pos, opponent):
                return True
        return False
        
    def _execute_move(self, start_pos, end_pos):
        """Executes a move on the board without validation."""
        piece = self.get_piece(start_pos)
        target_piece = self.get_piece(end_pos)
        
        # If a king is captured, remove it from the tracking list
        if target_piece and target_piece.type == 'king':
            self.king_pos[target_piece.color].remove(end_pos)
        
        self.board[end_pos[0]][end_pos[1]][end_pos[2]][end_pos[3]] = piece
        self.board[start_pos[0]][start_pos[1]][start_pos[2]][start_pos[3]] = None
        
        # If the piece moved was a king, update its position
        if piece.type == 'king':
            self.king_pos[piece.color].remove(start_pos)
            self.king_pos[piece.color].append(end_pos)

    def has_any_legal_moves(self, color):
        """Checks if a player has at least one legal move."""
        for bx, by, r, f in itertools.product(range(2), range(2), range(8), range(8)):
            piece = self.get_piece((bx, by, r, f))
            if piece and piece.color == color:
                if self.get_legal_moves((bx, by, r, f)):
                    return True
        return False
        
    def check_game_over(self):
        """Checks for game-ending conditions (checkmate or no kings left)."""
        opponent = 'black' if self.turn == 'white' else 'white'
        
        # Condition 1: Player has no kings left
        if not self.king_pos[self.turn]:
            print(f"Game Over! {self.turn} has no kings left. {opponent.capitalize()} wins!")
            return True
            
        # Condition 2: Player's last king is in checkmate
        if len(self.king_pos[self.turn]) == 1:
            if self.is_in_check(self.turn) and not self.has_any_legal_moves(self.turn):
                print(f"Checkmate! {opponent.capitalize()} wins!")
                return True
        
        # Condition 3: Stalemate
        if not self.is_in_check(self.turn) and not self.has_any_legal_moves(self.turn):
             print("Stalemate! The game is a draw.")
             return True

        return False

    def play(self):
        """The main game loop."""
        while True:
            self.display_board()
            
            # Check for game over condition *before* the player moves
            if self.check_game_over():
                break

            if self.is_in_check(self.turn):
                print(f"{self.turn.capitalize()} is in check!")

            # Get player input
            try:
                move_input = input(f"{self.turn.capitalize()}'s move (bx1 by1 r1 f1 bx2 by2 r2 f2): ")
                coords = [int(c) for c in move_input.split()]
                if len(coords) != 8: raise ValueError
                # Adjust rank from 1-8 to 0-7, file from letter to 0-7
                start_pos = (coords[0], coords[1], coords[2], coords[3])
                end_pos = (coords[4], coords[5], coords[6], coords[7])
                
                # Validate the move
                piece = self.get_piece(start_pos)
                if not piece or piece.color != self.turn:
                    print("Error: No piece of your color at the start position.")
                    continue
                
                legal_moves = self.get_legal_moves(start_pos)
                if end_pos not in legal_moves:
                    print("Error: That is not a legal move.")
                    continue
                
                # Make the move
                self._execute_move(start_pos, end_pos)
                
                # Switch turns
                self.turn = 'black' if self.turn == 'white' else 'white'

            except (ValueError, IndexError):
                print("Invalid input. Please use the format: 0 0 1 4 0 0 3 4")
                continue

if __name__ == '__main__':
    game = Chess4D()
    game.play()