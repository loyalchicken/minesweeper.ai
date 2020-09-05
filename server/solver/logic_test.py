from solver.logic import generateMines, convertFrom1Dto2D, generateNumbersArr, generateMoves, generateBoard
from solver.logic import unhideSurroundingSquaresWithZero, unhideSurroundingSquaresWithZeroHelper, isFlaggedComplete, unhideAllSurroundingSquares
from solver.logic import firstMove, findRandomZeroCell, uncover

import numpy as np

def test_generateMoves():
  num_rows=30
  num_cols=16
  num_mines=99
  board, hidden = generateBoard(num_rows, num_cols, num_mines)
  assert generateMoves(board, hidden, num_rows, num_cols, num_mines) == 0

######################################## SOLVER LOGIC #########################################################

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
    ["S", "S", "S"],
    ["S", "S", "S"],
    ["S", "S", "H"],
    ["H", "H", "H"]
  ]
  assert uncover(cell, hidden, board, num_rows, num_cols) == updatedHidden

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
  assert findRandomZeroCell(board, num_rows, num_cols) == (1,2)
  assert findRandomZeroCell(board2, num_rows, num_cols) == (0,0)

#######################################################################################################################
def test_generateMines():
  assert len(np.unique(generateMines(30,30,900))) == 900

def test_convert1Dto2D():
  assert convertFrom1Dto2D(7, 4) == (1,3)
  assert convertFrom1Dto2D(3, 4) == (0,3)
  assert convertFrom1Dto2D(0, 4) == (0,0)
  assert convertFrom1Dto2D(8, 4) == (2,0)

def test_generateNumbersArr():
  mines = [0,3, 7,8]
  num_rows = 4
  num_cols = 5
  numbersArr = generateNumbersArr(mines, num_rows, num_cols)
  expected = [
    [ 9, 2, 3, 9, 2 ],
    [ 1, 2, 9, 9, 2 ],
    [ 0, 1, 2, 2, 1 ],
    [ 0, 0, 0, 0, 0 ]
  ]
  v = numbersArr == expected
  assert v.all()


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
  row_index = 2
  cols_index = 1
  num_rows = 4
  num_cols = 3
  isComplete = isFlaggedComplete(3, hidden, row_index, cols_index, num_rows, num_cols)
  assert isComplete == True

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