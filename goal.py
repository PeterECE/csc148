"""CSC148 Assignment 2

CSC148 Winter 2024
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
Jaisie Sin, and Joonho Kim

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, Jaisie Sin, and Joonho Kim

Module Description:

This file contains the hierarchy of Goal classes and related helper functions.
"""
from __future__ import annotations
import random
from block import Block
from settings import colour_name, COLOUR_LIST


def generate_goals(num_goals: int) -> list[Goal]:
    """Return a randomly generated list of goals with length <num_goals>.

    Each goal must be randomly selected from the two types of Goals provided
    and must have a different randomly generated colour from COLOUR_LIST.
    No two goals can have the same colour.

    Preconditions:
    - num_goals <= len(COLOUR_LIST)
    """
    goal_type = PerimeterGoal if random.choice([0, 1]) == 0 else BlobGoal
    unique_indices = random.sample(range(len(COLOUR_LIST)), num_goals)
    goals = [goal_type(COLOUR_LIST[i]) for i in unique_indices]
    return goals


def flatten(block: Block) -> list[list[tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j].

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    lst = []
    if block.level == block.max_depth:
        lst.append([block.colour])
        return lst

    elif 0 == len(block.children):
        diff = block.max_depth - block.level

        for a in range(2 ** diff):
            new_lst = []
            lst.append(new_lst)
            for b in range(2 ** diff):
                lst[a].insert(b, block.colour)
        return lst

    else:
        upper_block_level = block.level + 1
        if block.max_depth == (block.level + 1) == upper_block_level:
            new_lst = [[], []]

            c0, c1, c2, c3 = (block.children[0],
                              block.children[1],
                              block.children[2], block.children[3])
            d0, d1, d2, d3 = c0.colour, c1.colour, c2.colour, c3.colour

            new_lst[0].append(d1)
            new_lst[0].append(d2)
            new_lst[1].append(d0)
            new_lst[1].append(d3)
            return new_lst

        else:
            diff = block.max_depth - block.level
            lst = []
            c0, c1, c2, c3 = (block.children[0],
                              block.children[1],
                              block.children[2], block.children[3])

            for i in range(2 ** diff):
                lst.append([])

            count = flatten(c1)
            for i in range(len(count)):
                lst[i].extend(count[i])

            count = flatten(c2)
            for i in range(len(count)):
                lst[i].extend(count[i])

            count = flatten(c0)
            for i in range(len(count)):
                ith = len(count) + i
                lst[ith].extend(count[i])
            count = flatten(c3)

            for i in range(len(count)):
                ith = len(count) + i
                lst[ith].extend(count[i])

            return lst


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    Instance Attributes:
    - colour: The target colour for this goal, that is the colour to which
              this goal applies.
    """

    colour: tuple[int, int, int]

    def __init__(self, target_colour: tuple[int, int, int]) -> None:
        """Initialize this goal to have the given <target_colour>."""
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given <board>.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal."""
        raise NotImplementedError


class PerimeterGoal(Goal):
    """A goal to maximize the presence of this goal's target colour
    on the board's perimeter.
    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.

        The score for a PerimeterGoal is defined to be the number of unit cells
        on the perimeter whose colour is this goal's target colour. Corner cells
        count twice toward the score.
        """
        flat = flatten(board)
        color = self.colour
        score = 0
        size = len(flat)

        for j in range(size):
            if flat[0][j] == color:
                score += 2 if j in {0, size - 1} else 1
            if flat[size - 1][j] == color:
                score += 2 if j in {0, size - 1} else 1

        for i in range(1, size - 1):
            if flat[i][0] == color:
                score += 1
            if flat[i][size - 1] == color:
                score += 1

        return score

    def description(self) -> str:
        """Return a description of this goal."""
        color = colour_name(self.colour)
        return (
            f'Player must aim to put the most possible units {color} on '
            f'the outer perimeter. Corner cells count twice.'
        )


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.
    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.

        The score for a BlobGoal is defined to be the total number of
        unit cells in the largest connected blob within this Block.
        """
        flat = flatten(board)
        visited = [[-1 for _ in row] for row in flat]
        max_blob_size = 0

        for x in range(len(flat)):
            for y in range(len(flat[0])):
                if visited[x][y] == -1 and flat[x][y] == self.colour:
                    current_blob_size = (
                        self._undiscovered_blob_size((x, y), flat, visited))
                    max_blob_size = max(max_blob_size, current_blob_size)

        return max_blob_size

    def _undiscovered_blob_size(
        self,
        pos: tuple[int, int],
        board: list[list[tuple[int, int, int]]],
        visited: list[list[int]],
    ) -> int:
        """Return the size of the largest connected blob in <board> that (a) is
        of this Goal's target <colour>, (b) includes the cell at <pos>, and (c)
        involves only cells that are not in <visited>.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure (to <board>) that, in each cell,
        contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.

        If <pos> is out of bounds for <board>, return 0.
        """
        x, y = pos

        if (x < 0 or x >= len(board)
                or y < 0 or y >= len(board[0])
                or visited[x][y] != -1):
            return 0    # Out of Bound -> 0

        if board[x][y] != self.colour:
            visited[x][y] = 0
            return 0

        visited[x][y] = 1
        blob_size = 1

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            blob_size += (self._undiscovered_blob_size
                          ((x + dx, y + dy), board, visited))

        return blob_size

    def description(self) -> str:
        """Return a description of this goal."""
        color = colour_name(self.colour)
        return f'The player must aim for the largest “blob” of a {color}'


if __name__ == '__main__':

    import python_ta

    python_ta.check_all(
        config={
            'allowed-import-modules': [
                'doctest',
                'python_ta',
                'random',
                'typing',
                'block',
                'settings',
                'math',
                '__future__',
            ],
            'max-attributes': 15,
        }
    )
