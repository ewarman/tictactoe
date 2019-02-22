from assertpy import assert_that
import ipdb
import tic_tac_toe
import mcts


class DumbMovePicker:
    def __init__(self):
        pass

    def pick_move(self, states):
        return states[0]

def test_stupid_tic_tac_toe():
    initial_state = tic_tac_toe.TicTacToeState()
    move_picker = DumbMovePicker()
    search = mcts.MonteCarloTreeSearch(
        initial_state,
        move_picker,
        tic_tac_toe.tic_tac_toe_reward
    )

    search.do_exploration()
