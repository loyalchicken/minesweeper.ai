from solver.logic.probability_helpers import expectedNumberOfMinesAdjacentToShownCells

def test_expectedNumberOfMinesAdjacentToShownCells():
  probability_map = {(6, 9): 0.7, (4, 6): 0.5, (6, 8): 0.2, (5, 6): 0.1}
  zero_probability_map = {}
  assert expectedNumberOfMinesAdjacentToShownCells(probability_map) == 1.5
  assert expectedNumberOfMinesAdjacentToShownCells(zero_probability_map) == 0

  