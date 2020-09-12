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

def round_dict(d, n):
  """Round all values in dictionary d to n decimal places
  """
  new_dict = dict()
  for key in d:
    new_dict[key]=round(d[key], n)
  return new_dict

def merge_two_dicts(x, y):
  z = x.copy()   # start with x's keys and values
  z.update(y)    # modifies z with y's keys and values & returns None
  return z

def win(hidden, num_rows, num_cols, num_mines):
  hidden = np.array(hidden)
  num_flagged = (hidden=="F").sum()
  num_hidden = (hidden=="H").sum()
  total_cells = num_rows*num_cols
  return num_flagged+num_hidden == num_mines
