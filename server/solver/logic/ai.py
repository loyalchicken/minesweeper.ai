import numpy as np
from solver.logic.unhide_helpers import unhideSurroundingSquaresWithZero, unhideSurroundingSquaresWithZeroHelper, isFlaggedComplete, unhideAllSurroundingSquares
from solver.logic.board_helpers import convertFrom1Dto2D, generateMines, generateNumbersArr
from solver.logic.utilities import adjacent_cells_of
############################################# SOLVER #########################################################

def generateBoard(num_rows, num_cols, num_mines):
  mines = generateMines(num_rows, num_cols, num_mines)
  board = generateNumbersArr(mines, num_rows, num_cols)
  hidden = [["H" for i in range(num_cols)] for j in range(num_rows)]
  return board, hidden

def generateMoves(board, hidden, num_rows, num_cols, num_mines):
  
  moves = []
  cell = findNextMove(board, hidden, num_rows, num_cols, num_mines) #need board to ensure first move hits a 0
  moves.append(cell)
  hidden = uncover(cell, hidden, board, num_rows, num_cols) #need board to unhide 0 patch if cell number is 0
  cells_to_flag = findDefiniteMines(hidden, num_rows, num_cols)

  while len(cells_to_flag) > 0:
    moves.append(cells_to_flag) #cells_to_flag is a list of lists
    hidden = flagDefiniteMines(hidden, cells_to_flag) 
    print(hidden)
    #keep clicking around the new flags 
    for cell in cells_to_flag:
      clickedCells, hidden = clickAdjacentCellsToUncover(cell, hidden, board, num_rows, num_cols) #need board to know which cells to unhide
      clickedCells = list(map(list, clickedCells))
      print(clickedCells)
      moves += clickedCells

    #once there are no more "clicks", keep flagging
    new_cells_to_flag = findDefiniteMines(hidden, num_rows, num_cols)
    if new_cells_to_flag == cells_to_flag:
      return moves
    cells_to_flag = new_cells_to_flag
  return moves

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
  A list of 2 elements (row index, col index)
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
  A list of 2 elements (row index, column index)
  """
  row_index, cols_index = convertFrom1Dto2D(np.random.randint(num_rows*num_cols), num_cols)
  while board[row_index][cols_index] != 0:
      row_index, cols_index = convertFrom1Dto2D(np.random.randint(num_rows*num_cols), num_cols)
  return [int(row_index), int(cols_index)]


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
  hidden     a 2D character array of visible state of cells [index by row, then column] 
  num_rows   number of rows
  num_cols   number of columns

  Returns
  -------
  A set of tuples --> a list of lists (of 2 elements (row index, col index))
  """
  #for each cell on border, check the number of adjacent hidden cells
  cells = set()
  for i in range(num_rows):
    for j in range(num_cols):
      if hidden[i][j] in [1,2,3,4,5,6,7,8]:
        complete, hiddenCells = isHiddenComplete(hidden[i][j], hidden, i, j, num_rows, num_cols)
        if complete: 
          cells = cells | hiddenCells
  return list(map(list, list(cells)))


def isHiddenComplete(num_adjacent_mines, hidden, row_index, cols_index, num_rows, num_cols):
  """Checks whether the number of adjacent cells hidden + flagged equals the number of the cell,
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
      if hidden[i][j]=="H" or hidden[i][j]=="F":
        num_hidden += 1
        hiddenSet.add((int(i),int(j)))
  return num_hidden == num_adjacent_mines, hiddenSet


def flagDefiniteMines(hidden, mines):
  """Updates the cells that are definite mines in hidden to "F", and return updated hidden.

  Parameters
  ----------
  hidden   a 2D array of visible state of cells [index by row, then column] 
  mines    the set of tuples (2d coordinates) of cells to be flagged as mines

  Returns
  -------
  Updated 2D hidden array
  """
  for cell in mines:
    row_index = cell[0]
    cols_index = cell[1]
    hidden[row_index][cols_index]="F"
  return hidden

def clickAdjacentCellsToUncover(cell, hidden, board, num_rows, num_cols):
  """Clicks the adjacent cells of the flagged cell if isFlaggedComplete(adjacent cell), 
     and unhideAllSurroundingSquares of the clicked adjacent cells.
     Updates hidden to reflect newly uncovered cells

  Parameters
  ----------
  cell      the current cell (tuple) 
  hidden    a 2D array of visible state of cells [index by row, then column] 
  board     a 2D integer array [index by row, then column]
  num_rows  number of rows
  num_cols  number of columns

  Returns
  -------
  A set of tuples (adjacent cells clicked), as well as the updated hidden. 
  """
  cells_clicked = []
  seen = set()
  for adj in adjacent_cells_of(cell, num_rows, num_cols):
    print(cell, adj)
    cells_clicked, hidden = clickCellsToUncoverHelper(cell, adj, cells_clicked, seen, hidden, board, num_rows, num_cols)
  return cells_clicked, hidden

def clickCellsToUncoverHelper(og_cell, adj, cells_clicked, seen, hidden, board, num_rows, num_cols):  
  if adj in seen:
    return cells_clicked, hidden
  
  row_index = int(adj[0])
  cols_index = int(adj[1])
  if hidden[row_index][cols_index] in [1,2,3,4,5,6,7,8] and isFlaggedComplete(hidden[row_index][cols_index], hidden, row_index, cols_index, num_rows, num_cols):
    seen.add(adj)
    cells_to_unhide = unhideAllSurroundingSquares(hidden, board, row_index, cols_index, num_rows, num_cols)
    if len(cells_to_unhide) > 0:
      cells_clicked.append((row_index, cols_index))
    for c in cells_to_unhide:
      hidden[int(c[0])][int(c[1])]=board[int(c[0])][int(c[1])]
      cells_clicked, cells_to_unhide = clickCellsToUncoverHelper(og_cell, c, cells_clicked, seen, hidden, board, num_rows, num_cols)
  return cells_clicked, hidden