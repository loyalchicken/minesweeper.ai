from solver.logic import generateMines, convertFrom1Dto2D, generateNumbersArr, generateMoves, generateBoard
from solver.logic import unhideSurroundingSquaresWithZero, unhideSurroundingSquaresWithZeroHelper, isFlaggedComplete, unhideAllSurroundingSquares
import numpy as np

def test_generateMoves():
  board, hidden = generateBoard(30, 16, 99)
  assert generateMoves(board, hidden) == 0

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
  rows = 4
  cols = 5
  numbersArr = generateNumbersArr(mines, rows, cols)
  expected = [
    [ 9, 2, 3, 9, 2 ],
    [ 1, 2, 9, 9, 2 ],
    [ 0, 1, 2, 2, 1 ],
    [ 0, 0, 0, 0, 0 ]
  ]
  v = numbersArr == expected
  assert v.all()


def test_unhideSurroundingSquaresWithZero():
  hidden = [
    [True, True, True],
    [True, True, True],
    [True, True, True],
    [True, True, True]
  ]
  mines = [
    [0, 0, 0],
    [0, 1, 1],
    [2, 3, 9],
    [9, 9, 2]
  ]
  row_index = 0
  cols_index = 0
  rows = 4
  cols = 3
  setIndices = unhideSurroundingSquaresWithZero(hidden, mines, row_index, cols_index, rows, cols)
  expected = {(0,0), (0,1), (0,2), (1,1), (1,2), (1,0), (2,0), (2,1)}
  assert setIndices == expected


def test_isFlaggedComplete():
  visible = [
    ["flag", "hidden", "show"],
    ["hidden", "flag", "hidden"],
    ["flag", "show", "hidden"],
    ["show", "flag", "hidden"]
  ]
  row_index = 2
  cols_index = 1
  rows = 4
  cols = 3
  isComplete = isFlaggedComplete(3, visible, row_index, cols_index, rows, cols)
  assert isComplete == True

def test_unhideAllSurroundingSquares_barebones():
  visible = [
    ["flag", "hidden", "show"],
    ["hidden", "flag", "hidden"],
    ["flag", "show", "hidden"],
    ["show", "flag", "hidden"]
  ]
  mines = [
    [1, 1, 1],
    [2, 9, 1],
    [9, 3, 2],
    [2, 9, 1]
  ]
  row_index = 2
  cols_index = 1
  rows = 4
  cols = 3
  setIndices = unhideAllSurroundingSquares(visible, mines, row_index, cols_index, rows, cols)
  expected = {(1,0), (1,2), (2,2), (3,2)}
  assert setIndices == expected


def test_unhideAllSurroundingSquares_full():
  visible = [
    ["hidden", "hidden", "hidden"],
    ["hidden", "hidden", "hidden"],
    ["flag", "show", "show"],
    ["show", "flag", "show"]
  ]
  mines = [
    [0, 0, 0],
    [1, 1, 0],
    [9, 2, 1],
    [2, 9, 1]
  ]
  row_index = 2
  cols_index = 2 
  rows = 4
  cols = 3 
  setIndices = unhideAllSurroundingSquares(visible, mines, row_index, cols_index, rows, cols)
  expected = {(1,1), (1,2), (0,1), (0,0), (1,0), (0,2), (2,1), (2,2)}
  assert setIndices == expected