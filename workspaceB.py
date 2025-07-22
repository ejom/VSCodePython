from copy import deepcopy

# Directions for sliding pieces
ORTHOGONAL_DIRS = [(-1,0),(1,0),(0,-1),(0,1)]
DIAGONAL_DIRS   = [(-1,-1),(-1,1),(1,-1),(1,1)]
KNIGHT_DIRS     = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
KING_DIRS       = ORTHOGONAL_DIRS + DIAGONAL_DIRS

def normalize(board_input):
    """
    Normalize input to an 8x8 list-of-lists of single-character codes or '' for empty.
    Accepts either:
      - A list of 8 lists, each length 8, with '' or single-character strings.
      - A list of 8 strings; empty string => rank of all empty, otherwise each string is split into chars.
    Raises ValueError if shape is wrong.
    """
    if not isinstance(board_input, list) or len(board_input) != 8:
        raise ValueError("Board must be list of length 8")
    board = []
    for row in board_input:
        if isinstance(row, list):
            if len(row) != 8:
                raise ValueError("Each row-list must have length 8")
            board.append([c if c not in ('n','N') else '' for c in row])
        elif isinstance(row, str):
            if len(row) == 0:
                board.append(['']*8)
            elif len(row) == 8:
                board.append([c if c not in ('n','N') else '' for c in row])
            else:
                raise ValueError("Each row-string must be length 8 or empty")
        else:
            raise ValueError("Each row must be list or string")
    return board

def find_king(board, color):
    target = 'k' if color=='black' else 'K'
    for r in range(8):
        for c in range(8):
            if board[r][c] == target:
                return (r,c)
    return None

def on_board(r,c):
    return 0 <= r < 8 and 0 <= c < 8

def is_attacked(board, r, c, by_color):
    """
    Is square (r,c) attacked by any piece of by_color?
    """
    enemy_pawns = ('p' if by_color=='white' else 'P')
    enemy_knight = ('h' if by_color=='white' else 'H')
    enemy_rook   = ('r' if by_color=='white' else 'R')
    enemy_bishop = ('b' if by_color=='white' else 'B')
    enemy_queen  = ('q' if by_color=='white' else 'Q')
    enemy_king   = ('k' if by_color=='white' else 'K')

    # Pawn attacks
    dr = -1 if by_color=='white' else 1
    for dc in (-1,1):
        rr,cc = r+dr, c+dc
        if on_board(rr,cc) and board[rr][cc]==enemy_pawns:
            return True

    # Knight attacks
    for dr,dc in KNIGHT_DIRS:
        rr,cc = r+dr, c+dc
        if on_board(rr,cc) and board[rr][cc]==enemy_knight:
            return True

    # Sliding attacks: rook/queen
    for dr,dc in ORTHOGONAL_DIRS:
        rr,cc = r+dr, c+dc
        while on_board(rr,cc):
            piece = board[rr][cc]
            if piece:
                if piece in (enemy_rook, enemy_queen):
                    return True
                break
            rr += dr; cc += dc

    # Sliding attacks: bishop/queen
    for dr,dc in DIAGONAL_DIRS:
        rr,cc = r+dr, c+dc
        while on_board(rr,cc):
            piece = board[rr][cc]
            if piece:
                if piece in (enemy_bishop, enemy_queen):
                    return True
                break
            rr += dr; cc += dc

    # King adjacency attack
    for dr,dc in KING_DIRS:
        rr,cc = r+dr, c+dc
        if on_board(rr,cc) and board[rr][cc]==enemy_king:
            return True

    return False

def generate_moves(board, r, c):
    """
    Generate all pseudo-legal moves for the piece at (r,c).
    Yields (r2,c2) target coords.
    """
    piece = board[r][c]
    if not piece:
        return
    is_white = piece.islower()
    color = 'white' if is_white else 'black'
    enemy = 'black' if is_white else 'white'
    p = piece.lower()

    def try_slide(dirs):
        for dr,dc in dirs:
            rr,cc = r+dr, c+dc
            while on_board(rr,cc):
                if not board[rr][cc]:
                    yield (rr,cc)
                else:
                    if board[rr][cc].isupper() != is_white:
                        yield (rr,cc)
                    break
                rr += dr; cc += dc

    if p=='r':
        yield from try_slide(ORTHOGONAL_DIRS)
    elif p=='b':
        yield from try_slide(DIAGONAL_DIRS)
    elif p=='q':
        yield from try_slide(ORTHOGONAL_DIRS+DIAGONAL_DIRS)
    elif p=='h':  # knight
        for dr,dc in KNIGHT_DIRS:
            rr,cc = r+dr, c+dc
            if on_board(rr,cc) and (not board[rr][cc] or board[rr][cc].isupper()!=is_white):
                yield (rr,cc)
    elif p=='k':
        for dr,dc in KING_DIRS:
            rr,cc = r+dr, c+dc
            if on_board(rr,cc) and (not board[rr][cc] or board[rr][cc].isupper()!=is_white):
                yield (rr,cc)
    elif p=='p':
        # pawn moves
        dir_forward = 1 if is_white else -1
        # one step
        rr,cc = r+dir_forward, c
        if on_board(rr,cc) and not board[rr][cc]:
            yield (rr,cc)
        # captures
        for dc in (-1,1):
            rr,cc = r+dir_forward, c+dc
            if on_board(rr,cc) and board[rr][cc] and board[rr][cc].isupper()!=is_white:
                yield (rr,cc)

def in_check(board, color):
    kp = find_king(board, color)
    if not kp:
        # should not happen under normal validate check
        return False
    return is_attacked(board, kp[0], kp[1], 'black' if color=='white' else 'white')

def has_any_legal(board, color):
    """
    Return True if color has at least one move that gets out of check.
    """
    is_white = (color=='white')
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p and (p.islower()==is_white):
                for (r2,c2) in generate_moves(board,r,c):
                    newb = deepcopy(board)
                    newb[r2][c2] = newb[r][c]
                    newb[r][c] = ''
                    # if moving the king, update its pos for check test
                    if newb[r2][c2].lower()=='k':
                        # ensure king not walking into check
                        if is_attacked(newb, r2, c2, 'black' if color=='white' else 'white'):
                            continue
                    if not in_check(newb, color):
                        return True
    return False

def checkmate_status(board_input):
    """
    Returns (is_checkmate:bool, code:str).
      code: 'W' if white is in checkmate, 'B' if black is in checkmate,
            '' if none, 'E' if invalid.
    """
    try:
        board = normalize(board_input)
    except ValueError:
        return False, 'E'

    # Validate kings
    wking = find_king(board, 'white')
    bking = find_king(board, 'black')
    if not wking or not bking:
        return False, 'E'

    w_in_check  = in_check(board, 'white')
    b_in_check  = in_check(board, 'black')
    w_can_move  = has_any_legal(board, 'white')
    b_can_move  = has_any_legal(board, 'black')

    w_mate = w_in_check and not w_can_move
    b_mate = b_in_check and not b_can_move

    # Both in mate or contradictory?
    if (w_mate and b_mate):
        return False, 'E'
    if w_mate:
        return True, 'W'
    if b_mate:
        return True, 'B'
    return False, ''

if __name__ == "__main__":
    # Your six test inputs:
    tests = [
        # 1. empty 2D list
        [['']*8 for _ in range(8)],

        # 2. mixed 2D list
        [
         ['', '', '', '', '', '', 'r', 'k'],
         ['', 'b', '', '', '', '', '', ''],
         ['']*8, ['']*8, ['']*8, ['']*8,
         ['', '', '', '', '', 'P', '', 'P'],
         ['', '', '', '', '', 'R', 'K', '']
        ],

        # 3. list of strings with empty ranks
        ["nhnnbrqk", "nnnpnnnp", "", "pnpnnnnn", "", "PPPPPPPP", "", "KRQNNBHR"],

        # 4. another 2D list
        [
         ['r','h','b','','k','','h','r'],
         ['p','p','p','p','','p','p','p'],
         ['']*8,
         ['', '', 'b', '', 'p', '', '', ''],
         ['', '', '', '', 'P', '', '', 'q'],
         ['', '', 'H', '', '', '', '', ''],
         ['P','P','P','P','','P','P','P'],
         ['R','','B','Q','K','B','H','R']
        ],

        # 5. yet another 2D list
        [
         ['','', 'k','r','','','',''],
         ['p','p','p','','','p','p','p'],
         ['']*8,
         ['', '', '', '', 'p', '', '', ''],
         ['', '', '', '', 'P', '', 'b',''],
         ['', '', '', '', 'Q', '', '', ''],
         ['P','','','','','P','P','P'],
         ['','H','','','K','B','','R']
        ],

        # 6. invalid: two black kings
        ["", "", "", "", "", "NNNNNBKH", "", "nnnnnnnk"],

        # 7. final 2D list
        [
         ['','','','','','','','Q'],
         ['','p','p','k','','p','p',''],
         ['','', 'h','','','','','p'],
         ['','p','','p','','b','',''],
         ['']*8,
         ['b','','P','','P','','',''],
         ['P','','H','','','P','P','P'],
         ['','', 'K','R','','','H','R']
        ],
    ]

    results = [checkmate_status(t) for t in tests]
    print(results)
