################################## GENERATING BOARD LOGIC #####################################################

import numpy as np

def generateMines(num_rows, num_cols, num_mines):
  """Generates a list of numbers corresponding to the 1D coordinates of the squares that are mines.
     O(n) time, where n = num_rows*num_cols
  
  Parameters
  ----------
  num_rows   number of rows
  num_cols   number of columns
  num_mines  number of mines

  Returns
  -------
  a list of numbers
  """
  arr = np.random.permutation(num_rows * num_cols)
  return arr[:num_mines]


def generateNumbersArr(mines, num_rows, num_cols):
  """Generates a 2D array of numbers, where the value of each index is the number of mines a cell is adjacent to.

  Parameters
  ----------
  mines      list of numbers corresponding to the 1D coordinates of the cells that are mines 
  num_rows   number of rows
  num_cols   number of columns

  Returns
  -------
  2D array of numbers (col, row)
  """
  minesIn2D = [convertFrom1Dto2D(mine, num_cols) for mine in mines] 
  minesSet = set(minesIn2D) #set of tuples

  #initialize a 2D array
  #newArr = new Array(rows).fill(0).map(() => new Array(cols).fill(0));
  newArr = np.zeros(shape=(num_rows, num_cols))
  for i in range(num_rows):
    for j in range(num_cols):
      if ((i, j) in minesSet):
         newArr[i][j]=9
      else:
        newArr[i][j]=numNeighbors(minesSet, i, j, num_cols, num_rows)
  return newArr


def numNeighbors(minesSet, row_index, cols_index, num_cols, num_rows):
  """Finds the number of neighbors of current cell that are mines.

  Parameters
  ----------
  minesSet   set (of 2D coords or tuples) of mines
  row_index  row index of current cell
  cols_index  column index of current cell
  num_rows   number of rows
  num_cols   number of columns

  Returns
  -------
  Number of neighbors that are mines
  """
  mines = 0
  for j in np.arange(max(0, cols_index-1), min(num_cols-1, cols_index+1)+1):
    for i in np.arange(max(0, row_index-1), min(num_rows-1, row_index+1)+1):
      if ((i, j) in minesSet):
        mines+=1
  return mines


def convertFrom1Dto2D(coord, num_cols):
  """Converts 1D coordinate to 2D coordinate (row, cols).

  Parameters
  ----------
  coord      a number
  num_cols   number of columns

  Returns
  -------
  2D coordinate, a tuple
  """
  y = int(np.floor(coord/num_cols))
  x = coord % num_cols
  return (y,x)