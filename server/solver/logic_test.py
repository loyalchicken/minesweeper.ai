from solver.logic import generateMines, convertFrom1Dto2D, generateNumbersArr
import numpy as np


def test_generateMines():
  assert len(np.unique(generateMines(30,30,900))) == 900

def test_convert1Dto2D():
  assert convertFrom1Dto2D(7, 4) == (3,1)
  assert convertFrom1Dto2D(3, 4) == (3,0)
  assert convertFrom1Dto2D(0, 4) == (0,0)
  assert convertFrom1Dto2D(8, 4) == (0,2)

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