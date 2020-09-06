######################## UNCOVERING CELLS AND FLAGGING HELPER FUNCTIONS ########################################
import numpy as np

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


def isFlaggedComplete(num_adjacent_mines, hidden, row_index, cols_index, num_rows, num_cols):
  """Checks whether the number of adjacent cells flagged equals the number of the cell's neighboring mines.
  
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
  A boolean 
  """

  num_flagged = 0
  for i in np.arange(max(0, row_index-1), min(num_rows-1, row_index+1)+1):
    for j in np.arange(max(0, cols_index-1), min(num_cols-1, cols_index+1)+1):
      if hidden[i][j]=="F":
        num_flagged += 1
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