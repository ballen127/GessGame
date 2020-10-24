
class LegalMove():
    """
    Tests proposed moves for correct cardinal direction and for obstacles in path
    Called by propagate_board method in Class GessGame
    """
    def __init__(self, gameboard, fp, fp_total, dir):
        """
        Initializes parameters passed from Class GessGame, used to determine legality of move

        :param gameboard: hypothetical gameboard reflecting proposed move
        :param fp:        elements of 3 x 3-square footprint containing stones
        :param fp_total:  3 x 3-square footprint containing stones and empty squares
        :param dir:       normalized direction of movement
        """

        self._gb = gameboard
        self._fp = fp
        self._fp_total = fp_total
        self._dir = dir

    def validate_cardinal(self, s_row, s_col):
        """
        Validates proposed move is legal given composition of piece

        :param s_row: starting row
        :param s_col: starting column
        :return:      True if legal cardinal direction, False otherwise
        """

        if [s_row + self._dir[0], s_col + self._dir[1]] in self._fp:
            return True
        else:
            return False

    def validate_capture(self):
        """
        Propagates move one-step into the future and evaluates for potential captured stone

        :return: True if stone is encountered on proposed move, False otherwise
        """

        for square in self._fp_total:
            prop_sq = self._gb[ square[0] + self._dir[0] ][ square[1] + self._dir[1] ]
            if [(square[0] + self._dir[0]), (square[1] + self._dir[1])] not in self._fp_total:
                if prop_sq is not None:
                    return True
        return False


class GessGame():
    """
    Implements Gess game
    20 x 20-square board with 19 x 19-square playable area
    Player Black ('x') vs Player White ('o'). Play begins with Black's move
    Player's piece is composed of 3 x 3-square grid centered on the player-selected center stone
    Movement direction and distance is determined by configuration of piece
    Movement that overrides a stone of any color captures that stone and removes it from play
    Win by eliminating your opponent's sole ring. Black's / White's initial rings at klm 2-4 / klm 17-19
    """

    def __init__(self):
        """
        Initializes Player Black to 'x' and Player White to 'o'
        Initializes game board places players' stones in starting positions
        Communicates with class LegalMove to validate cardinal direction and presence of obstacle in path

        Private data members:
            _player_b
            _player_w
            _board
            _direction
            _footprint
            _footprint_none
            _footprint_total
            _game_state
            _resign_game
            _turn
        """

        # Define Player Black and Player White
        self._player_b = 'x'
        self._player_w = 'o'

        self.init_board()

    def init_board(self):
        # Initialize game board
        self._board = [[None] * 20 for _ in range(20)]

        # Define starting positions for Player Black
        self._board[18][2] = self._board[18][4] = self._board[18][6] = self._board[18][7] = self._board[18][8] = \
            self._board[18][9] = self._board[18][10] = self._board[18][11] = self._board[18][12] = \
            self._board[18][13]= self._board[18][15] = self._board[18][17] = \
            self._board[17][1] = self._board[17][2] = self._board[17][3] = self._board[17][5] = self._board[17][7] = \
            self._board[17][8] = self._board[17][9] = self._board[17][10] = self._board[17][12] = \
            self._board[17][14] = self._board[17][16] = self._board[17][17] = self._board[17][18] = \
            self._board[16][2] = self._board[16][4] = self._board[16][6] = self._board[16][7] = self._board[16][8] = \
            self._board[16][9] = self._board[16][10] = self._board[16][11] = self._board[16][12] = \
            self._board[16][13] = self._board[16][15] = self._board[16][17] = \
            self._board[13][2] = self._board[13][5] = self._board[13][8] = self._board[13][11] = \
            self._board[13][14] = self._board[13][17] = self._player_b

        # Define starting positions for Player White
        self._board[1][2] = self._board[1][4] = self._board[1][6] = self._board[1][7] = self._board[1][8] = \
            self._board[1][9] = self._board[1][10] = self._board[1][11] = self._board[1][12] = self._board[1][13]= \
            self._board[1][15] = self._board[1][17] = \
            self._board[2][1] = self._board[2][2] = self._board[2][3] = self._board[2][5] = self._board[2][7] = \
            self._board[2][8] = self._board[2][9] = self._board[2][10] = self._board[2][12] = self._board[2][14] = \
            self._board[2][16] = self._board[2][17] = self._board[2][18] = \
            self._board[3][2] = self._board[3][4] = self._board[3][6] = self._board[3][7] = self._board[3][8] = \
            self._board[3][9] = self._board[3][10] = self._board[3][11] = self._board[3][12] = self._board[3][13] = \
            self._board[3][15] = self._board[3][17] = \
            self._board[6][2] = self._board[6][5] = self._board[6][8] = self._board[6][11] = self._board[6][14] = \
            self._board[6][17] = self._player_w

        # Initialize private data members
        self._direction = []
        self._footprint = []
        self._footprint_none = []
        self._footprint_total = []
        self._game_state = 'UNFINISHED'
        self._resign_game = False
        self._turn = 'x'

    def get_board(self):
        return self._board

    def get_turn(self):
        return self._turn

    def resign_game(self):
        """
        Allows the current player to concede the game, giving the other player the win

        :return: _game_state
        """
        if self._turn == 'x':
            self._game_state = 'WHITE_WON'
        else:
            self._game_state = 'BLACK_WON'

    def get_game_state(self):
        """
        Returns game status: 'UNFINISHED', 'BLACK_WON' or 'WHITE_WON'
        :return: _game.state
        """
        return self._game_state

    def make_footprint(self, var_board, s_row, s_col):
        """
        Evaluates the 3 x 3 footprint of the player's selected piece and creates a list of coordinates
        corresponding to stones and a separate list corresponding to empty spaces

        :param var_board: game board
        :param s_row:     starting row
        :param s_col:     starting column
        :return:          footprint      (coordinate list of stones in footprint)
                          footprint_none (coordinate list of empty squares in footprint)
        """

        board = var_board
        footprint = []
        footprint_none = []
        for r in range(-1, 2, 1):
            for c in range(-1, 2, 1):
                if board[s_row + r][s_col + c] is not None:
                    if board[s_row + r][s_col + c] not in [self._turn]:
                        # Selected piece has mixed stones or it is not the player's turn. Return negative values
                        return [-1],[-1]
                    else:
                        footprint.append([(s_row + r), (s_col + c)])
                else:
                    footprint_none.append([(s_row + r), (s_col + c)])
        return footprint, footprint_none

    def convert_axes(self, starting, ending):
        """
        Converts user's alphanumeric entry to the coordinate system of the game
        a20 corresponds to coordinate [0, 0] and t1 corresponds to [19, 19]

        :param starting: coordinates of central stone in piece
        :param ending:   coordinates of proposed destination for piece
        :return:         s_row: starting row (in game coordinate system
                         s_col: starting column
                         e_row: ending row
                         e_col: ending column
        """

        # Convert alphabetical column values to numbers
        alpha_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4,
                      "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,
                      "k": 10, "l": 11, "m": 12, "n": 13, "o": 14,
                      "p": 15, "q": 16, "r": 17, "s": 18, "t": 19}

        s_col, e_col = alpha_dict[starting[0]], alpha_dict[ending[0]]

        # Correct row entry for game axes system
        s_row, e_row = (20 - int(starting[1:])), (20 - int(ending[1:]))
        return s_row, s_col, e_row, e_col

    def ring_scan(self, hyp_board):
        """
        Scans game board for presence of rings from both players
        Awards victory if the sole ring of an opponent is disrupted
        Prevents moves that disrupt player's sole ring. In this case, the proposed (hypothetical)
            game board is rejected

        :param hyp_board: proposed (hypothetical) game board
        :return:          False if player's move removes that player's sole ring
        """
        x_ring_stat = False
        y_ring_stat = False
        for row in range(2,18):
            for col in range(2,18):
                if hyp_board[row][col] is None:
                    per1 = [hyp_board[row + m][col + n] for m in [-1, 1] for n in range(-1, 2)]
                    per2 = [hyp_board[row][col + n] for n in [-1, 1]]
                    perimeter = per1 + per2

                    x_ring = all(sq == 'x' for sq in perimeter)
                    if x_ring is True:
                        # Black ring identified
                        x_ring_stat = True
                    y_ring = all(sq == 'o' for sq in perimeter)
                    if y_ring is True:
                        # White ring identified
                        y_ring_stat = True

        if x_ring_stat is True:
            # Black ring exists
            if y_ring_stat is False:
                # White ring does not exist
                if self._turn == 'x':
                    # Black's turn
                    self._game_state = 'BLACK_WON'
                    return
                else:
                    # White's turn. Move disrupts White's sole ring
                    return False
        else:
            # Black ring does not exist
            if y_ring_stat is False:
                if self._turn == 'o':
                    return False
                else:


                # White's turn
                    self._game_state = 'WHITE_WON'
                return
            else:
                # Black's turn. Move disrupts Black's sole ring
                return False

    def propagate_board(self, s_row, s_col, e_row, e_col, ring_scan=True):
        """
        Propagates player's piece on a hypothetical game board, from starting to ending row / col
        If proposed move is valid per propagate_board, the move is committed in the actual game board
            in method advance_board

        :param s_row: starting row
        :param s_col: starting column
        :param e_row: ending row
        :param e_col: ending column
        :return:      True if proposed move is valid
        """

        # Create a hypothetical board that is an exact copy of the current game board
        hyp_board = []
        for i in self._board:
            hyp_board.append(list(i))

        capture = False

        while [s_row, s_col] != [e_row, e_col]:
            # Repeat ONE BLOCK AT A TIME until we reach the destination row and column
            footprint, footprint_none = self.make_footprint(hyp_board, s_row, s_col)
            if footprint == [-1]:
                # Negative value signals failed footprint creation (i.e. mixed stone, not player's turn)
                return False
            footprint_total = footprint + footprint_none

            # Check legality of move
            legal_obj = LegalMove(hyp_board, footprint, footprint_total, self.direction)
            cardinal = legal_obj.validate_cardinal(s_row, s_col)

            # Tests for approved cardinal direction
            if cardinal is False:
                # Proposed cardinal direction is not permitted by the stone configuration
                return False
            else:
                # Tests if the next step of the proposed move results in capture
                capture = legal_obj.validate_capture()

                if capture is True:
                    if (s_row + self.direction[0], s_col + self.direction[1]) != (e_row, e_col):
                        # Path to requested destination is blocked by stone. Move not allowed
                        return False

                # No capture on next step. Continue to propagate forward

                # Propagate hypothetical board by one step
                for stone in footprint:
                    hyp_board[stone[0]][stone[1]] = None
                for stone in footprint:
                    hyp_board[stone[0] + self.direction[0]][stone[1] + self.direction[1]] = self._turn

                for blank in footprint_none:
                    hyp_board[blank[0] + self.direction[0]][blank[1] + self.direction[1]] = None

                s_row, s_col = (s_row + self.direction[0]), (s_col + self.direction[1])

                if ring_scan == True:
                    # Check status of players' rings
                    ring_stat = self.ring_scan(hyp_board)
                    if ring_stat is False:
                        # Fails ring scan (i.e. move disrupts player's sole ring)
                        return False
        return True

    def advance_board(self, s_row, s_col, e_row, e_col):
        """
        Advances player's piece on the actual game board from starting to ending (destination) row / column
        Move previously validated in the hypothetical board of the propagate_board method

        :param s_row: starting row
        :param s_col: starting column
        :param e_row: ending (destination) row
        :param e_col: ending (destination) column
        :return:      True at completion of move
        """

        while [s_row, s_col] != [e_row, e_col]:
            # Repeat ONE BLOCK AT A TIME until we reach the destination row and column
            self._footprint, self._footprint_none = self.make_footprint(self._board, s_row, s_col)
            self._footprint_total = self._footprint + self._footprint_none

            # Move piece on game board, one step at a time
            for stone in self._footprint:
                self._board[stone[0]][stone[1]] = None
            for stone in self._footprint:
                self._board[stone[0] + self.direction[0]][stone[1] + self.direction[1]] = self._turn

            for blank in self._footprint_none:
                self._board[blank[0] + self.direction[0]][blank[1] + self.direction[1]] = None

            s_row, s_col = (s_row + self.direction[0]), (s_col + self.direction[1])
        return True

    def make_move(self, starting, ending, axes=0):
        """
        Moves player's 3x3 piece from starting position to ending (destination) position
        Validates move via propagate_board method
        Commits move via advance_board method
        Removes any stones in the margins
        Switches turn to next player

        :param starting: user-entered starting coordinates (alphanumeric)
        :param ending:   user-entered ending coordinates (alphanumeric)
        :return:         True if move completed successfully; False otherwise
        """

        # Test if game has already been won
        if self._game_state in ['BLACK_WON','WHITE_WON']:
            return False

        else:
            # Convert user's input to game axes system
            if axes == 0:
                s_row, s_col, e_row, e_col = self.convert_axes(starting, ending)
            else:
                s_row, s_col, e_row, e_col = starting[0], starting[1], ending[0], ending[1]

            # Test for user's input that is out-of-bounds
            user_entry = [s_row, s_col, e_row, e_col]
            for element in user_entry:
                if element not in range(1, 19):
                    return False

            # Calculate magnitude of requested move in y and x axes
            move_y = abs(s_row - e_row)
            move_x = abs(e_col - s_col)

            # Normalize movement values and resolve into unit direction
            if move_y != 0:
                norm_y = int((e_row - s_row) / abs(e_row - s_row))
            else:
                norm_y = 0
            if move_x != 0:
                norm_x = int((e_col - s_col) / abs(e_col - s_col))
            else:
                norm_x = 0

            self.direction = [norm_y, norm_x]

            # Tests for requested move exceeding 3-block limit (no center stone)
            if self._board[s_row][s_col] is None:
                # No central stone. Move limited to 3 spaces maximum
                if abs(max(move_y, move_x)) > 3:
                    # Requested move > 3 for piece without central stone
                    return False

            # Validate move using hypothetical board
            advance = self.propagate_board(s_row, s_col, e_row, e_col)

            if advance is True:
                # Propagation scan looks good. Advance on the actual game board
                self.advance_board(s_row, s_col, e_row, e_col)
            else:
                # Propagation scan found an issue. Stay put and don't advance game board
                return False

            # Wipe-out stones in the border zone
            for i in (0, 19):
                for j in range(20):
                    self._board[i][j] = None
                    self._board[j][i] = None

            # Switch player turn
            if self._turn == 'x':
                self._turn = 'o'
            else:
                self._turn = 'x'
        return True

    def moves_available(self, row, col):
        moves = []
        for r, pieces_row in enumerate(self._board):
            for c, piece in enumerate(pieces_row):
                move_y = abs(row - r)
                move_x = abs(col - c)
                if self._board[row][col] is None:
                    if abs(max(move_y, move_x)) > 3:
                        continue

                if move_y != 0:
                    norm_y = int((r - row) / abs(r - row))
                else:
                    norm_y = 0
                if move_x != 0:
                    norm_x = int((c - col) / abs(c - col))
                else:
                    norm_x = 0

                self.direction = [norm_y, norm_x]

                try:
                    if self.propagate_board(row, col, r, c, ring_scan=False) and (row, col) != (r, c):
                        moves.append((r, c))
                except:
                    pass
        return moves

# game = GessGame()
# print(game.make_move('b6','c7'))
# print(game.make_move('s15', 'o11'))
# # move_result = game.make_move('m3', 'm6')
# # game.make_move('e14', 'g14')
# # print(move_result)
# print(game.get_game_state())
# game.resign_game()
# print(game.get_game_state())