import numpy as np 

def adjacent_cells_of(cell, num_rows, num_cols):
  cells = set()
  row_index = cell[0]
  cols_index = cell[1]
  for i in np.arange(max(0, row_index-1), min(num_rows-1, row_index+1)+1):
    for j in np.arange(max(0, cols_index-1), min(num_cols-1, cols_index+1)+1):
      if (i,j) != (row_index, cols_index):
        cells.add((int(i),int(j)))
  return cells

