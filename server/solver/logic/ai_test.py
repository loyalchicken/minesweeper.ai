from solver.logic.ai import firstMove, findRandomZeroCell, uncover, findDefiniteMines, isHiddenComplete, flagDefiniteMines, clickAdjacentCellsToUncover
from solver.logic.ai import generateBoard, generateMoves 
from solver.logic.ai import findSegments, dfs, findBorder, findBorderHelper
from solver.logic.ai import isAssignmentConsistent, getAllAdjacentHiddenCellsOfSegment, selectUnassignedVariable, backtrack, getProbabilityDistr
from solver.logic.utilities import round_dict

import numpy as np

def test_generateMoves():
  num_rows=30
  num_cols=16
  num_mines=99
  board, hidden = generateBoard(num_rows, num_cols, num_mines)
  #assert generateMoves(board, hidden, num_rows, num_cols, num_mines) == 0

######################################## SOLVER LOGIC #########################################################

def test_firstMove():
  hidden = [
    ["H", "H", "H"],
    ["H", "H", "H"]
  ]
  hidden2 = [
    ["S", "H", "H"],
    ["H", "H", "H"]
  ]
  num_rows = 2
  num_cols = 3
  assert firstMove(hidden, num_rows, num_cols) == True
  assert firstMove(hidden2, num_rows, num_cols) == False

def test_findRandomZeroCell():
  board = [
    [1, 2, 1],
    [1, 4, 0]
  ]
  board2 = [
    [0, 2, 1],
    [1, 4, 2]
  ]
  num_rows=2
  num_cols=3
  assert findRandomZeroCell(board, num_rows, num_cols) == [[1,2]]
  assert findRandomZeroCell(board2, num_rows, num_cols) == [[0,0]]

def test_backtrack():
  hidden = [
    [1,     2,   3],
    [1,     1,   1],
    ["H", "H", "H"],
    ["H",   2, "F"]
  ]
  graph = {
    (2,0): {(1,0), (1,1), (3,1)}, 
    (2,1): {(1,0), (1,1), (1,2), (3,1)},
    (2,2): {(1,1), (1,2), (3,1)},
    (3,0): {(3,1)},
    (1,0): {(2,0), (2,1)},
    (1,1): {(2,0), (2,1), (2,2)},
    (1,2): {(2,1), (2,2)},
    (3,1): {(3,0), (2,0), (2,1), (2,2)}
  }
  segment = {(3, 1), (1, 2), (1, 0), (1, 1)}
  P_dict = {
    (1,0): 1,
    (1,1): 1,
    (1,2): 1,
    (3,1): 1
  }
  solutions = backtrack(hidden, segment, graph, P_dict)
  expected_solutions = [{(2, 0): 0, (2, 1): 1, (2, 2): 0, (3, 0): 0}]
  assert solutions == expected_solutions

def test_backtrack20():
  hidden = [
    [1,     1,   1],
    ["H", "H", "H"],
    ["H", "H", "H"],
    [1,   "H",   1]
  ]
  graph = {
    (0,0): {(1,0), (1,1)},
    (0,1): {(1,0), (1,1), (1,2)},
    (0,2): {(1,1), (1,2)},
    (3,0): {(2,0), (2,1), (3,1)},
    (3,2): {(3,1), (2,1), (2,2)},
    (1,0): {(0,0), (0,1)},
    (1,1): {(0,0), (0,1), (0,2)},
    (1,2): {(0,1), (0,2)},
    (2,0): {(3,0)},
    (2,1): {(3,0), (3,2)},
    (3,1): {(3,0), (3,2)},
    (2,2): {(3,2)}
  }
  segment = {(0,0), (0,1), (0,2)}
  P_dict = {
    (0,0): 1,
    (0,1): 1,
    (0,2): 1,
    (3,0): 1,
    (3,2): 1
  }
  solutions = backtrack(hidden, segment, graph, P_dict)
  expected_solutions = [{(1,0): 0, (1,1): 1, (1,2): 0}]
  assert solutions == expected_solutions

def test_backtrack21():
  hidden = [
    [1,     1,   1],
    ["H", "H", "H"],
    ["H", "H", "H"],
    [1,   "H",   1]
  ]
  graph = {
    (0,0): {(1,0), (1,1)},
    (0,1): {(1,0), (1,1), (1,2)},
    (0,2): {(1,1), (1,2)},
    (3,0): {(2,0), (2,1), (3,1)},
    (3,2): {(3,1), (2,1), (2,2)},
    (1,0): {(0,0), (0,1)},
    (1,1): {(0,0), (0,1), (0,2)},
    (1,2): {(0,1), (0,2)},
    (2,0): {(3,0)},
    (2,1): {(3,0), (3,2)},
    (3,1): {(3,0), (3,2)},
    (2,2): {(3,2)}
  }
  P_dict = {
    (0,0): 1,
    (0,1): 1,
    (0,2): 1,
    (3,0): 1,
    (3,2): 1
  }
  segment = {(3,0), (3,2)}
  solutions = backtrack(hidden, segment, graph, P_dict)
  expected_solutions = [
    {(2, 0): 0, (3, 1): 0, (2, 1): 1, (2, 2): 0}, 
    {(2, 0): 0, (3, 1): 1, (2, 1): 0, (2, 2): 0},
    {(2, 0): 1, (3, 1): 0, (2, 1): 0, (2, 2): 1}
  ]
  assert solutions == expected_solutions

def test_backtrack3():
  hidden = [
    [1,   "H",  "H",   1],
    ["H", "H",  "H", "H"],
    ["H", "H",  "H", "H"],
    [1,   "H",  "H",   1]
  ]
  graph= {
    (0,0): {(1,0), (1,1), (0,1)},
    (0,3): {(0,2), (1,2), (1,3)},
    (3,0): {(2,0), (2,1), (3,1)},
    (3,3): {(3,2), (2,2), (2,3)},
    (0,1): {(0,0)},
    (1,1): {(0,0)},
    (1,0): {(0,0)},
    (0,2): {(0,3)},
    (1,2): {(0,3)},
    (1,3): {(0,3)},
    (2,0): {(3,0)},
    (2,1): {(3,0)},
    (3,1): {(3,0)},
    (3,2): {(3,3)},
    (2,2): {(3,3)},
    (2,3): {(3,3)}
  }
  P_dict = {
    (0,0): 1,
    (0,3): 1,
    (3,0): 1,
    (3,3): 1
  }
  segment = {(3, 0)}
  solutions = backtrack(hidden, segment, graph, P_dict)
  expected_solutions = [
    {(2,0): 0, (2,1): 1, (3,1): 0},
    {(2,0): 0, (2,1): 0, (3,1): 1},
    {(2,0): 1, (2,1): 0, (3,1): 0},
  ]
  assert solutions == expected_solutions

  segment2 = {(0,3)}
  solutions2 = backtrack(hidden, segment2, graph, P_dict)
  expected_solutions2 = [
    {(0,2): 1, (1,2): 0, (1,3): 0},
    {(0,2): 0, (1,2): 0, (1,3): 1},
    {(0,2): 0, (1,2): 1, (1,3): 0},
  ]
  assert solutions2 == expected_solutions2

  segment3 = {(0,0)}
  solutions3 = backtrack(hidden, segment3, graph, P_dict)
  expected_solutions3 = [
    {(0,1): 0, (1,1): 1, (1,0): 0},
    {(0,1): 0, (1,1): 0, (1,0): 1},
    {(0,1): 1, (1,1): 0, (1,0): 0},
  ]
  assert solutions3 == expected_solutions3

  segment4 = {(3,3)}
  solutions4 = backtrack(hidden, segment4, graph, P_dict)
  expected_solutions4 = [
    {(2,2): 1, (2,3): 0, (3,2): 0},
    {(2,2): 0, (2,3): 1, (3,2): 0},
    {(2,2): 0, (2,3): 0, (3,2): 1},
  ]
  assert solutions4 == expected_solutions4

def test_backtrack4():
  hidden = [
    [2,   "H",  "H",   2],
    ["H", "H",  "H", "H"],
    [1  ,  2,    1,    1],
    [0,    0,    0,    1]
  ]  
  graph= {
    (0,0): {(1,0), (1,1), (0,1)},
    (0,3): {(0,2), (1,2), (1,3)},
    (2,0): {(1,0), (1,1)},
    (2,1): {(1,0), (1,1), (1,2)},
    (2,2): {(1,1), (1,2), (1,3)},
    (2,3): {(1,2), (1,3)},
    (0,2): {(0,3)},
    (1,2): {(0,3), (2,1), (2,2), (2,3)},
    (1,3): {(0,3), (2,2), (2,3)},
    (0,1): {(0,0)},
    (1,0): {(0,0), (2,0), (2,1)},
    (1,1): {(0,0), (2,0), (2,1), (2,2)}
  }
  P_dict = {
    (0,0): 2,
    (0,3): 2,
    (2,0): 1,
    (2,1): 2,
    (2,2): 1,
    (2,3): 1
  }
  segment = {(0,0), (0,3), (2,0), (2,1), (2,2), (2,3)}
  solutions = backtrack(hidden, segment, graph, P_dict)
  expected_solutions = [
    {(0, 1): 1, (0, 2): 1, (1,0): 1, (1,1): 0, (1,2): 1, (1,3): 0}
  ]
  assert solutions == expected_solutions

def test_backtrack5():
  hidden = [
    [0  ,   0,   1, "H"],
    [0  ,   0,   1, "H"],
    [1  ,   1,   2, "H"],
    ["H", "H", "H", "H"]
  ]  
  graph= {
    (0,2): {(0,3), (1,3)},
    (1,2): {(0,3), (1,3), (2,3)},
    (2,2): {(1,3), (2,3), (3,3), (3,2), (3,1)},
    (2,1): {(3,0), (3,1), (3,2)},
    (2,0): {(3,0), (3,1)},
    (0,3): {(0,2), (1,2)},
    (1,3): {(0,2), (1,2), (2,2)},
    (2,3): {(1,2), (2,2)},
    (3,3): {(2,2)},
    (3,2): {(2,2), (2,1)},
    (3,1): {(2,2), (2,1), (2,0)}, 
    (3,0): {(2,1), (2,0)}
  }
  segment = {(2,0), (2,1), (2,2), (1,2), (0,2)}
  P_dict = {
    (2,0): 1,
    (2,1): 1,
    (2,2): 2,
    (1,2): 1,
    (0,2): 1,
  }
  solutions = backtrack(hidden, segment, graph, P_dict)
  expected_solutions = [
    {(0,3): 1, (1,3): 0, (2,3): 0, (3,3): 1, (3,2): 0, (3,1): 1, (3,0): 0},
    {(0,3): 0, (1,3): 1, (2,3): 0, (3,3): 0, (3,2): 0, (3,1): 1, (3,0): 0},
    {(0,3): 0, (1,3): 1, (2,3): 0, (3,3): 1, (3,2): 0, (3,1): 0, (3,0): 1},
  ]
  assert solutions == expected_solutions

def test_getAllAdjacentHiddenCellsOfSegment():
  #hidden = [
  #  [1,     1,   1],
  #  ["H", "H", "H"],
  #  ["H", "H", "H"],
  #  [1,   "H",   1]
  #]
  #num_rows = 4
  #num_cols = 3
  graph= {
    (0,0): {(1,0), (1,1)},
    (0,1): {(1,0), (1,1), (1,2)},
    (0,2): {(1,1), (1,2)},
    (3,0): {(2,0), (2,1), (3,1)},
    (3,2): {(3,1), (2,1), (2,2)},
    (1,0): {(0,0), (0,1)},
    (1,1): {(0,0), (0,1), (0,2)},
    (1,2): {(0,1), (0,2)},
    (2,0): {(3,0)},
    (2,1): {(3,0), (3,2)},
    (3,1): {(3,0), (3,2)},
    (2,2): {(3,2)}
  }
  #expected_segments = [{(0,0), (0,1), (0,2)}, {(3,0), (3,2)}]
  segment = {(0,0), (0,1), (0,2)}
  expected_variables = {(1,0), (1,1), (1,2)}
  assert getAllAdjacentHiddenCellsOfSegment(segment, graph) == expected_variables

  segment = {(3,0), (3,2)}
  expected_variables = {(2,0), (2,1), (2,2), (3,1)}
  assert getAllAdjacentHiddenCellsOfSegment(segment, graph) == expected_variables


def test_selectUnassignedVariable():
  variables = [(0,0), (1,1), (2,2)]
  assignment = {}
  assert selectUnassignedVariable(variables, assignment) == (0,0)

  variables = [(0,0), (1,1), (2,2)]
  assignment = {(0,0): 1, (1,1): 0}
  assert selectUnassignedVariable(variables, assignment) == (2,2)

  variables = [(0,0), (1,1), (2,2)]
  assignment = {(0,0): 1}
  assert selectUnassignedVariable(variables, assignment) == (1,1)

def test_isAssignmentConsistent():
  hidden = [
    [1,     2,   3],
    [1,     1,   1],
    ["H", "H", "H"],
    ["H",   2, "F"]
  ]
  num_rows = 4
  num_cols = 3

  graph = {
    (2,0): {(1,0), (1,1), (3,1)}, 
    (2,1): {(1,0), (1,1), (1,2), (3,1)},
    (2,2): {(1,1), (1,2), (3,1)},
    (3,0): {(3,1)},
    (1,0): {(2,0), (2,1)},
    (1,1): {(2,0), (2,1), (2,2)},
    (1,2): {(2,1), (2,2)},
    (3,1): {(3,0), (2,0), (2,1), (2,2)}
  }
  segment = {(3, 1), (1, 2), (1, 0), (1, 1)}
  P_dict = {
    (1,0): 1,
    (1,1): 1,
    (1,2): 1,
    (3,1): 1
  }  

  ###### assignment: {(2,0): 1} ######
  assignment = {(2,0): 1}
  var = (2,1)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == True
  assignment = {(2,0): 1}
  var = (2,1)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False

  assignment = {(2,0): 1}
  var = (2,2)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == True
  assignment = {(2,0): 1}
  var = (2,2)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False

  assignment = {(2,0): 1}
  var = (3,0)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False
  assignment = {(2,0): 1}
  var = (3,0)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == True

  ###### assignment: {(2,0): 0} ######
  assignment = {(2,0): 0}
  var = (2,1)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False
  assignment = {(2,0): 0}
  var = (2,1)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == True

  assignment = {(2,0): 0}
  var = (2,2)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == True
  assignment = {(2,0): 0}
  var = (2,2)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == True

  assignment = {(2,0): 0}
  var = (3,0)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == True
  assignment = {(2,0): 0}
  var = (3,0)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == True


  ###### assignment: {(2,0): 0, (2,2): 1} ######
  assignment = {(2,0): 0, (2,2): 1}  
  var = (2,1)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False
  assignment = {(2,0): 0, (2,2): 1}  
  var = (2,1)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False

  assignment = {(2,0): 0, (2,2): 1}  
  var = (3,0)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == True
  assignment = {(2,0): 0, (2,2): 1}  
  var = (3,0)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False


  ###### assignment: {(2,0): 0, (2,2): 0} ######
  assignment = {(2,0): 0, (2,2): 0}  
  var = (2,1)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False
  assignment = {(2,0): 0, (2,2): 0}  
  var = (2,1)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == True

  assignment = {(2,0): 0, (2,2): 0}  
  var = (3,0)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == True
  assignment = {(2,0): 0, (2,2): 0}  
  var = (3,0)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == True


  ###### assignment: {(2,0): 0, (2,2): 0, (3,0): 0} ######
  assignment = {(2,0): 0, (2,2): 0, (3,0): 0}  
  var = (2,1)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False
  assignment = {(2,0): 0, (2,2): 0, (3,0): 0}  
  var = (2,1)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == True

  ###### assignment: {(2,0): 0, (2,2): 0, (3,0): 1} ######
  assignment = {(2,0): 0, (2,2): 0, (3,0): 1}  
  var = (2,1)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False
  assignment = {(2,0): 0, (2,2): 0, (3,0): 1}  
  var = (2,1)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False

  ###### assignment: {(2,0): 0, (2,2): 1, (3,0): 0} ######
  assignment = {(2,0): 0, (2,2): 1, (3,0): 0}  
  var = (2,1)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False
  assignment = {(2,0): 0, (2,2): 1, (3,0): 0}  
  var = (2,1)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False

  ###### assignment: {(2,0): 1, (2,2): 1, (3,0): 0} ######
  assignment = {(2,0): 1, (2,2): 0, (3,0): 0}  
  var = (2,1)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False
  assignment = {(2,0): 1, (2,2): 0, (3,0): 0}  
  var = (2,1)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False

  ###### assignment: {(2,0): 1, (2,2): 1, (3,0): 0} ######
  assignment = {(2,0): 1, (2,2): 1, (3,0): 0}  
  var = (2,1)
  value = 0
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False
  assignment = {(2,0): 1, (2,2): 1, (3,0): 0}  
  var = (2,1)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == False


def test_isAssignmentConsistent2():
  hidden = [
    [1,     2,   3],
    [1,     1,   1],
    ["H", "H", "H"],
    ["H",   2, "F"]
  ]
  num_rows = 4
  num_cols = 3

  graph = {
    (2,0): {(1,0), (1,1), (3,1)}, 
    (2,1): {(1,0), (1,1), (1,2), (3,1)},
    (2,2): {(1,1), (1,2), (3,1)},
    (3,0): {(3,1)},
    (1,0): {(2,0), (2,1)},
    (1,1): {(2,0), (2,1), (2,2)},
    (1,2): {(2,1), (2,2)},
    (3,1): {(3,0), (2,0), (2,1), (2,2)}
  }
  segment = {(3, 1), (1, 2), (1, 0), (1, 1)}
  P_dict = {
    (1,0): 1,
    (1,1): 1,
    (1,2): 1,
    (3,1): 1
  }
  assignment = {(2,0): 0, (2,2): 0}  
  var = (2,1)
  value = 1
  assert isAssignmentConsistent(var, value, assignment, segment, graph, P_dict) == True

def test_findBorder():
  hidden = [
    ["H",   2, "H"],
    [1,     1, "F"],
    ["H",   2, "H"],
    [2,   "H", "H"]
  ]
  num_rows = 4
  num_cols = 3

  border = findBorder(hidden, num_rows, num_cols)
  expected_border = {(1,0), (1,1), (1,2), (0,1), (2,1), (3,0)}
  assert expected_border == border

def test_findBorder2():
  hidden = [
    [1,     2,   3],
    [1,     1,   3],
    ["H", "H", "H"],
    ["H", "F", "F"]
  ]
  num_rows = 4
  num_cols = 3

  border = findBorder(hidden, num_rows, num_cols)
  expected_border = {(1,0), (1,1), (1,2), (3,1), (3,2)}
  assert expected_border == border

def test_findBorderHelper():
  hidden = [
    ["H", "H", "H"],
    [1,     1, "H"],
    ["F",   2, "H"],
    ["F",   2,   0]
  ]
  seen = set()
  row_index = 1
  cols_index = 0
  border = set()
  num_rows = 4
  num_cols = 3

  border, seen = findBorderHelper(hidden, seen, row_index, cols_index, num_rows, num_cols, border)
  expected_seen = {(1,0), (1,1), (2,0), (2,1), (3,0), (3,1), (3,2)}
  expected_border = {(1,0), (1,1), (2,1), (3,1), (3,2)}
  assert expected_seen == seen
  assert expected_border == border

def test_findBorderHelper2():
  hidden = [
    ["H",   2, "H"],
    [1,     1, "F"],
    ["H",   2, "H"],
    [2,   "H", "H"]
  ]
  seen = set()
  row_index = 1
  cols_index = 0
  border = set()
  num_rows = 4
  num_cols = 3

  border, seen = findBorderHelper(hidden, seen, row_index, cols_index, num_rows, num_cols, border)
  expected_seen = {(1,0), (1,1), (1,2), (0,1), (2,1)}
  expected_border = {(1,0), (1,1), (1,2), (0,1), (2,1)}
  assert expected_seen == seen
  assert expected_border == border

#makes sure flagged cells on border aren't considered in "graph"
def test_findSegments():
  hidden = [
    [1,     2,   3],
    [1,     1,   3],
    ["H", "H", "H"],
    ["H",   1, "F"]
  ]
  num_rows = 4
  num_cols = 3

  expected_graph= {
    (2,0): {(1,0), (1,1), (3,1)}, 
    (2,1): {(1,0), (1,1), (1,2), (3,1)},
    (2,2): {(1,1), (1,2), (3,1)},
    (3,0): {(3,1)},
    (1,0): {(2,0), (2,1)},
    (1,1): {(2,0), (2,1), (2,2)},
    (1,2): {(2,1), (2,2)},
    (3,1): {(3,0), (2,0), (2,1), (2,2)}
  }
  expected_segments = [{(3, 1), (1, 2), (1, 0), (1, 1)}]
  expected_P_dict = {
    (1,0): 1,
    (1,1): 1,
    (1,2): 3,
    (3,1): 0
  }

  graph, segments, P_dict = findSegments(hidden, num_rows, num_cols)

  assert segments == expected_segments
  assert graph == expected_graph
  assert P_dict == expected_P_dict

def test_findSegment2():
  hidden = [
    [1,     1,   1],
    ["H", "H", "H"],
    ["H", "H", "H"],
    [1,   "H",   1]
  ]
  num_rows = 4
  num_cols = 3

  expected_graph= {
    (0,0): {(1,0), (1,1)},
    (0,1): {(1,0), (1,1), (1,2)},
    (0,2): {(1,1), (1,2)},
    (3,0): {(2,0), (2,1), (3,1)},
    (3,2): {(3,1), (2,1), (2,2)},
    (1,0): {(0,0), (0,1)},
    (1,1): {(0,0), (0,1), (0,2)},
    (1,2): {(0,1), (0,2)},
    (2,0): {(3,0)},
    (2,1): {(3,0), (3,2)},
    (3,1): {(3,0), (3,2)},
    (2,2): {(3,2)}
  }
  expected_segments = [{(0,0), (0,1), (0,2)}, {(3,0), (3,2)}]
  expected_P_dict = {
    (0,0): 1,
    (0,1): 1,
    (0,2): 1,
    (3,0): 1,
    (3,2): 1
  }

  graph, segments, P_dict = findSegments(hidden, num_rows, num_cols)
  assert segments == expected_segments
  assert graph == expected_graph
  assert P_dict == expected_P_dict

def test_findSegment3():
  hidden = [
    [1,   "H",  "H",   1],
    ["H", "H",  "H", "H"],
    ["H", "H",  "H", "H"],
    [1,   "H",  "H",   1]
  ]
  num_rows = 4
  num_cols = 4

  expected_graph= {
    (0,0): {(1,0), (1,1), (0,1)},
    (0,3): {(0,2), (1,2), (1,3)},
    (3,0): {(2,0), (2,1), (3,1)},
    (3,3): {(3,2), (2,2), (2,3)},
    (0,1): {(0,0)},
    (1,1): {(0,0)},
    (1,0): {(0,0)},
    (0,2): {(0,3)},
    (1,2): {(0,3)},
    (1,3): {(0,3)},
    (2,0): {(3,0)},
    (2,1): {(3,0)},
    (3,1): {(3,0)},
    (3,2): {(3,3)},
    (2,2): {(3,3)},
    (2,3): {(3,3)}
  }
  expected_segments = [{(3, 0)}, {(0, 3)}, {(0, 0)}, {(3, 3)}]
  expected_P_dict = {
    (0,0): 1,
    (0,3): 1,
    (3,0): 1,
    (3,3): 1
  }

  graph, segments, P_dict = findSegments(hidden, num_rows, num_cols)
  assert segments == expected_segments
  assert graph == expected_graph
  assert P_dict == expected_P_dict

def test_findSegment4():
  hidden = [
    [2,   "H",  "H",   2],
    ["H", "H",  "H", "H"],
    [1  ,  2,    1,    1],
    [0,    0,    0,    1]
  ]  
  num_rows = 4
  num_cols = 4

  expected_graph= {
    (0,0): {(1,0), (1,1), (0,1)},
    (0,3): {(0,2), (1,2), (1,3)},
    (2,0): {(1,0), (1,1)},
    (2,1): {(1,0), (1,1), (1,2)},
    (2,2): {(1,1), (1,2), (1,3)},
    (2,3): {(1,2), (1,3)},
    (0,2): {(0,3)},
    (1,2): {(0,3), (2,1), (2,2), (2,3)},
    (1,3): {(0,3), (2,2), (2,3)},
    (0,1): {(0,0)},
    (1,0): {(0,0), (2,0), (2,1)},
    (1,1): {(0,0), (2,0), (2,1), (2,2)}
  }
  expected_segments = [{(0,0), (0,3), (2,0), (2,1), (2,2), (2,3)}]
  expected_P_dict = {
    (0,0): 2,
    (0,3): 2,
    (2,0): 1,
    (2,1): 2,
    (2,2): 1,
    (2,3): 1
  }

  graph, segments, P_dict = findSegments(hidden, num_rows, num_cols)
  assert segments == expected_segments
  assert graph == expected_graph
  assert P_dict == expected_P_dict

def test_findSegment5():
  hidden = [
    [0  ,   0,   1, "H"],
    [0  ,   0,   1, "H"],
    [1  ,   1,   2, "H"],
    ["H", "H", "H", "H"]
  ]  
  num_rows = 4
  num_cols = 4

  expected_graph= {
    (0,2): {(0,3), (1,3)},
    (1,2): {(0,3), (1,3), (2,3)},
    (2,2): {(1,3), (2,3), (3,3), (3,2), (3,1)},
    (2,1): {(3,0), (3,1), (3,2)},
    (2,0): {(3,0), (3,1)},
    (0,3): {(0,2), (1,2)},
    (1,3): {(0,2), (1,2), (2,2)},
    (2,3): {(1,2), (2,2)},
    (3,3): {(2,2)},
    (3,2): {(2,2), (2,1)},
    (3,1): {(2,2), (2,1), (2,0)}, 
    (3,0): {(2,1), (2,0)}
  }
  expected_segments = [{(2,0), (2,1), (2,2), (1,2), (0,2)}]
  expected_P_dict = {
    (2,0): 1,
    (2,1): 1,
    (2,2): 2,
    (1,2): 1,
    (0,2): 1,
  }

  graph, segments, P_dict = findSegments(hidden, num_rows, num_cols)
  assert segments == expected_segments
  assert graph == expected_graph
  assert P_dict == expected_P_dict

def test_dfs():
  graph = {
    (2,0): {(1,0), (1,1), (3,1)}, 
    (2,1): {(1,0), (1,1), (1,2), (3,1), (3,2)},
    (2,2): {(1,1), (1,2), (3,1), (3,2)},
    (3,0): {(3,1)},
    (1,0): {(2,0), (2,1)},
    (1,1): {(2,0), (2,1), (2,2)},
    (1,2): {(2,1), (2,2)},
    (3,1): {(3,0), (2,0), (2,1), (2,2)},
    (3,2): {(2,1), (2,2)}
  }
  start_vertex = (1,1)
  seen, segment = dfs(start_vertex, graph, set(), set())
  expected_segment = {(1, 2), (3, 2), (3, 0), (3, 1), (2, 1), (2, 0), (2, 2), (1, 0), (1, 1)}
  expected_seen = {(1, 2), (3, 2), (3, 0), (3, 1), (2, 1), (2, 0), (2, 2), (1, 0), (1, 1)}
  assert seen == expected_seen
  assert segment == expected_segment

def test_getProbabilityDistr1():
  solutions = [
    {(0,3): 1, (1,3): 0, (2,3): 0, (3,3): 1, (3,2): 0, (3,1): 1, (3,0): 0},
    {(0,3): 0, (1,3): 1, (2,3): 0, (3,3): 0, (3,2): 0, (3,1): 1, (3,0): 0},
    {(0,3): 0, (1,3): 1, (2,3): 0, (3,3): 1, (3,2): 0, (3,1): 0, (3,0): 1}
  ]
  probs = round_dict(getProbabilityDistr(solutions),7)
  expected_probs = round_dict({(0,3): 2/3, (1,3): 1/3, (2,3): 1.0, (3,3): 1/3, (3,2): 1.0, (3,1): 1/3, (3,0): 2/3},7)
  assert probs == expected_probs

def test_getProbabilityDistr2():
  solutions = [
    {(0, 1): 1, (0, 2): 1, (1,0): 1, (1,1): 0, (1,2): 1, (1,3): 0}
  ]
  probs = round_dict(getProbabilityDistr(solutions),7)
  expected_probs = round_dict({(0, 1): 0.0, (0, 2): 0.0, (1,0): 0.0, (1,1): 1.0, (1,2): 0.0, (1,3): 1.0},7)
  assert probs == expected_probs

def test_uncover():
  board = [
    [0, 0, 0],
    [0, 1, 1],
    [2, 3, 9],
    [9, 9, 2]
  ]
  hidden = [
    ["H", "H", "H"],
    ["H", "H", "H"],
    ["H", "H", "H"],
    ["H", "H", "H"]
  ]
  cell=[[0,0]]
  num_rows=4
  num_cols=3
  updatedHidden = [
    [0, 0, 0],
    [0, 1, 1],
    [2, 3, "H"],
    ["H", "H", "H"]
  ]
  hidden, uncovered_mine = uncover(cell, hidden, board, num_rows, num_cols)
  assert hidden == updatedHidden
  assert uncovered_mine == False


def test_findDefiniteMines():
  hidden = [
    [0, 0, 0],
    [0, 1, 1],
    [2, 3, "H"],
    ["H", "H", "H"]
  ]
  num_rows=4
  num_cols=3
  definiteMines = {(2,2), (3,0), (3,1)}
  assert set(map(tuple, findDefiniteMines(hidden, num_rows, num_cols))) == definiteMines

def test_isHiddenComplete():
  hidden = [
    ["S", "H", "S"],
    ["S", "S", "H"],
    ["S", "S", "H"],
    ["S", "S", "H"]
  ]
  num_adjacent_mines = 3
  row_index = 2
  cols_index = 1
  num_rows = 4
  num_cols = 3
  complete, hiddenSet = isHiddenComplete(num_adjacent_mines, hidden, row_index, cols_index, num_rows, num_cols)
  assert complete == True
  assert hiddenSet == {(1,2), (2,2), (3,2)}


def test_flagDefiniteMines():
  board = [
    [0, 0, 0],
    [0, 1, 1],
    [2, 3, 9],
    [9, 9, 2]
  ]
  hidden = [
    ["H", "H", "H"],
    ["H", "H", "H"],
    ["H", "H", "H"],
    ["H", "H", "H"]
  ]
  mines={(0,0), (2,1)}
  updatedHidden = [
    ["F", "H", "H"],
    ["H", "H", "H"],
    ["H", "F", "H"],
    ["H", "H", "H"]
  ]
  assert flagDefiniteMines(hidden, mines) == updatedHidden

def test_clickAdjacentCellsToUncover():
  cell = (2,1)
  board = [
    [0, 0, 0],
    [1, 1, 1],
    [2, 9, 1],
    [9, 2, 1]
  ]
  hidden = [
    ["H", "H", "H"],
    ["H",   1,   1],
    [2,   "F", "H"],
    ["H", "H", "H"]
  ]
  num_rows=4
  num_cols=3

  expected_updated_hidden = [
    [0,     0,   0],
    [1,     1,   1],
    [2,   "F",   1],
    ["H",   2,   1]
  ]

  expected_clicked = [(1,1), (2,2)]
  cells_clicked, updated_hidden = clickAdjacentCellsToUncover(cell, hidden, board, num_rows, num_cols)
  assert cells_clicked == expected_clicked
  assert expected_updated_hidden == updated_hidden

def test_clickAdjacentCellsToUncover2():
  cell = (1,2)
  board = [
    [9,2,1,1],
    [1,2,9,1],
    [0,1,1,1],
    [0,0,1,1],
    [0,0,1,9]
  ]
  hidden = [
    ["H", "H", "H", "H"],
    [1,   2,   "F", "H"],
    [0,   1,     1, "H"],
    [0,   0,     1, "H"],
    [0,   0,     1, "H"]
  ]
  num_rows=5
  num_cols=4

  expected_updated_hidden = [
    ["H", 2,     1,   1],
    [1,   2,   "F",   1],
    [0,   1,     1,   1],
    [0,   0,     1,   1],
    [0,   0,     1, "H"]
  ]

  expected_clicked = [(2,2), (1,3), (0,2)]
  cells_clicked, updated_hidden = clickAdjacentCellsToUncover(cell, hidden, board, num_rows, num_cols)
  assert cells_clicked == expected_clicked
  assert expected_updated_hidden == updated_hidden


def test_generateMoves():
  board = [[0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 9.0, 9.0, 9.0, 1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 3.0, 9.0, 4.0, 3.0, 9.0, 2.0, 2.0, 2.0, 3.0, 2.0, 1.0, 1.0, 9.0, 1.0], [1.0, 2.0, 9.0, 9.0, 9.0, 9.0, 5.0, 9.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0], [9.0, 2.0, 2.0, 5.0, 9.0, 9.0, 4.0, 9.0, 4.0, 2.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0], [1.0, 1.0, 0.0, 2.0, 9.0, 4.0, 3.0, 4.0, 9.0, 9.0, 3.0, 3.0, 3.0, 9.0, 1.0, 0.0], [0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 9.0, 3.0, 9.0, 4.0, 9.0, 9.0, 9.0, 2.0, 1.0, 0.0], [2.0, 3.0, 3.0, 9.0, 1.0, 2.0, 2.0, 4.0, 2.0, 3.0, 3.0, 9.0, 4.0, 3.0, 2.0, 1.0], [9.0, 9.0, 9.0, 2.0, 1.0, 1.0, 9.0, 2.0, 9.0, 2.0, 2.0, 2.0, 2.0, 9.0, 9.0, 2.0], [4.0, 9.0, 4.0, 1.0, 0.0, 2.0, 2.0, 3.0, 1.0, 3.0, 9.0, 2.0, 1.0, 2.0, 3.0, 9.0], [2.0, 9.0, 3.0, 1.0, 1.0, 1.0, 9.0, 1.0, 0.0, 2.0, 9.0, 2.0, 0.0, 0.0, 1.0, 1.0], [3.0, 3.0, 4.0, 9.0, 2.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0], [9.0, 9.0, 4.0, 9.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0], [3.0, 4.0, 9.0, 2.0, 2.0, 1.0, 1.0, 0.0, 0.0, 1.0, 3.0, 9.0, 3.0, 1.0, 0.0, 0.0], [1.0, 9.0, 2.0, 1.0, 1.0, 9.0, 1.0, 0.0, 0.0, 1.0, 9.0, 9.0, 9.0, 1.0, 0.0, 0.0], [1.0, 1.0, 2.0, 1.0, 3.0, 2.0, 3.0, 1.0, 1.0, 1.0, 2.0, 3.0, 2.0, 1.0, 0.0, 0.0], [0.0, 1.0, 2.0, 9.0, 2.0, 9.0, 4.0, 9.0, 3.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0], [1.0, 2.0, 9.0, 3.0, 3.0, 4.0, 9.0, 9.0, 9.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 9.0], [2.0, 9.0, 4.0, 3.0, 9.0, 3.0, 9.0, 5.0, 4.0, 3.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0], [2.0, 9.0, 9.0, 2.0, 1.0, 2.0, 3.0, 9.0, 3.0, 9.0, 9.0, 2.0, 1.0, 9.0, 1.0, 0.0], [1.0, 2.0, 2.0, 2.0, 1.0, 1.0, 2.0, 9.0, 3.0, 3.0, 9.0, 2.0, 1.0, 1.0, 1.0, 0.0], [0.0, 0.0, 0.0, 2.0, 9.0, 3.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 2.0, 9.0, 4.0, 9.0, 2.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 1.0, 1.0], [0.0, 0.0, 0.0, 1.0, 1.0, 3.0, 9.0, 2.0, 0.0, 0.0, 0.0, 1.0, 9.0, 2.0, 9.0, 1.0], [2.0, 2.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 3.0, 2.0, 2.0], [9.0, 9.0, 1.0, 1.0, 2.0, 3.0, 2.0, 1.0, 2.0, 9.0, 2.0, 1.0, 1.0, 2.0, 9.0, 1.0], [2.0, 3.0, 2.0, 2.0, 9.0, 9.0, 9.0, 2.0, 4.0, 9.0, 5.0, 3.0, 9.0, 2.0, 1.0, 1.0], [1.0, 2.0, 9.0, 2.0, 4.0, 9.0, 4.0, 3.0, 9.0, 9.0, 9.0, 9.0, 2.0, 1.0, 0.0, 0.0], [9.0, 3.0, 2.0, 1.0, 2.0, 9.0, 3.0, 3.0, 9.0, 4.0, 3.0, 2.0, 1.0, 0.0, 0.0, 0.0], [3.0, 9.0, 2.0, 1.0, 2.0, 2.0, 9.0, 3.0, 2.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0], [9.0, 2.0, 2.0, 9.0, 1.0, 1.0, 2.0, 9.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 9.0, 1.0]]
  board = [list(map(int, lst)) for lst in board]
  num_rows = 30
  num_cols = 16
  num_mines = 99
  hidden = [["H" for i in range(num_cols)] for j in range(num_rows)]
  generateMoves(board, hidden, num_rows, num_cols, num_mines)


def test_generateMoves2():
  board = [[0.0, 0.0, 1.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 2.0, 9.0, 3.0, 9.0, 2.0, 9.0, 2.0, 9.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [9.0, 1.0, 2.0, 9.0, 3.0, 2.0, 3.0, 2.0, 2.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 9.0, 2.0, 1.0, 1.0, 1.0, 2.0, 3.0, 9.0, 2.0, 1.0], [1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 2.0, 9.0, 2.0, 2.0, 9.0, 9.0, 3.0, 9.0, 1.0], [1.0, 9.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 9.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0], [1.0, 1.0, 2.0, 9.0, 1.0, 1.0, 9.0, 2.0, 3.0, 4.0, 3.0, 1.0, 0.0, 0.0, 0.0, 0.0], [0.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 2.0, 9.0, 9.0, 9.0, 1.0, 0.0, 0.0, 1.0, 1.0], [1.0, 2.0, 9.0, 2.0, 2.0, 2.0, 3.0, 3.0, 4.0, 9.0, 3.0, 1.0, 0.0, 0.0, 1.0, 9.0], [2.0, 9.0, 3.0, 9.0, 3.0, 9.0, 9.0, 9.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [9.0, 2.0, 2.0, 2.0, 4.0, 9.0, 5.0, 4.0, 4.0, 2.0, 1.0, 1.0, 9.0, 1.0, 0.0, 0.0], [2.0, 2.0, 0.0, 1.0, 9.0, 2.0, 2.0, 9.0, 9.0, 9.0, 2.0, 1.0, 1.0, 1.0, 0.0, 0.0], [9.0, 1.0, 1.0, 3.0, 3.0, 2.0, 1.0, 3.0, 9.0, 9.0, 3.0, 1.0, 0.0, 0.0, 0.0, 0.0], [3.0, 3.0, 2.0, 9.0, 9.0, 1.0, 0.0, 1.0, 2.0, 3.0, 9.0, 2.0, 2.0, 1.0, 1.0, 0.0], [9.0, 9.0, 3.0, 3.0, 2.0, 1.0, 0.0, 0.0, 0.0, 1.0, 2.0, 9.0, 2.0, 9.0, 2.0, 1.0], [2.0, 3.0, 9.0, 2.0, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 9.0, 2.0], [1.0, 2.0, 4.0, 9.0, 4.0, 9.0, 3.0, 9.0, 1.0, 1.0, 9.0, 1.0, 1.0, 3.0, 9.0, 2.0], [2.0, 9.0, 3.0, 9.0, 9.0, 3.0, 9.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 9.0, 3.0, 1.0], [9.0, 3.0, 3.0, 2.0, 2.0, 3.0, 2.0, 2.0, 1.0, 9.0, 2.0, 2.0, 9.0, 9.0, 2.0, 0.0], [2.0, 9.0, 2.0, 1.0, 0.0, 1.0, 9.0, 1.0, 1.0, 1.0, 3.0, 9.0, 5.0, 4.0, 4.0, 2.0], [1.0, 2.0, 9.0, 2.0, 1.0, 2.0, 2.0, 3.0, 2.0, 2.0, 4.0, 9.0, 5.0, 9.0, 9.0, 9.0], [0.0, 1.0, 1.0, 3.0, 9.0, 2.0, 1.0, 9.0, 9.0, 2.0, 9.0, 9.0, 5.0, 9.0, 4.0, 2.0], [0.0, 1.0, 2.0, 4.0, 9.0, 2.0, 2.0, 3.0, 3.0, 2.0, 3.0, 9.0, 3.0, 1.0, 1.0, 0.0], [1.0, 2.0, 9.0, 9.0, 4.0, 3.0, 2.0, 9.0, 1.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0], [1.0, 9.0, 4.0, 9.0, 9.0, 3.0, 9.0, 2.0, 2.0, 1.0, 1.0, 2.0, 9.0, 3.0, 9.0, 9.0], [1.0, 1.0, 2.0, 3.0, 4.0, 9.0, 2.0, 2.0, 2.0, 9.0, 3.0, 4.0, 9.0, 3.0, 2.0, 2.0], [0.0, 0.0, 0.0, 2.0, 9.0, 3.0, 2.0, 2.0, 9.0, 3.0, 9.0, 9.0, 2.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 4.0, 9.0, 3.0, 1.0, 9.0, 2.0, 2.0, 2.0, 2.0, 1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 9.0, 9.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 2.0, 2.0, 1.0, 1.0, 9.0, 1.0, 1.0, 9.0, 1.0, 0.0, 0.0, 0.0, 0.0]]
  board = [list(map(int, lst)) for lst in board]
  num_rows = 30
  num_cols = 16
  num_mines = 99
  moves = [[28, 0], [[28, 4], [27, 4], [26, 4], [28, 3]], [26, 3], [28, 2], [29, 3], [29, 4], [28, 5], [27, 5]]
  hidden = [["H" for i in range(num_cols)] for j in range(num_rows)]
  generateMoves(board, hidden, num_rows, num_cols, num_mines)

def test_generateMoves3():
  board = [[9., 2., 2., 1., 2., 1., 2., 9., 1., 0., 0., 0., 1., 9., 2., 1.],
       [2., 9., 3., 9., 3., 9., 2., 1., 1., 0., 0., 0., 1., 2., 9., 2.],
       [1., 1., 4., 9., 4., 2., 2., 1., 1., 1., 1., 0., 0., 2., 3., 9.],
       [0., 1., 3., 9., 3., 2., 9., 2., 2., 9., 1., 0., 1., 3., 9., 4.],
       [0., 1., 9., 4., 9., 2., 3., 9., 3., 1., 1., 1., 2., 9., 9., 9.],
       [1., 2., 3., 9., 2., 1., 3., 9., 3., 0., 0., 1., 9., 3., 3., 2.],
       [1., 9., 2., 2., 2., 1., 2., 9., 3., 1., 1., 1., 1., 1., 0., 0.],
       [1., 1., 2., 2., 9., 2., 2., 1., 2., 9., 2., 1., 1., 1., 1., 1.],
       [0., 1., 2., 9., 3., 9., 1., 0., 1., 2., 3., 9., 1., 1., 9., 1.],
       [0., 1., 9., 2., 2., 1., 1., 1., 2., 4., 9., 4., 3., 3., 2., 1.],
       [0., 2., 2., 2., 0., 0., 0., 2., 9., 9., 9., 5., 9., 9., 2., 0.],
       [0., 1., 9., 1., 0., 0., 0., 2., 9., 4., 3., 9., 9., 9., 4., 1.],
       [0., 1., 1., 2., 1., 1., 0., 1., 2., 3., 3., 3., 4., 9., 3., 9.],
       [0., 0., 1., 2., 9., 1., 0., 0., 1., 9., 9., 1., 1., 1., 3., 2.],
       [1., 1., 2., 9., 3., 1., 0., 0., 1., 3., 3., 2., 0., 0., 1., 9.],
       [9., 1., 3., 9., 3., 1., 1., 2., 1., 2., 9., 2., 1., 1., 1., 1.],
       [1., 2., 3., 9., 2., 1., 9., 2., 9., 3., 2., 2., 9., 2., 1., 1.],
       [0., 1., 9., 2., 1., 1., 1., 2., 2., 9., 2., 2., 2., 4., 9., 3.],
       [1., 2., 3., 3., 2., 1., 0., 0., 1., 2., 9., 1., 1., 9., 9., 9.],
       [2., 9., 2., 9., 9., 1., 0., 1., 2., 4., 3., 2., 2., 5., 9., 5.],
       [9., 2., 2., 2., 3., 3., 2., 2., 9., 9., 9., 2., 2., 9., 9., 9.],
       [1., 2., 1., 1., 2., 9., 9., 2., 3., 9., 4., 9., 2., 2., 4., 9.],
       [0., 2., 9., 2., 2., 9., 3., 1., 1., 1., 2., 1., 1., 1., 2., 2.],
       [1., 3., 9., 2., 1., 1., 1., 0., 0., 0., 0., 0., 0., 1., 9., 1.],
       [9., 3., 2., 3., 1., 1., 0., 1., 1., 1., 0., 1., 1., 2., 1., 1.],
       [2., 3., 9., 2., 9., 1., 1., 2., 9., 1., 0., 1., 9., 1., 0., 0.],
       [1., 9., 2., 2., 1., 1., 2., 9., 3., 1., 1., 3., 3., 2., 0., 0.],
       [3., 4., 3., 1., 0., 0., 2., 9., 2., 0., 1., 9., 9., 1., 0., 0.],
       [9., 9., 9., 2., 0., 0., 1., 1., 2., 1., 2., 2., 2., 1., 1., 1.],
       [2., 4., 9., 2., 0., 0., 0., 0., 1., 9., 1., 0., 0., 0., 1., 9.]]
  board = [list(map(int, lst)) for lst in board]
  num_rows = 30
  num_cols = 16
  num_mines = 99
  hidden = [["H" for i in range(num_cols)] for j in range(num_rows)]
  generateMoves(board, hidden, num_rows, num_cols, num_mines)

def test_generateMoves4():
  board = [[9.0, 4.0, 9.0, 9.0, 9.0, 1.0, 1.0, 3.0, 9.0, 9.0, 2.0, 2.0, 3.0, 9.0, 9.0, 9.0], [9.0, 6.0, 9.0, 7.0, 4.0, 2.0, 1.0, 9.0, 9.0, 3.0, 2.0, 9.0, 9.0, 4.0, 4.0, 3.0], [3.0, 9.0, 9.0, 9.0, 9.0, 2.0, 2.0, 2.0, 3.0, 2.0, 3.0, 3.0, 3.0, 2.0, 9.0, 1.0], [2.0, 9.0, 4.0, 3.0, 3.0, 9.0, 1.0, 0.0, 1.0, 9.0, 2.0, 9.0, 1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 2.0, 1.0, 2.0, 1.0, 1.0, 0.0, 1.0, 1.0, 3.0, 2.0, 2.0, 0.0, 1.0, 1.0], [1.0, 2.0, 3.0, 9.0, 2.0, 2.0, 1.0, 1.0, 0.0, 1.0, 2.0, 9.0, 1.0, 0.0, 1.0, 9.0], [1.0, 9.0, 9.0, 3.0, 9.0, 2.0, 9.0, 1.0, 0.0, 1.0, 9.0, 2.0, 2.0, 1.0, 2.0, 1.0], [2.0, 3.0, 2.0, 2.0, 1.0, 2.0, 1.0, 1.0, 0.0, 1.0, 1.0, 2.0, 2.0, 9.0, 1.0, 0.0], [9.0, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 9.0, 2.0, 1.0, 0.0], [1.0, 2.0, 9.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 9.0, 3.0, 2.0, 2.0, 1.0, 1.0], [0.0, 1.0, 2.0, 9.0, 1.0, 1.0, 9.0, 9.0, 2.0, 2.0, 3.0, 9.0, 2.0, 3.0, 9.0, 2.0], [1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 4.0, 3.0, 3.0, 9.0, 2.0, 2.0, 3.0, 9.0, 9.0, 2.0], [9.0, 2.0, 1.0, 0.0, 1.0, 9.0, 2.0, 9.0, 2.0, 1.0, 1.0, 1.0, 9.0, 3.0, 2.0, 1.0], [2.0, 9.0, 1.0, 0.0, 1.0, 1.0, 2.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0], [2.0, 2.0, 2.0, 0.0, 0.0, 1.0, 2.0, 2.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0], [2.0, 9.0, 2.0, 0.0, 0.0, 1.0, 9.0, 9.0, 2.0, 0.0, 1.0, 1.0, 3.0, 9.0, 2.0, 0.0], [3.0, 9.0, 4.0, 2.0, 1.0, 2.0, 3.0, 9.0, 2.0, 0.0, 2.0, 9.0, 4.0, 9.0, 2.0, 0.0], [2.0, 9.0, 9.0, 3.0, 9.0, 2.0, 1.0, 1.0, 1.0, 1.0, 3.0, 9.0, 3.0, 1.0, 1.0, 0.0], [2.0, 3.0, 4.0, 4.0, 9.0, 2.0, 1.0, 2.0, 2.0, 3.0, 9.0, 3.0, 1.0, 0.0, 1.0, 1.0], [1.0, 9.0, 3.0, 9.0, 2.0, 1.0, 2.0, 9.0, 9.0, 4.0, 9.0, 3.0, 1.0, 2.0, 3.0, 9.0], [1.0, 2.0, 9.0, 2.0, 1.0, 0.0, 2.0, 9.0, 4.0, 5.0, 9.0, 4.0, 2.0, 9.0, 9.0, 2.0], [0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 2.0, 9.0, 9.0, 4.0, 9.0, 4.0, 4.0, 3.0], [1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 3.0, 9.0, 4.0, 2.0, 3.0, 9.0, 9.0], [1.0, 9.0, 2.0, 1.0, 1.0, 1.0, 9.0, 1.0, 0.0, 1.0, 1.0, 2.0, 9.0, 2.0, 3.0, 9.0], [2.0, 2.0, 3.0, 9.0, 2.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0], [9.0, 1.0, 2.0, 9.0, 2.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [2.0, 2.0, 3.0, 2.0, 2.0, 0.0, 1.0, 9.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [1.0, 9.0, 3.0, 9.0, 2.0, 2.0, 3.0, 2.0, 2.0, 9.0, 1.0, 1.0, 9.0, 1.0, 1.0, 9.0], [1.0, 2.0, 9.0, 2.0, 2.0, 9.0, 9.0, 2.0, 2.0, 1.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0], [0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 9.0, 1.0, 0.0, 1.0, 9.0, 1.0, 0.0, 0.0, 0.0]] 
  board = [list(map(int, lst)) for lst in board]
  num_rows = 30
  num_cols = 16
  num_mines = 99
  hidden = [["H" for i in range(num_cols)] for j in range(num_rows)]
  generateMoves(board, hidden, num_rows, num_cols, num_mines)


