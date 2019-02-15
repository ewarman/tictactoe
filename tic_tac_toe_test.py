from assertpy import assert_that
import tic_tac_toe


def test_starting_board():
    state = tic_tac_toe.starting_board()
    assert_that(state.board).is_empty()
