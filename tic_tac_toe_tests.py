from pyassert import *
import tic_tac_toe
import unittest

class TicTacToeStateTests(unittest.TestCase):
  def test_starting_board(self):
    state = tic_tac_toe.starting_board()
    assert_that(state.board).is_emtpy()

if __name__=="__main__":
  unittest.main()
