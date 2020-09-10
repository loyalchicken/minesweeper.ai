import numpy as np
from solver.logic.unhide_helpers import unhideSurroundingSquaresWithZero, unhideSurroundingSquaresWithZeroHelper, isFlaggedComplete, unhideAllSurroundingSquares
from solver.logic.board_helpers import convertFrom1Dto2D, generateMines, generateNumbersArr
from solver.logic.utilities import adjacent_cells_of, connected_cells_of
############################################# SOLVER #########################################################

def generateBoard(num_rows, num_cols, num_mines):
  mines = generateMines(num_rows, num_cols, num_mines)
  board = generateNumbersArr(mines, num_rows, num_cols)
  hidden = [["H" for i in range(num_cols)] for j in range(num_rows)]
  return board, hidden

def generateMoves(board, hidden, num_rows, num_cols, num_mines):
  moves = []
  cells_flagged = set()
  cell = findNextMove(board, hidden, num_rows, num_cols, num_mines) #need board to ensure first move hits a 0
  moves.append(cell)
  hidden = uncover(cell, hidden, board, num_rows, num_cols) #need board to unhide 0 patch if cell number is 0
  cells_to_flag = findDefiniteMines(hidden, num_rows, num_cols)

  cells_to_flag = (cells_to_flag | cells_flagged) - cells_flagged
  cells_flagged = cells_flagged | cells_to_flag

  while len(cells_to_flag) > 0:
    moves.append(list(map(list, list(cells_to_flag)))) #cells_to_flag is a list of lists
    hidden = flagDefiniteMines(hidden, cells_to_flag) 
    #keep clicking around the new flags 
    for cell in cells_to_flag:
      clickedCells, hidden = clickAdjacentCellsToUncover(cell, hidden, board, num_rows, num_cols) #need board to know which cells to unhide
      clickedCells = list(map(list, clickedCells))
      moves += clickedCells

    #once there are no more "clicks", keep flagging
    new_cells_to_flag = findDefiniteMines(hidden, num_rows, num_cols)

    if new_cells_to_flag == cells_to_flag:
      graph, segments, P_dict = findSegments(hidden, num_rows, num_cols)
      return moves, segments
    cells_to_flag = new_cells_to_flag
    cells_to_flag = (cells_to_flag | cells_flagged) - cells_flagged
    cells_flagged = cells_flagged | cells_to_flag
  
  graph, segments, P_dict = findSegments(hidden, num_rows, num_cols)
  
  return moves, segments

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

  nextMoves = []
  graph, segments, P_dict = findSegments(hidden, num_rows, num_cols)
  for segment in segments:
    probabilityMap = backtrack(hidden, board, segment, graph, P_dict, num_rows, num_cols)
    #append all the keys associated to value 1 to nextMoves 
  
  #if nextMoves is empty (no definite moves, we have to guess)
  #if max(probabilities) < randomProbability(), then return random hidden cell
  #else return cell with max(probability) 

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


def backtrack(hidden, board, segment, graph, P_dict, num_rows, num_cols):
  """Finds all consistent mine configurations and generates a probability map (hidden cell -> probability not a mine)
     The process of finding solutions to each segment is formulated as a Constraint Satisfaction Problem (CSP):
      - Variables: The set of n hidden cells adjacent to the segment {X1, ..., Xn}
      - Domain: {0,1}
      - Constraints: 
          Let {Y1, ..., Ym} be the set of m border cells in current segment
          Each border cell is associated with its number of adjacent hidden cells which are mines, which we call {P1, ..., Pm}
          Then, for each cell, Yi, in the segment, a constraint is given by the following equation 
              Pi = sum(graph[Yi]), where graph[Yi] is a set of Yi's adjacent hidden cells, {Xi1, ..., Xiq}

  Parameters
  ----------
  hidden     a 2D character array of visible state of cells [index by row, then column] 
  board      2D integer array [index by row, then column]
  segment    set of cells in the current segment to perform backtracking
  graph      adjacency list of all border cells in current hidden state (use this to access hidden cells adjacent to each border cell)
  P_dict     maps each border cell to its number of adjacent hidden cells which are mines {Y1: P1, ..., Ym: Pm}
  num_rows   number of rows
  num_cols   number of columns

  Returns
  -------
  A dictionary that maps hidden cells (adjacent to the current segment) to probabilities
  """
  #get all hidden cells adjacent to segment, ie. the variables 
  #domain of CSP is {0,1}
  #constraints are given by iterating through each cell in segment
  #find all possible solutions
  #assuming all solutions are equally likely, generate a probability map 
  return 0

def findSegments(hidden, num_rows, num_cols):
  """Returns a list of segments (sets of non-flagged border cells which share hidden cells) to backtrack on
  
  Parameters
  ----------
  hidden     a 2D character array of visible state of cells [index by row, then column] 
  num_rows   number of rows
  num_cols   number of columns

  Returns
  -------
  1) a dictionary that maps border cells to their adjacent hidden cells, 
  2) a list of segments (sets),
  3) a dictionary that maps each border cell to its number of adjacent hidden cells which are mines
  """
  segments=[]
  graph = dict()
  border_cells = findBorder(hidden, num_rows, num_cols)
  P_dict = dict()

  #graph: constructs undirected bipartite graph (one side hidden cells, other side border cells)
  #P_dict: initializes each cell to hidden[cell], and subtracts 1 for each adjacent flag
  for cell in border_cells:
    #we only care about cells on the border that aren't flagged
    if hidden[cell[0]][cell[1]]=="F":
      continue

    if cell not in graph:
      graph[cell]=set()

    if cell not in P_dict:
      P_dict[cell]=hidden[cell[0]][cell[1]]

    for adj in adjacent_cells_of(cell, num_rows, num_cols):
      if hidden[adj[0]][adj[1]] == "H":
        if adj not in graph:
          graph[adj]=set()
        graph[adj].add(cell)
        graph[cell].add(adj)
      if hidden[adj[0]][adj[1]] == "F":
        P_dict[cell]-=1

  #finds all connected components, and extract the border cells from component for each segment
  seen = set()
  for v, _ in graph.items():
    if v not in seen:
      seen, segment = dfs(v, graph, seen, set())
      segments.append(segment.intersection(border_cells))

  return graph, segments, P_dict

def dfs(vertex, graph, seen, segment):
  seen.add(vertex)
  segment.add(vertex)
  for adj in graph[vertex]:
    if adj not in seen:
      seen, segment = dfs(adj, graph, seen, segment)
  return seen, segment

def findBorder(hidden, num_rows, num_cols):
  """Find all cells on the border of the "non-hidden islands"  
     Recurses through each island (findBorderHelper) to find its border.  
  Parameters
  ----------
  hidden     a 2D character array of visible state of cells [index by row, then column] 
  num_rows   number of rows
  num_cols   number of columns

  Returns
  -------
  Set of cells on border
  """
  seen = set()
  border = set()

  for i in range(num_rows):
    for j in range(num_cols):
      if hidden[i][j] != "H" and (i,j) not in seen:
        new_border, seen = findBorderHelper(hidden, seen, i, j, num_rows, num_cols, border)
        border = border | new_border
  return border

def findBorderHelper(hidden, seen, row_index, cols_index, num_rows, num_cols, border):
  """Finds all cells on the border of the island (row_index, cols_index) is in
  Parameters
  ----------
  hidden     a 2D character array of visible state of cells [index by row, then column] 
  seen       set of cells on board already visited
  row_index  row index of current cell
  cols_index column index of current cell
  num_rows   number of rows
  num_cols   number of columns
  border     the cells in the border of current island so far

  Returns
  -------
  Set of cells on border of current island
  """
  if hidden[row_index][cols_index] == "H" or (row_index,cols_index) in seen:
    return border, seen
  seen.add((row_index,cols_index))

  #any cell adjacent to a hidden cell is considered on the border
  for cell in adjacent_cells_of((row_index,cols_index), num_rows, num_cols):
    if hidden[cell[0]][cell[1]] == "H":
      border.add((row_index,cols_index))
  
  #only recurse on connected cells (ie. ones that share an edge)
  for cell in connected_cells_of((row_index,cols_index), num_rows, num_cols):
    border, seen = findBorderHelper(hidden, seen, cell[0], cell[1], num_rows, num_cols, border)
  return border, seen

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
  return cells

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
  for cell in adjacent_cells_of((row_index, cols_index), num_rows, num_cols):
    if hidden[cell[0]][cell[1]]=="H" or hidden[cell[0]][cell[1]]=="F":
      num_hidden += 1
      hiddenSet.add((int(cell[0]),int(cell[1])))
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
  """Iterates through the adjacent cells of the flagged cell and clickCellToUncover(adj cell)
  Parameters
  ----------
  cell      the current flagged cell (tuple) 
  hidden    a 2D array of visible state of cells [index by row, then column] 
  board     a 2D integer array [index by row, then column]
  num_rows  number of rows
  num_cols  number of columns

  Returns
  -------
  A set of tuples (adjacent cells to click based on the current flagged cell), as well as updated hidden. 
  """
  cells_clicked = []
  seen = set()
  for adj in adjacent_cells_of(cell, num_rows, num_cols):
    cells_clicked, hidden = clickCellsToUncoverHelper(adj, cells_clicked, seen, hidden, board, num_rows, num_cols)
  return cells_clicked, hidden

def clickCellsToUncoverHelper(cell, cells_clicked, seen, hidden, board, num_rows, num_cols): 
  """Finds all shown cells to click based on possibly initially clicking cell
  If the cell is shown and isFlaggedComplete(cell), click cell if clicking the cell uncovers a nonzero number of cells
  Recurse on each cell that's uncovered by this clicking this cell
  Parameters
  ----------
  cell            the cell to click if it hasn't already been clicked
  cells_clicked   a list of the cells to click (in order)
  seen            a set to keep track of cells that already have been clicked 
  hidden          a 2D array of visible state of cells [index by row, then column] 
  board           a 2D integer array [index by row, then column]
  num_rows        number of rows
  num_cols        number of columns

  Returns
  -------
  A list of the cells to click, as well as updated hidden. 
  """
  if cell in seen:
    return cells_clicked, hidden
  
  row_index = int(cell[0])
  cols_index = int(cell[1])
  if hidden[row_index][cols_index] in [1,2,3,4,5,6,7,8] and isFlaggedComplete(hidden[row_index][cols_index], hidden, row_index, cols_index, num_rows, num_cols):
    seen.add(cell)
    cells_to_unhide = unhideAllSurroundingSquares(hidden, board, row_index, cols_index, num_rows, num_cols)
    if len(cells_to_unhide) > 0:
      cells_clicked.append((row_index, cols_index))
    for c in cells_to_unhide:
      hidden[int(c[0])][int(c[1])]=board[int(c[0])][int(c[1])]
    for c in cells_to_unhide:
      cells_clicked, hidden = clickCellsToUncoverHelper(c, cells_clicked, seen, hidden, board, num_rows, num_cols)
  return cells_clicked, hidden