from solver.logic.utilities import adjacent_cells_of, connected_cells_of
import numpy as np

def test_adjacent_cells_of():
  cells = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
  num_rows = 3
  num_cols = 3
  assert adjacent_cells_of(cells[0], num_rows, num_cols) == [(0, 1), (1, 0), (1, 1)]
  assert adjacent_cells_of(cells[1], num_rows, num_cols) == [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)]
  assert adjacent_cells_of(cells[2], num_rows, num_cols) == [(0,1), (1,1), (1,2)]
  assert adjacent_cells_of(cells[3], num_rows, num_cols) == [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)]
  assert adjacent_cells_of(cells[4], num_rows, num_cols) == [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)]
  assert adjacent_cells_of(cells[5], num_rows, num_cols) == [(0, 1), (0, 2), (1, 1), (2, 1), (2, 2)]
  assert adjacent_cells_of(cells[6], num_rows, num_cols) == [(1,0), (1,1), (2,1)]
  assert adjacent_cells_of(cells[7], num_rows, num_cols) == [(1, 0), (1, 1), (1, 2), (2, 0), (2, 2)]
  assert adjacent_cells_of(cells[8], num_rows, num_cols) == [(1, 1), (1, 2), (2, 1)]

def test_connected_cells_of():
  cells = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
  num_rows = 3
  num_cols = 3
  assert connected_cells_of(cells[0], num_rows, num_cols) == [(0, 1), (1, 0)]
  assert connected_cells_of(cells[1], num_rows, num_cols) == [(0, 0), (0, 2), (1, 1)]
  assert connected_cells_of(cells[2], num_rows, num_cols) == [(0,1), (1,2)]
  assert connected_cells_of(cells[3], num_rows, num_cols) == [(0, 0), (1, 1), (2, 0)]
  assert connected_cells_of(cells[4], num_rows, num_cols) == [(0,1), (1,0), (1,2), (2,1)]
  assert connected_cells_of(cells[5], num_rows, num_cols) == [(0, 2), (1, 1), (2, 2)]
  assert connected_cells_of(cells[6], num_rows, num_cols) == [(1,0), (2,1)]
  assert connected_cells_of(cells[7], num_rows, num_cols) == [(1, 1), (2, 0), (2, 2)]
  assert connected_cells_of(cells[8], num_rows, num_cols) == [(1, 2), (2, 1)]
