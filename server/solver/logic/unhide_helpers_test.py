from solver.logic.unhide_helpers import unhideSurroundingSquaresWithZero, unhideSurroundingSquaresWithZeroHelper, isFlaggedComplete, unhideAllSurroundingSquares

import numpy as np


def test_unhideSurroundingSquaresWithZero():
  board = [
    [0, 0, 0],
    [0, 1, 1],
    [2, 3, 9],
    [9, 9, 2]
  ]
  row_index = 0
  cols_index = 0
  num_rows = 4
  num_cols = 3
  setIndices = unhideSurroundingSquaresWithZero(board, row_index, cols_index, num_rows, num_cols)
  expected = {(0,0), (0,1), (0,2), (1,1), (1,2), (1,0), (2,0), (2,1)}
  assert setIndices == expected


def test_isFlaggedComplete():
  hidden = [
    ["F", "H", "S"],
    ["H", "F", "H"],
    ["F", "S", "H"],
    ["S", "F", "H"]
  ]
  num_adjacent_mines = 3
  row_index = 2
  cols_index = 1
  num_rows = 4
  num_cols = 3
  assert isFlaggedComplete(num_adjacent_mines, hidden, row_index, cols_index, num_rows, num_cols) == True

def test_unhideAllSurroundingSquares_barebones():
  hidden = [
    ["F", "H", "S"],
    ["H", "F", "H"],
    ["F", "S", "H"],
    ["S", "F", "H"]
  ]
  board = [
    [1, 1, 1],
    [2, 9, 1],
    [9, 3, 2],
    [2, 9, 1]
  ]
  row_index = 2
  cols_index = 1
  num_rows = 4
  num_cols = 3
  setIndices = unhideAllSurroundingSquares(hidden, board, row_index, cols_index, num_rows, num_cols)
  expected = {(1,0), (1,2), (2,2), (3,2)}
  assert setIndices == expected


def test_unhideAllSurroundingSquares_full():
  hidden = [
    ["H", "H", "H"],
    ["H", "H", "H"],
    ["F", "S", "S"],
    ["S", "F", "S"]
  ]
  board = [
    [0, 0, 0],
    [1, 1, 0],
    [9, 2, 1],
    [2, 9, 1]
  ]
  row_index = 2
  cols_index = 2 
  num_rows = 4
  num_cols = 3 
  setIndices = unhideAllSurroundingSquares(hidden, board, row_index, cols_index, num_rows, num_cols)
  expected = {(1,1), (1,2), (0,1), (0,0), (1,0), (0,2), (2,1), (2,2)}
  assert setIndices == expected