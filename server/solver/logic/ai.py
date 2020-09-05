import numpy as np
from solver.logic.unhide_helpers import unhideSurroundingSquaresWithZero, unhideSurroundingSquaresWithZeroHelper, isFlaggedComplete, unhideAllSurroundingSquares
from solver.logic.board_helpers import convertFrom1Dto2D, generateMines, generateNumbersArr

############################################# SOLVER #########################################################

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
        #b. for all shown cells around flag, if isComplete("F"), click cell to unhideAllSurroundingSquares

def generateMoves(board, hidden, num_rows, num_cols, num_mines):
  moves = []

  cell = findNextMove(board, hidden, num_rows, num_cols, num_mines) #need board to ensure first move hits a 0
  moves.append(cell)

  hidden = uncover(cell, hidden, board, num_rows, num_cols) #need board to unhide 0 patch if cell number is 0

  print(hidden)
  mines = findDefiniteMines(hidden)
  #while len(mines) > 0:
    #hidden = flagDefiniteMines(hidden, board, mines) 
    #moves.append(mines) #mines is a list of tuples
    #for mine in mines:
      #hidden = clickSurroundingCellIfFlaggingComplete(mine, hidden, board) #need board to know unhide surrounding cells/0 patch

    #after flagging/uncovering based on first click, keep going if possible
    #mines = findDefiniteMines(hidden)
 
  return 0


######################################## GENERATE MOVES HELPERS ########################################################

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


def uncover(cell, hidden, board, num_rows, num_cols):
  """Updates cell in hidden to "S", unhide adjacent "0" patch if cell is 0, and return updated hidden.

  Parameters
  ----------
  cell     a tuple of cell's coordinates
  hidden   a 2D array of visible state of cells [index by row, then column] 

  Returns
  -------
  Updated 2D character array
  """
  row_index = cell[0]
  cols_index = cell[1]
  hidden[row_index][cols_index]=board[row_index][cols_index]
  if board[row_index][cols_index] == 0:
    cells_to_unhide = unhideSurroundingSquaresWithZero(board, row_index, cols_index, num_rows, num_cols)
    for c in cells_to_unhide:
      hidden[c[0]][c[1]]=board[c[0]][c[1]]
  return hidden



def findDefiniteMines(hidden, num_rows, num_cols):
  """Returns the cells which are definitely mines (to be flagged) by iterating through all shown cells
  
  Parameters
  ----------
  hidden               a 2D character array of visible state of cells [index by row, then column] 
  num_rows             number of rows
  num_cols             number of columns

  Returns
  -------
  A set of tuples
  """
  #for each cell on border, check the number of adjacent hidden cells
  cells = set()
  for i in range(num_rows):
    for j in range(num_cols):
      if hidden[i][j] in [1,2,3,4,5,6,7,8]:
        complete, hiddenCells = isHiddenComplete(hidden[i][j], hidden, i, j, num_rows, num_cols)
        if complete: 
          cells = cells | hiddenCells
  return cells


def isHiddenComplete(num_adjacent_mines, hidden, row_index, cols_index, num_rows, num_cols):
  """Checks whether the number of adjacent cells hidden equals the number of the cell,
     and returns the cell coordinates of the adjacent hidden cells.
  
  Parameters
  ----------
  num_adjacent_mines   the number of adjacent cells which are mines
  hidden               a 2D character array of visible state of cells [index by row, then column] 
  row_index            row index of current cell
  cols_index           column index of current cell
  num_rows             number of rows
  num_cols             number of columns

  Returns
  -------
  A tuple, with the first index a boolean, second index a set of cells which are hidden
  """
  hiddenSet = set()
  num_hidden = 0
  for i in np.arange(max(0, row_index-1), min(num_rows-1, row_index+1)+1):
    for j in np.arange(max(0, cols_index-1), min(num_cols-1, cols_index+1)+1):
      if hidden[i][j]=="H":
        num_hidden += 1
        hiddenSet.add((i,j))
  return num_hidden == num_adjacent_mines, hiddenSet


#def flagDefiniteMines(hidden, board, mines):
