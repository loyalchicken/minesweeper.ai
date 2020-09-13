import numpy as np
import random

def probabilityRandomCellIsNotMine(hidden, hidden_cells_region1, num_mines, probability_map):
  """Calculates the probability that a hidden cell not adjacent to shown cells is not a mine
    REGION 1: HIDDEN CELLS ADJACENT TO SHOWN CELLS 
    REGION 2: HIDDEN CELLS NOT ADJACENT TO SHOWN CELLS

  Parameters
  ----------
  hidden                   a 2D character array of visible state of cells [index by row, then column] 
  hidden_cells_region1     a set of cells that are adjacent to the shown cells
  num_mines                number of mines
  probability_map          a dictionary mapping all hidden cells (adjacent to currently shown cells) to probability of it not being a mine

  Returns
  -------
  A number between 0-1
  """
  all_hidden_cells = np.asarray(np.where(np.array(hidden)=="H")).T
  all_hidden_cells = set([tuple(cell) for cell in all_hidden_cells])
  hidden_cells_region2 = all_hidden_cells - hidden_cells_region1 
  print("printing guess probabilities")
  print(len(hidden_cells_region2))
  num_flagged = numFlagged(hidden) 

  expected_number_of_mines_region1 = expectedNumberOfMinesAdjacentToShownCells(probability_map)
  expected_number_of_mines_region2 = num_mines - expected_number_of_mines_region1 - num_flagged

  if len(hidden_cells_region2) == 0:
    return 0
  #print("printing")
  #print(expected_number_of_mines_region2)
  #print(len(hidden_cells_region2))
  return 1 - (expected_number_of_mines_region2 / len(hidden_cells_region2))

def numFlagged(hidden):
  return len(np.asarray(np.where(np.array(hidden)=="F")).T)

def expectedNumberOfMinesAdjacentToShownCells(probability_map):
  """Calculates expected number of mines adjacent to currently shown cells
  
  Parameters
  ----------
  probability_map      a dictionary mapping hidden cells all (adjacent to currently shown cells) to probability of it not being a mine

  Returns
  -------
  A number (expected value)
  """
  if len(probability_map) == 0:
    return 0
  return len(probability_map) - sum(probability_map.values())


def findRandomHiddenCell(hidden, hidden_cells_adjacent_to_segments):
  """Chooses a random cell from a hidden cell not adjacent to the currently shown cells

  Parameters
  ----------
  hidden                                a 2D character array of visible state of cells [index by row, then column] 
  hidden_cells_adjacent_to_segments     a set of cells that are adjacent to the shown cells

  Returns
  -------
  A cell (tuple)
  """

  all_hidden_cells = np.asarray(np.where(np.array(hidden)=="H")).T
  all_hidden_cells = set([tuple(cell) for cell in all_hidden_cells])
  hidden_cells_of_relevance = all_hidden_cells - hidden_cells_adjacent_to_segments 
  cell = random.choice(list(hidden_cells_of_relevance))
  return (int(cell[0]), int(cell[1]))