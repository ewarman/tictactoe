from assertpy import assert_that
from tic_tac_toe import Move
from tic_tac_toe import starting_board
from tic_tac_toe import PLAYER_1
from tic_tac_toe import PLAYER_2
from tic_tac_toe import EMPTY


def test_starting_board():
  state = starting_board()
  for i in range(9):
    assert_that(state.board[i]).is_equal_to(EMPTY)


def test_apply_move():
  state = starting_board()
  move = Move(player=PLAYER_1, position=0)
  new_state = state.apply_move(move)
  assert_that(new_state.players_turn()).is_equal_to(PLAYER_2)

  # this is also leaking internal representation a little bit
  assert_that(new_state.board[0]).is_equal_to(PLAYER_1)
  for i in range(1, 9):
    assert_that(new_state.board[i]).is_equal_to(EMPTY)


def test_is_legal_move():
  initial_state = starting_board()
  move = Move(player=PLAYER_1, position=0)
  new_state = initial_state.apply_move(move)
  # Applying the same move is illegal
  assert_that(new_state.is_legal_move(move)).is_false()
  # Applying the same move with a different player is illegal
  move = Move(player=PLAYER_2, position=0)
  assert_that(new_state.is_legal_move(move)).is_false()
  # Applying a move in an empty space is legal
  move = Move(player=PLAYER_2, position=1)
  assert_that(new_state.is_legal_move(move)).is_true()


def test_all_legal_moves():
  state = starting_board()
  expected_moves = set(
    Move(player=PLAYER_1, position=i) for i in range(9)
  )
  assert_that(set(state.all_legal_moves())).is_equal_to(expected_moves)


def test_is_over_player_1_wins():
  '''
  Play until board looks like

  xox
  oxo
  x
  '''
  current_state = starting_board()

  for i in range(7):
    move = Move(
      player=(PLAYER_1 if i%2 == 0 else PLAYER_2),
      position=i
    )
    current_state = current_state.apply_move(move)

  pass
