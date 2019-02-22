from dataclasses import dataclass

@dataclass(frozen=True)
class ExplorationData:
    ''' Data stored in a node while we explore it in the Monte Carlo Tree Search.

    This data is used to determine which move to explore next.
    '''
    cumulative_score: float = 0.0
    visits: int = 0

    def update_with_score(self, score):
       return ExplorationData(
           cumulative_score=self.cumulative_score + score,
           visits=self.visits + 1,
       )


class Node:
    def __init__(self, state, parent=None):
        """
        state: An object which has the following methods:

         - apply_move: accept a Move and produce a new state as output
         - is_over: return an EndState if this game is over (used to determine if the state is a leaf)
         - all_legal_moves: return all legal Moves from this state

        parent: A Node that points to a previous game state.
        """
        self.state = state
        self.children = []
        self.parent = parent
        self.exploration_data = ExplorationData()

    def expand(self):
        """Expand all possible child nodes achievable by legal moves.

        If this node is a leaf, this method is a no-op.
        """
        if self.children:
           return self.children

        child_states = self.state.all_legal_moves()
        self.children = [Node(state=child_state, parent=self) for child_state in child_states]
        return self.children

    @property
    def is_leaf(self):
        """If the node's state is end of game (no more moves to apply), return True."""
        end_state = self.state.is_over()
        return end_state.is_over


class MonteCarloTreeSearch:
    '''
    A class that performs Monte Carlo Tree Search on a given game state.
    '''
    def __init__(self, initial_board_state, move_picker, reward_fn):
        '''
        Args:
            initial_board_state: a State to start the search from
            move_picker: an object which implements
               - pick_move: [State] -> State accepts a list of candidate moves and returns one of them
                            as the choice for what to do next
            reward_fn: a callable (State, EndState) -> float that determines the score at the end
              of a game, awarded to the winner in the end state.
        '''
        self.tree_root = Node(state=initial_board_state, parent=None)
        self.move_picker = move_picker
        self.reward_fn = reward_fn

    def do_exploration(self):
        '''
        Explore the tree by performing a single self-play of the game, starting from the root.

        1. Iteratively choose a move to play, expanding the node as necessary until reaching a leaf
        2. Record the score at that leaf
        3. Backtrack up the tree, updating the ExplorationData at each node until reaching the root
        '''
        node = self.tree_root
        while not node.is_leaf:
           node = move_picker.pick_move(node.expand())

        end_state = node.state.is_over()

        while not node.parent:
            node = node.parent
            score = self.reward_fn(node.state, end_state)
            node.exploration_data = node.exploration_data.update_with_score(score)

    def explore(self, game_count=10000):
        """Run game_count many iterations of self-play, and then update move_picker to learn from the
        explored tree."""
        pass
