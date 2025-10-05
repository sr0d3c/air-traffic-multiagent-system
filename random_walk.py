"""
Generalized behavior for random walking, one grid cell at a time.
"""

import mesa
import agents


class RandomWalker(mesa.Agent):
    """
    Class implementing random walker methods in a generalized manner.

    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.

    """

    grid = None
    x = None
    y = None
    moore = False

    def __init__(self, unique_id, pos, model, moore=False):
        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        """
        super().__init__(unique_id, model)
        
        self.pos = pos
        self.moore = moore


    def random_move(self):
        """
        Step one cell in any allowable direction.
        """

        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, include_center=False)

        for i in range(len(next_moves)):

            next_move = self.random.choice(next_moves)
            next_cell = self.model.grid.get_cell_list_contents([next_move])
            planes = [obj for obj in next_cell if isinstance(obj, agents.Plane)]
            airports = [obj for obj in next_cell if isinstance(obj, agents.Airport)]

            if len(airports) == 0 and len(planes) > 0:

                continue

            else:

                # Now move:
                self.model.grid.move_agent(self, next_move)
                break
