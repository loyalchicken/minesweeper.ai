from solver.logic.probability_helpers import expectedNumberOfMinesAdjacentToShownCells, probabilityRandomCellIsNotMine, numFlagged

def test_expectedNumberOfMinesAdjacentToShownCells():
  probability_map = {(6, 9): 0.7, (4, 6): 0.5, (6, 8): 0.2, (5, 6): 0.1}
  zero_probability_map = {}
  assert expectedNumberOfMinesAdjacentToShownCells(probability_map) == 2.5
  assert expectedNumberOfMinesAdjacentToShownCells(zero_probability_map) == 0

  
#def test_probabilityRandomCellIsNotMine():

def test_numFlagged():
  hidden = [["F", "F", 2, 2, "F"], ["F", 2, 2, 2, 3], ["F", 1, 2, 3, 4]]
  assert numFlagged(hidden) == 5