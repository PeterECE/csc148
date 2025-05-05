"""CSC148 Assignment 0

=== CSC148 Winter 2024 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jonathan Calver and Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) Jonathan Calver, Diane Horton, and Sophia Huynh.

=== Module Description ===

This file contains some provided tests for the assignment and is where
you will write additional tests.

To run the tests in this file, right-click here and select the option
that says "Run 'Python tests in test...'"

Note: We will not run pyTA on this file when grading your assignment.

"""
from __future__ import annotations

from four_in_a_row import *
from a0 import *


class TestHelpers:
    """
    These are provided tests related to Task 1, which are meant to remind you
    of the structure of a pytest for later tasks. For Task 1, you are asked
    to write doctests instead.

    While not required, you are welcome to add other pytests here as you
    develop your code.
    """

    def test_within_grid_in_grid(self):
        """Test that (0, 0) is inside a 4-by-4 grid."""
        assert within_grid((0, 0), 4)

    def test_within_grid_outside_grid(self):
        """Test that (4, 4) is outside a 4-by-4 grid."""
        assert not within_grid((4, 4), 4)

    def test_all_within_grid_all_in_grid(self):
        """Test when the four coordinates are all within a 4-by-4 grid."""
        assert all_within_grid([(0, 0), (1, 1), (2, 2), (3, 3)], 4)

    def test_reflect_vertically_above(self):
        """Test reflecting vertically for a coordinate above the middle."""
        assert reflect_vertically((0, 1), 5) == (4, 1)

    def test_reflect_vertically_middle(self):
        """Test reflecting vertically for a coordinate on the middle row."""
        assert reflect_vertically((2, 1), 5) == (2, 1)

    def test_reflect_points(self):
        """Test reflecting a very short line"""
        assert reflect_points([(0, 1), (1, 2)], 5) == [(4, 1), (3, 2)]


class TestLine:
    def test_is_row_1(self):
        """Test to see if is in a row"""
        squares = [Square((0, 1)), Square((0, 2)), Square((0, 3)), Square((0, 4))]
        assert is_row(squares) == True

    def test_is_row_2(self):
        """Test to see if is in a row"""
        squares = [Square((0, 1)), Square((0, 2)), Square((0, 4)), Square((0, 3))]
        assert is_row(squares) == False

    def test_is_column_1(self):
        """Test to see if is in a row"""
        squares = [Square((0, 1)), Square((1, 1)), Square((2, 1)), Square((3, 1))]
        assert is_column(squares) == True

    def test_is_column_2(self):
        """Test to see if is in a row"""
        squares = [Square((0, 1)), Square((1, 1)), Square((3, 1)), Square((2, 1))]
        assert is_column(squares) == False

    def test_is_diagonal_true_down(self):
        """Test turn down"""
        squares = [Square((0, 0)), Square((1, 1)), Square((2, 2)), Square((3, 3))]
        assert is_diagonal(squares) == True

    def test_is_diagonal_true_up(self):
        """Test turn up"""
        squares = [Square((3, 0)), Square((2, 1)), Square((1, 2)), Square((0, 3))]
        assert is_diagonal(squares) == True

    def test_is_diagonal_random(self):
        squares = [Square((0, 0)), Square((1, 1)), Square((3, 3)), Square((2, 2))]
        assert is_diagonal(squares) == False

    def test_line_drop_1(self):
        lines = Line([Square((0, 0)), Square((1, 0)), Square((2, 0)), Square((3, 0))])
        assert lines.drop('X') == 3

    def test_line_drop_2(self):
        lines = Line([Square((0, 0)), Square((1, 0)), Square((2, 0)), Square((3, 0))])
        lines.drop('X')
        assert lines.drop('X') == 2

    def test_line_is_full_1(self):
        empty_line = Line([Square((0, 1)), Square((1, 1)), Square((2, 1)), Square((3, 1))])
        assert empty_line.is_full() == False

    def test_line_is_full_2(self):
        full_line = Line([Square((0, 1), 'X'), Square((1, 1), 'X'), Square((2, 1), 'X'), Square((3, 1), 'X')])
        assert full_line.is_full() == True

    def test_line_has_fair_1(self):
        line = Line([Square((0, 1)), Square((0, 2)), Square((0, 3)), Square((0, 4))])
        assert line.has_fiar((0, 2)) == False

    def test_line_has_fair_2(self):
        line = Line([Square((0, 1), 'X'), Square((0, 2), 'X'), Square((0, 3), 'X'), Square((0, 4), 'X')])
        assert line.has_fiar((0, 2)) == True

    def test_line_has_fair_3(self):
        line = Line([Square((0, 1), 'X'), Square((0, 2), 'X'), Square((0, 3), 'X'), Square((0, 4), 'X'), Square((0, 5), 'X')])
        len(line)
        assert line.has_fiar((0, 1))


class TestGrid:
    """
    TODO Task 3.1: add tests for the Grid methods and related functions
                 You must write two tests for each of:
                   - Grid.drop, Grid.is_full
                   - create_rows_and_columns


    TODO Task 3.2: add tests for the Grid methods and related functions
                 You must write two tests for each of:
                   - Grid.has_fiar
                   - create_mapping
    """
    def test_grid_drop_1(self):
        g = Grid(4)
        assert g.drop(1, 'X') == 3
        assert g.drop(1, 'X') == 2

    def test_grid_drop_2(self):
        g = Grid(4)
        assert g.drop(1, 'X') == 3
        assert g.drop(1, 'X') == 2
        assert g.drop(1, 'X') == 1
        assert g.drop(1, 'X') == 0
        assert g.drop(1, 'X') is None

    def test_grid_is_full_1(self):
        g = Grid(4)
        assert g.is_full() == False

    def test_grid_is_full_2(self):
        g = Grid(5)
        for i in range(5):
            for _ in range(5):
                g.drop(i, "X")
        assert g.is_full()

    def test_create_rows_and_columns_1(self):
        squares = create_squares(4)
        rows, columns = create_rows_and_columns(squares)
        assert rows[0][0] is columns[0][0]

    def test_create_rows_and_columns_2(self):
        squares = create_squares(5)
        rows, columns = create_rows_and_columns(squares)
        assert rows[0][0] is columns[0][0]

    def test_grid_has_fiar_1(self):
        g = Grid(4)
        assert not g.has_fiar((0, 0))
    def test_grid_has_fiar_2(self):
        g = Grid(4)
        g.drop(0, "X")
        g.drop(0, "X")
        g.drop(0, "X")
        g.drop(0, "X")
        assert g.has_fiar((0, 0))

    def test_creat_mapping_1(self):
        squares = create_squares(6)
        mapping = create_mapping(squares)
        lines = mapping[(2,0)]
        assert len(lines) == 3

    def test_creat_mapping_2(self):
        squares = create_squares(6)
        mapping = create_mapping(squares)
        lines = mapping[(3, 3)]
        assert len(lines) == 4



class TestFourInARow:
    """
    TODO TASK 4:
     - run check_coverage.py to get the code coverage report.
     - Using the code coverage report, identify which branches of the code
       are not currently being tested.
     - add tests below in order to achieve 100% code coverage when you run
       check_coverage.py. Your tests should follow a similar structure
       to the test_x_wins test defined below.
    """

    def test_x_wins(self) -> None:
        """
        Provided test demonstrating how you can test FourInARow.play using
        a StringIO object to "script" the input.

        See both the handout and the Task 4 section of the supplemental slides
        for a detailed explanation of this example.
        """
        fiar = play_game(GAME_SCRIPT_X_WINS)

        assert fiar.result == WIN

    def test_x_losses(self) -> None:
        """
        Provided test demonstrating how you can test FourInARow.play using
        a StringIO object to "script" the input.

        See both the handout and the Task 4 section of the supplemental slides
        for a detailed explanation of this example.
        """
        GAME_SCRIPT_X_LOSSES ='5 True True\n' \
                              '2\n' \
                              '0\n' \
                              '1\n' \
                              '0\n' \
                              '1\n' \
                              '0\n' \
                              '1\n' \
                              '0\n'
        fiar = play_game(GAME_SCRIPT_X_LOSSES)

        assert fiar.result == LOSS

    def test_x_draws(self) -> None:
        GAME_SCRIPT_X_DRAWS ='4 True True\n' \
                                   '1\n' \
                                   '0\n' \
                                   '1\n' \
                                   '0\n' \
                                   '1\n' \
                                   '0\n' \
                                   '2\n' \
                                   '3\n' \
                                   '2\n' \
                                   '3\n' \
                                   '2\n' \
                                   '3\n'\
                                   '0\n' \
                                   '1\n' \
                                   '3\n' \
                                   '2\n'
        fiar = play_game(GAME_SCRIPT_X_DRAWS)
        assert fiar.result == DRAW

if __name__ == '__main__':
    import pytest

    pytest.main(['test_a0.py'])
