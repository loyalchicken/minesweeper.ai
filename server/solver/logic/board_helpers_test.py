from solver.logic.board_helpers import generateMines, convertFrom1Dto2D, generateNumbersArr

import numpy as np

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
