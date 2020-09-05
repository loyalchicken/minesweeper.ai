import numpy as np

def generateBoard(num_rows, num_cols, num_mines):
  mines = generateMines(num_rows, num_cols, num_mines)
  board = generateNumbersArr(mines, num_rows, num_cols)
  hidden = [["H" for i in range(num_cols)] for j in range(num_rows)]
  return board, hidden


# generateMoves:
# while not win / don't have to guess:
#1. findNextMove(current board) --> return a cell
#2. uncover(cell)
  #a. if a zero is clicked on, then unhideSurroundingSquaresWithZero
#3. while there are definite mines (iterate through borders to get set of definite mines):
      #for all shown cells that are definite mines: 
        #a. flagCell()
        #b. for all shown cells around flag, if isFlaggedComplete, click cell to unhideAllSurroundingSquares

def generateMoves(board, hidden, num_rows, num_cols, num_mines):
  moves = []

  cell = findNextMove(board, hidden, num_rows, num_cols, num_mines) #need board to ensure first move hits a 0
  moves.append(cell)

  hidden = uncover(cell, hidden, board, num_rows, num_cols) #need board to unhide 0 patch if cell number is 0

  #mines = findDefiniteMines(hidden)
  #while len(mines) > 0:
    #hidden = flagDefiniteMines(hidden, board, mines) 
    #moves.append(mines) #mines is a list of tuples
    #for mine in mines:
      #hidden = clickSurroundingCellIfFlaggingComplete(mine, hidden, board) #need board to know unhide surrounding cells/0 patch

  #after flagging/uncovering based on first click, keep going if possible
  #definiteMines = findDefiniteMines(hidden)
 
  return 0

############################################# SOLVER #########################################################

def uncover(cell, hidden, board, num_rows, num_cols):
  """Updates cell in hidden to "S", unhide adjacent "0" patch if cell is 0, and return updated hidden.

  Parameters
  ----------
  cell     a tuple of cell's coordinates
  hidden   a 2D   array of visible state of cells [index by row, then column] 

  Returns
  -------
  Updated 2D character array
  """
  row_index = cell[0]
  cols_index = cell[1]
  hidden[row_index][cols_index]="S"
  if board[row_index][cols_index] == 0:
    cells_to_unhide = unhideSurroundingSquaresWithZero(board, row_index, cols_index, num_rows, num_cols)
    for c in cells_to_unhide:
      hidden[c[0]][c[1]]="S"
  return hidden


def findNextMove(board, hidden, num_rows, num_cols, num_mines):
  """Returns the cell (tuple) to next uncover.

  Parameters
  ----------
  board      2D integer array [index by row, then column]
  hidden     a 2D character array of visible state of cells [index by row, then column] 
  num_rows   number of rows
  num_cols   number of columns
  num_mines  number of mines

  Returns
  -------
  A tuple
  """
  #choose a random cell on the board (0 -> size of board-1)
  if firstMove(hidden, num_rows, num_cols):
    return findRandomZeroCell(board, num_rows, num_cols)

####### findNextMove HELPER FUNCTIONS ########
def firstMove(hidden, num_rows, num_cols):
  """Checks whether all cells in board are hidden.
  
  Parameters
  ----------
  hidden     a 2D character array of visible state of cells [index by row, then column] 
  num_rows   number of rows
  num_cols   number of columns

  Returns
  -------
  A boolean
  """
  return len(np.argwhere(np.array(hidden)=='H')) == num_rows*num_cols

def findRandomZeroCell(board, num_rows, num_cols):
  """Finds a random cell (tuple) that has number "0"
  
  Parameters
  ----------
  board      2D integer array [index by row, then column]
  num_rows   number of rows
  num_cols   number of columns

  Returns
  -------
  A tuple
  """
  row_index, cols_index = convertFrom1Dto2D(np.random.randint(num_rows*num_cols), num_cols)
  while board[row_index][cols_index] != 0:
      row_index, cols_index = convertFrom1Dto2D(np.random.randint(num_rows*num_cols), num_cols)
  return (row_index, cols_index)

######################## UNCOVERING CELLS AND FLAGGING HELPER FUNCTIONS ########################################

def unhideSurroundingSquaresWithZero(board, row_index, cols_index, num_rows, num_cols):
  """Unhides the surrounding "0" cells of the current cell (row_index, cols_index).
 
  Parameters
  ----------
  board       2D integer array [index by row, then column]
  num_rows    number of rows
  num_cols    number of columns
  row_index   row index of current cell
  cols_index  column index of current cell

  Returns
  -------
  A set of 2D indices (tuples) that need to be hidden
  """
  setOfHiddenIndices = set()
  setOfSeenIndices = set()
  unhideSurroundingSquaresWithZeroHelper(board, row_index, cols_index, num_rows, num_cols, setOfHiddenIndices, setOfSeenIndices)
  return setOfHiddenIndices

def unhideSurroundingSquaresWithZeroHelper(board, row_index, cols_index, num_rows, num_cols, setOfHiddenIndices, setOfSeenIndices):
  setOfSeenIndices.add((row_index, cols_index))
  for i in np.arange(max(0, row_index-1), min(num_rows-1, row_index+1)+1):
    for j in np.arange(max(0, cols_index-1), min(num_cols-1, cols_index+1)+1):
      setOfHiddenIndices.add((i,j))
      if (board[i][j]==0 and (i,j) not in setOfSeenIndices):
        unhideSurroundingSquaresWithZeroHelper(board, i, j, num_rows, num_cols, setOfHiddenIndices, setOfSeenIndices)


def isFlaggedComplete(num_adjacent_mines, board, row_index, cols_index, num_rows, num_cols):
  """Checks whether the number of adjacent cells flagged equals the number of the cell's neighboring mines.
  
  Parameters
  ----------
  num_adjacent_mines   the number of adjacent cells which are mines
  board                2D integer array [index by row, then column]
  row_index            row index of current cell
  cols_index           column index of current cell
  num_rows             number of rows
  num_cols             number of columns

  Returns
  -------
  A boolean
  """
  num_flagged = 0
  for i in np.arange(max(0, row_index-1), min(num_rows-1, row_index+1)+1):
    for j in np.arange(max(0, cols_index-1), min(num_cols-1, cols_index+1)+1):
      if board[i][j]=="F":
        num_flagged+=1
  return num_flagged == num_adjacent_mines

def unhideAllSurroundingSquares(hidden, board, row_index, cols_index, num_rows, num_cols):
  """Unhides all neighboring cells that aren't flagged, including all "0" patches if a neighboring cell has "0".

  Parameters
  ----------
  board        2D integer array [index by row, then column]
  hidden       a 2D character array of visible state of cells [index by row, then column] 
  row_index    row index of current cell
  cols_index   column index of current cell
  num_rows     number of rows
  num_cols     number of columns
  num_mines    number of mines

  Returns a set of 2D indices (tuples) that need to be hidden
  -------
  A tuple
  """
  setOfHiddenIndices = set()
  for i in np.arange(max(0, row_index-1), min(num_rows-1, row_index+1)+1):
    for j in np.arange(max(0, cols_index-1), min(num_cols-1, cols_index+1)+1):
      if hidden[i][j]=="H":
         setOfHiddenIndices.add((i,j))
      if board[i][j]==0:
        patchZeroSet = unhideSurroundingSquaresWithZero(board, i, j, num_rows, num_cols)
        setOfHiddenIndices.update(list(patchZeroSet))
  return setOfHiddenIndices



################################## GENERATING BOARD LOGIC #####################################################

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