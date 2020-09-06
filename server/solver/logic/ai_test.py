from solver.logic.ai import firstMove, findRandomZeroCell, uncover, findDefiniteMines, isHiddenComplete, flagDefiniteMines, clickAdjacentCellsToUncover
from solver.logic.ai import generateBoard, generateMoves 

import numpy as np

def test_generateMoves():
  num_rows=30
  num_cols=16
  num_mines=99
  board, hidden = generateBoard(num_rows, num_cols, num_mines)
  #assert generateMoves(board, hidden, num_rows, num_cols, num_mines) == 0

######################################## SOLVER LOGIC #########################################################

def test_firstMove():
  hidden = [
    ["H", "H", "H"],
    ["H", "H", "H"]
  ]
  hidden2 = [
    ["S", "H", "H"],
    ["H", "H", "H"]
  ]
  num_rows = 2
  num_cols = 3
  assert firstMove(hidden, num_rows, num_cols) == True
  assert firstMove(hidden2, num_rows, num_cols) == False

def test_findRandomZeroCell():
  board = [
    [1, 2, 1],
    [1, 4, 0]
  ]
  board2 = [
    [0, 2, 1],
    [1, 4, 2]
  ]
  num_rows=2
  num_cols=3
  assert findRandomZeroCell(board, num_rows, num_cols) == [1,2]
  assert findRandomZeroCell(board2, num_rows, num_cols) == [0,0]


def test_uncover():
  board = [
    [0, 0, 0],
    [0, 1, 1],
    [2, 3, 9],
    [9, 9, 2]
  ]
  hidden = [
    ["H", "H", "H"],
    ["H", "H", "H"],
    ["H", "H", "H"],
    ["H", "H", "H"]
  ]
  cell=(0,0)
  num_rows=4
  num_cols=3
  updatedHidden = [
    [0, 0, 0],
    [0, 1, 1],
    [2, 3, "H"],
    ["H", "H", "H"]
  ]
  assert uncover(cell, hidden, board, num_rows, num_cols) == updatedHidden


def test_findDefiniteMines():
  hidden = [
    [0, 0, 0],
    [0, 1, 1],
    [2, 3, "H"],
    ["H", "H", "H"]
  ]
  num_rows=4
  num_cols=3
  definiteMines = {(2,2), (3,0), (3,1)}
  assert set(map(tuple, findDefiniteMines(hidden, num_rows, num_cols))) == definiteMines

def test_isHiddenComplete():
  hidden = [
    ["S", "H", "S"],
    ["S", "S", "H"],
    ["S", "S", "H"],
    ["S", "S", "H"]
  ]
  num_adjacent_mines = 3
  row_index = 2
  cols_index = 1
  num_rows = 4
  num_cols = 3
  complete, hiddenSet = isHiddenComplete(num_adjacent_mines, hidden, row_index, cols_index, num_rows, num_cols)
  assert complete == True
  assert hiddenSet == {(1,2), (2,2), (3,2)}


def test_flagDefiniteMines():
  board = [
    [0, 0, 0],
    [0, 1, 1],
    [2, 3, 9],
    [9, 9, 2]
  ]
  hidden = [
    ["H", "H", "H"],
    ["H", "H", "H"],
    ["H", "H", "H"],
    ["H", "H", "H"]
  ]
  mines={(0,0), (2,1)}
  updatedHidden = [
    ["F", "H", "H"],
    ["H", "H", "H"],
    ["H", "F", "H"],
    ["H", "H", "H"]
  ]
  assert flagDefiniteMines(hidden, mines) == updatedHidden


def test_clickAdjacentCellsToUncover():
  cell = (2,1)
  board = [
    [0, 0, 0],
    [1, 1, 1],
    [2, 9, 1],
    [9, 2, 1]
  ]
  hidden = [
    ["H", "H", "H"],
    ["H",   1,   1],
    [2,   "F", "H"],
    ["H", "H", "H"]
  ]
  num_rows=4
  num_cols=3

  expected_updated_hidden = [
    [0,     0,   0],
    [1,     1,   1],
    [2,   "F",   1],
    ["H",   2,   1]
  ]

  expected_clicked = {(1,1), (1,2), (2,2), (3,2), (1,0)}
  cells_clicked, updated_hidden = clickAdjacentCellsToUncover(cell, hidden, board, num_rows, num_cols)
  assert cells_clicked == expected_clicked
  assert expected_updated_hidden == updated_hidden

def test_generateMoves():
  board = [[0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 9.0, 9.0, 9.0, 1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 3.0, 9.0, 4.0, 3.0, 9.0, 2.0, 2.0, 2.0, 3.0, 2.0, 1.0, 1.0, 9.0, 1.0], [1.0, 2.0, 9.0, 9.0, 9.0, 9.0, 5.0, 9.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0], [9.0, 2.0, 2.0, 5.0, 9.0, 9.0, 4.0, 9.0, 4.0, 2.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0], [1.0, 1.0, 0.0, 2.0, 9.0, 4.0, 3.0, 4.0, 9.0, 9.0, 3.0, 3.0, 3.0, 9.0, 1.0, 0.0], [0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 9.0, 3.0, 9.0, 4.0, 9.0, 9.0, 9.0, 2.0, 1.0, 0.0], [2.0, 3.0, 3.0, 9.0, 1.0, 2.0, 2.0, 4.0, 2.0, 3.0, 3.0, 9.0, 4.0, 3.0, 2.0, 1.0], [9.0, 9.0, 9.0, 2.0, 1.0, 1.0, 9.0, 2.0, 9.0, 2.0, 2.0, 2.0, 2.0, 9.0, 9.0, 2.0], [4.0, 9.0, 4.0, 1.0, 0.0, 2.0, 2.0, 3.0, 1.0, 3.0, 9.0, 2.0, 1.0, 2.0, 3.0, 9.0], [2.0, 9.0, 3.0, 1.0, 1.0, 1.0, 9.0, 1.0, 0.0, 2.0, 9.0, 2.0, 0.0, 0.0, 1.0, 1.0], [3.0, 3.0, 4.0, 9.0, 2.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0], [9.0, 9.0, 4.0, 9.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0], [3.0, 4.0, 9.0, 2.0, 2.0, 1.0, 1.0, 0.0, 0.0, 1.0, 3.0, 9.0, 3.0, 1.0, 0.0, 0.0], [1.0, 9.0, 2.0, 1.0, 1.0, 9.0, 1.0, 0.0, 0.0, 1.0, 9.0, 9.0, 9.0, 1.0, 0.0, 0.0], [1.0, 1.0, 2.0, 1.0, 3.0, 2.0, 3.0, 1.0, 1.0, 1.0, 2.0, 3.0, 2.0, 1.0, 0.0, 0.0], [0.0, 1.0, 2.0, 9.0, 2.0, 9.0, 4.0, 9.0, 3.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0], [1.0, 2.0, 9.0, 3.0, 3.0, 4.0, 9.0, 9.0, 9.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 9.0], [2.0, 9.0, 4.0, 3.0, 9.0, 3.0, 9.0, 5.0, 4.0, 3.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0], [2.0, 9.0, 9.0, 2.0, 1.0, 2.0, 3.0, 9.0, 3.0, 9.0, 9.0, 2.0, 1.0, 9.0, 1.0, 0.0], [1.0, 2.0, 2.0, 2.0, 1.0, 1.0, 2.0, 9.0, 3.0, 3.0, 9.0, 2.0, 1.0, 1.0, 1.0, 0.0], [0.0, 0.0, 0.0, 2.0, 9.0, 3.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 2.0, 9.0, 4.0, 9.0, 2.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 1.0, 1.0], [0.0, 0.0, 0.0, 1.0, 1.0, 3.0, 9.0, 2.0, 0.0, 0.0, 0.0, 1.0, 9.0, 2.0, 9.0, 1.0], [2.0, 2.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 3.0, 2.0, 2.0], [9.0, 9.0, 1.0, 1.0, 2.0, 3.0, 2.0, 1.0, 2.0, 9.0, 2.0, 1.0, 1.0, 2.0, 9.0, 1.0], [2.0, 3.0, 2.0, 2.0, 9.0, 9.0, 9.0, 2.0, 4.0, 9.0, 5.0, 3.0, 9.0, 2.0, 1.0, 1.0], [1.0, 2.0, 9.0, 2.0, 4.0, 9.0, 4.0, 3.0, 9.0, 9.0, 9.0, 9.0, 2.0, 1.0, 0.0, 0.0], [9.0, 3.0, 2.0, 1.0, 2.0, 9.0, 3.0, 3.0, 9.0, 4.0, 3.0, 2.0, 1.0, 0.0, 0.0, 0.0], [3.0, 9.0, 2.0, 1.0, 2.0, 2.0, 9.0, 3.0, 2.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0], [9.0, 2.0, 2.0, 9.0, 1.0, 1.0, 2.0, 9.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 9.0, 1.0]]
  board = [list(map(int, lst)) for lst in board]
  num_rows = 30
  num_cols = 16
  num_mines = 99
  hidden = [["H" for i in range(num_cols)] for j in range(num_rows)]
  generateMoves(board, hidden, num_rows, num_cols, num_mines)