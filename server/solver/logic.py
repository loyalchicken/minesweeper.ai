import numpy as np

def generateBoard(num_rows, num_cols, num_mines):
  mines = generateMines(num_rows, num_cols, num_mines)
  board = generateNumbersArr(mines, num_rows, num_cols)
  hidden = [[True for i in range(num_cols)] for j in range(num_rows)]
  return board, hidden

def generateMoves(board, hidden):
  return 0

############################################# SOLVER #########################################################

#def uncover(cell, hidden, board):


#def findNextMove(hidden, num_rows, num_cols, num_mines):

#while not win / don't have to guess:
#1. findNextMove(current board) --> return a cell
#2. uncover(cell)
  #a. if a zero is clicked on, then unhideSurroundingSquaresWithZero
#3. while there are definite mines (iterate through borders to get set of definite mines):
      #for all shown cells that are definite mines: 
        #a. flagCell()
        #b. for all shown cells around flag, if isFlaggedComplete, click cell to unhideAllSurroundingSquares



########################### UNCOVERING CELLS AND FLAGGING LOGIC ###############################################

###
 # Unhides the surrounding "0" cells of the current cell (row_index, cols_index)
 # @param hidden: a 2D boolean array [index by row, then column] 
 # @param mines: 2D integer array [index by row, then column]
 # @param row_index: current cell row index
 # @param cols_index: current cell column index
 # @param rows (number of rows)
 # @param cols (number of columns)
 # @return set of 2D indices (tuples) that need to be hidden   
###
def unhideSurroundingSquaresWithZero(hidden, mines, row_index, cols_index, rows, cols):
  setOfHiddenIndices = set()
  setOfSeenIndices = set()
  unhideSurroundingSquaresWithZeroHelper(hidden, mines, row_index, cols_index, rows, cols, setOfHiddenIndices, setOfSeenIndices)
  return setOfHiddenIndices

def unhideSurroundingSquaresWithZeroHelper(hidden, mines, row_index, cols_index, rows, cols, setOfHiddenIndices, setOfSeenIndices):
  setOfSeenIndices.add((row_index, cols_index))
  for i in np.arange(max(0, row_index-1), min(rows-1, row_index+1)+1):
    for j in np.arange(max(0, cols_index-1), min(cols-1, cols_index+1)+1):
      setOfHiddenIndices.add((i,j))
      if (mines[i][j]==0 and (i,j) not in setOfSeenIndices):
        unhideSurroundingSquaresWithZeroHelper(hidden, mines, i, j, rows, cols, setOfHiddenIndices, setOfSeenIndices)

###
 # Checks whether the number of adjacent cells flagged equals the number of the cell's neighboring mines
 # @param numMines: the number of adjacent cells which are mines
 # @param visible: 2D integer array of current status of cells [index by row, then column]
 # @param row_index: current cell row index
 # @param cols_index: current cell column index
 # @param rows (number of rows)
 # @param cols (number of columns)
 # @return boolean   
 ###
def isFlaggedComplete(numMines, visible, row_index, cols_index, rows, cols):
  numFlagged = 0
  for i in np.arange(max(0, row_index-1), min(rows-1, row_index+1)+1):
    for j in np.arange(max(0, cols_index-1), min(cols-1, cols_index+1)+1):
      if visible[i][j]=="flag":
        numFlagged+=1
  return numFlagged == numMines

###
 # Unhides all neighboring cells that aren't flagged, including all "0" patches if a neighboring cell has "0" 
 # @param mines: 2D integer array [index by row, then column]
 # @param visible: 2D integer array of current status of cells [index by row, then column]
 # @param row_index: current cell row index
 # @param cols_index: current cell column index
 # @param rows (number of rows)
 # @param cols (number of columns)
 # @return set of 2D indices (tuples) that need to be hidden   
###
def unhideAllSurroundingSquares(visible, mines, row_index, cols_index, rows, cols):
  setOfHiddenIndices = set()
  for i in np.arange(max(0, row_index-1), min(rows-1, row_index+1)+1):
    for j in np.arange(max(0, cols_index-1), min(cols-1, cols_index+1)+1):
      if visible[i][j]=="hidden":
         setOfHiddenIndices.add((i,j))
      if mines[i][j]==0:
        patchZeroSet = unhideSurroundingSquaresWithZero(visible, mines, i, j, rows, cols)
        setOfHiddenIndices.update(list(patchZeroSet))
  return setOfHiddenIndices


################################## GENERATING BOARD LOGIC #####################################################

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

###
 # Finds the number of neighbors of current cell that are mines
 # @param minesSet: set (of 2D coords or tuples) of mines
 # @param x: col_index of current cell
 # @param y: row_index of current cell
 # @return number of neighbors that are mines
###
def numNeighbors(minesSet, row_index, col_index, num_cols, num_rows):
  mines = 0
  for j in np.arange(max(0, col_index-1), min(num_cols-1, col_index+1)+1):
    for i in np.arange(max(0, row_index-1), min(num_rows-1, row_index+1)+1):
      if ((i, j) in minesSet):
        mines+=1
  return mines

###
 # Converts 1D coordinate to 2D coordinate (row, cols)
 # @param mine: a number 
 # @param cols: number of columns
 # @return tuple, 2D coordinate  
###
def convertFrom1Dto2D(mines, num_cols):
  y = int(np.floor(mines/num_cols))
  x = mines % num_cols
  return (y,x)