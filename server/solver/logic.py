import numpy as np

def generateBoard(num_rows, num_cols, num_mines):
  mines = generateMines(num_rows, num_cols, num_mines)
  return generateNumbersArr(mines, num_rows, num_cols)

 ### Generates a list of numbers corresponding to the 1D coordinates of the squares that are mines  
 # O(n) time, where n = num_rows*num_cols 
 # @param numMines (number of mines)
 # @param rows (number of rows)
 # @param cols (number of cols)
 # @return a list of numbers
 ###
def generateMines(num_rows, num_cols, num_mines):
  arr = np.random.permutation(num_rows * num_cols)
  return arr[:num_mines]

###
 # Generates a 2D array of numbers, where the value of each index is the number of mines a square is adjacent to
 # @param mines: list of numbers corresponding to the 1D coordinates of the squares that are mines
 # @return 2D array of numbers (col, row)
###
def generateNumbersArr(mines, num_rows, num_cols):
  minesIn2D = [convertFrom1Dto2D(mine, num_cols) for mine in mines]
  minesSet = set(minesIn2D)

  #initialize a 2D array
  #newArr = new Array(rows).fill(0).map(() => new Array(cols).fill(0));
  newArr = np.zeros(shape=(num_rows, num_cols))
  for i in range(num_rows):
    for j in range(num_cols):
      if ((j, i) in minesSet):
         newArr[i][j]=9
      else:
        newArr[i][j]=numNeighbors(minesSet, j, i, num_cols, num_rows)
  return newArr

###
 # Finds the number of neighbors of current cell that are mines
 # @param minesSet: set (of 2D coords) of mines
 # @param x: col_index of current cell
 # @param y: row_index of current cell
 # @return number of neighbors that are mines
###
def numNeighbors(minesSet, x, y, num_cols, num_rows):
  mines = 0
  x_arr = np.arange(max(0, x-1), min(num_cols-1, x+1)+1)
  y_arr = np.arange(max(0, y-1), min(num_rows-1, y+1)+1)
  for i in x_arr:
    for j in y_arr:
      if ((i, j) in minesSet):
        mines+=1
  return mines

###
 # Converts 1D coordinate to 2D coordinate (cols, row)
 # @param mine: a number 
 # @param cols: number of columns
 # @return 2D coordinate  
###
def convertFrom1Dto2D(mines, num_cols):
  y = int(np.floor(mines/num_cols))
  x = mines % num_cols
  return (x,y)





