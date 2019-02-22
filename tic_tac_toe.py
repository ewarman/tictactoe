'''Game datatypes'''

from dataclasses import dataclass

EMPTY = ' '
PLAYER_1 = 'x'
PLAYER_2 = 'o'

@dataclass(frozen=True)
class EndState:
  '''
  A possible end state of a game.

  If the game is over, is_over is set to True, and score is a nonzero int, where a positive value
  for score means that Player 1 is awared value, and a negative score means that Player 2 is
  awarded a value.
  If the game is not over, is_over is set to False, and score must be ignored.
  '''
  is_over: bool = False
  score: int = 0  # may be +/-1 if the game is over and one player wins

@dataclass(frozen=True)
class Move:
  '''A description of a TicTacToe move.'''
  player: str = PLAYER_1
  position: int = 0


lines_to_check = [
  (0, 1, 2),
  (3, 4, 5),
  (6, 7, 8),
  (0, 3, 6),
  (1, 4, 7),
  (2, 5, 8),
  (0, 4, 8),
  (2, 4, 6),
]


class TicTacToeState:
  '''The state of a TicTacToe board.'''
  def __init__(self, initial_state=None):
    if not initial_state:
      self.board = [EMPTY for _ in range(9)]
    else:
      self.board = initial_state.copy()

  @staticmethod
  def starting_board():
    return TicTacToeState()

  def apply_move(self, move):
    '''
    Args:
      move: Move instance specifying the move

    Returns:
      A new copy of the board with the move applied.
    '''
    new_state = TicTacToeState(self.board)
    new_state.board[move.position] = move.player
    return new_state

  def is_legal_move(self, move):
    '''Return true if the given move by the given player is legal for this board state.'''
    return move.player == self.players_turn() and self.board[move.position] == EMPTY

  def players_turn(self):
    xs_count = len([pos for pos in self.board if pos == PLAYER_1])
    os_count = len([pos for pos in self.board if pos == PLAYER_2])
    if xs_count == os_count:
      return PLAYER_1
    else:
      return PLAYER_2

  def __getitem__(self, position):
    return self.board[position]

  def tic_tac_toe(self):
    '''Returns winning player if tic tac toe, none if no winner.'''
    for (x, y, z) in lines_to_check:
      if self.board[x] == self.board[y] == self.board[z]:
        return self.board[x]
    return None

  def is_over(self):
    score_map = {PLAYER_1: 1, PLAYER_2: -1}
    board_full = EMPTY not in self.board
    winner = self.tic_tac_toe()
    is_tic_tac_toe = bool(winner)

    if is_tic_tac_toe:
      return EndState(is_over=True, score=score_map[winner])
    elif board_full:
      return EndState(is_over=True, score=0)
    else:
      return EndState(is_over=False)

  def all_legal_moves(self):
    moves = []
    for player in [PLAYER_1, PLAYER_2]:
      for space in self.board:
        move = Move(player=player, position=space)
        if self.is_legal_move(move):
          moves.append(move)
    return moves

  def __str__(self):
    return '''{}{}{}
    {}{}{}
    {}{}{}'''.format(*self.board)

  @classmethod
  def parse(self, str):
    pass


def tic_tac_toe_reward(state, end_state):
    """
    Need a way to say: given a State S and an EndState E, such that E was reached while exploring S,
    what is the reward that should be given to S.
    """
    if state.players_turn() == PLAYER_1:
       return end_state.score
    elif state.players_turn() == PLAYER_2:
       return -end_state.score


def starting_board():
  return TicTacToeState.starting_board()
