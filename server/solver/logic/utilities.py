import numpy as np 

def adjacent_cells_of(cell, num_rows, num_cols):
  cells = []
  row_index = cell[0]
  cols_index = cell[1]
  for i in np.arange(max(0, row_index-1), min(num_rows-1, row_index+1)+1):
    for j in np.arange(max(0, cols_index-1), min(num_cols-1, cols_index+1)+1):
      if (i,j) != (row_index, cols_index):
        cells.append((int(i),int(j)))
  return cells

def connected_cells_of(cell, num_rows, num_cols):
  cells = []
  row_index = cell[0]
  cols_index = cell[1]
  if row_index-1>=0:
    cells.append((row_index-1, cols_index))
  if cols_index-1>=0:
    cells.append((row_index, cols_index-1))
  if cols_index<num_cols-1:
    cells.append((row_index, cols_index+1))
  if row_index<num_rows-1:
    cells.append((row_index+1, cols_index))
  return cells
