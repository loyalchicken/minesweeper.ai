/**
 * Generates a list of numbers corresponding to the 1D coordinates of the squares that are mines  
 * O(n) time, where n = rows*cols 
 * @param numMines (number of mines)
 * @param rows (number of rows)
 * @param cols (number of cols)
 * @return a list of numbers
 **/
const generateMines = (numMines,rows, cols) => {
  const arr = Array.from(Array(rows*cols).keys());
  for (var i = rows*cols-1; i >= 0; i--) {
    const randNum = Math.floor(Math.random() * i); //generate random index between 0 and i
    swap(arr, i, randNum);
  }
  return arr.slice(0, numMines);
}

const swap = (arr, index1, index2) => {
  var temp = arr[index1];
  arr[index1]=arr[index2];
  arr[index2]=temp;
}

/**
 * Generates a 2D array of numbers, where the value of each index is the number of mines a square is adjacent to
 * @param mines: list of numbers corresponding to the 1D coordinates of the squares that are mines
 * @return 2D array of numbers (col, row)
 **/
const generateNumbersArr = (mines, rows, cols) => {
  const minesIn2D = mines.map(mine => {
    const coords = convertFrom1Dto2D(mine, cols)
    return [coords[0], coords[1]].toString();
  })

  var minesSet = new Set(minesIn2D);

  //initialize a 2D array
  const newArr = new Array(rows).fill(0).map(() => new Array(cols).fill(0));

  //populate the number of neighboring mines for each cell appropriately
  //cells that are mines are set to -1
  return newArr.map((row, row_index) => {
    return row.map((_, col_index) => {
      if (minesSet.has([col_index, row_index].toString())) return 9; 
      return numNeighbors(minesSet, col_index, row_index, cols, rows);
    })
  })
}

/**
 * Finds the number of neighbors of current cell that are mines
 * @param minesSet: set (of 2D coords) of mines
 * @param x: col_index of current cell
 * @param y: row_index of current cell
 * @return number of neighbors that are mines
 **/
const numNeighbors = (minesSet, x, y, cols, rows) => {
  var mines = 0;
  for (var i = Math.max(0, x-1); i <= Math.min(cols-1, x+1); i++) {
    for (var j = Math.max(0, y-1); j <= Math.min(rows-1, y+1); j++) {
      if (minesSet.has([i, j].toString())) mines+=1;
    }
  }
  return mines;
}

/**
 * Converts 1D coordinate to 2D coordinate (cols, row)
 * @param mine: a number 
 * @param cols: number of columns
 * @return 2D coordinate  
 **/
const convertFrom1Dto2D = (mines, cols) => {
  const y = Math.floor(mines/cols);
  const x = mines % cols;
  return [x,y];
}

/**
 * Unhides the surrounding "0" cells of the current cell (row_index, cols_index)
 * @param hidden: a 2D boolean array [index by row, then column] 
 * @param mines: 2D integer array [index by row, then column]
 * @param row_index: current cell row index
 * @param cols_index: current cell column index
 * @param rows (number of rows)
 * @param cols (number of columns)
 * @return set of 2D indices that need to be hidden   
 **/
const unhideSurroundingSquaresWithZero = (hidden, mines, row_index, cols_index, rows, cols) => {
  let setOfHiddenIndices = new Set();
  let setOfSeenIndices = new Set();
  unhideSurroundingSquaresWithZeroHelper(hidden, mines, row_index, cols_index, rows, cols, setOfHiddenIndices, setOfSeenIndices);
  return setOfHiddenIndices;
}

const unhideSurroundingSquaresWithZeroHelper = (hidden, mines, row_index, cols_index, rows, cols, setOfHiddenIndices, setOfSeenIndices) => {
  setOfSeenIndices.add([row_index, cols_index].toString());
  for (var i = Math.max(0, row_index-1); i <= Math.min(rows-1, row_index+1); i++) {
    for (var j = Math.max(0, cols_index-1); j <= Math.min(cols-1, cols_index+1); j++) {
      setOfHiddenIndices.add([i,j].toString());
      if (mines[i][j]===0 && !setOfSeenIndices.has([i,j].toString())) {
        unhideSurroundingSquaresWithZeroHelper(hidden, mines, i, j, rows, cols, setOfHiddenIndices, setOfSeenIndices);
      }
    }
  }
}

/**
 * Checks whether the number of adjacent cells flagged equals the number of the cell's neighboring mines
 * @param numMines: the number of adjacent cells which are mines
 * @param visible: 2D integer array of current status of cells [index by row, then column]
 * @param row_index: current cell row index
 * @param cols_index: current cell column index
 * @param rows (number of rows)
 * @param cols (number of columns)
 * @return boolean   
 **/
const isFlaggedComplete = (numMines, visible, row_index, cols_index, rows, cols) => {
  var numFlagged = 0;
  for (var i = Math.max(0, row_index-1); i <= Math.min(rows-1, row_index+1); i++) {
    for (var j = Math.max(0, cols_index-1); j <= Math.min(cols-1, cols_index+1); j++) {
      if (visible[i][j]==="flag") {
        numFlagged+=1;
      }
    }
  }
  return numFlagged === numMines;
}

/**
 * Unhides all neighboring cells that aren't flagged, including all "0" patches if a neighboring cell has "0" 
 * @param mines: 2D integer array [index by row, then column]
 * @param visible: 2D integer array of current status of cells [index by row, then column]
 * @param row_index: current cell row index
 * @param cols_index: current cell column index
 * @param rows (number of rows)
 * @param cols (number of columns)
 * @return set of 2D indices that need to be hidden   
 **/
const unhideAllSurroundingSquares = (visible, mines, row_index, cols_index, rows, cols) => {
  let setOfHiddenIndices = new Set();
  for (var i = Math.max(0, row_index-1); i <= Math.min(rows-1, row_index+1); i++) {
    for (var j = Math.max(0, cols_index-1); j <= Math.min(cols-1, cols_index+1); j++) {
      if (visible[i][j]==="hidden") setOfHiddenIndices.add([i,j].toString());
      if (mines[i][j]===0) {
        let patchZeroSet = unhideSurroundingSquaresWithZero(visible, mines, i, j, rows, cols);
        patchZeroSet.forEach(setOfHiddenIndices.add, setOfHiddenIndices);
      }
    }
  }
  return setOfHiddenIndices;
}


module.exports = { 
  generateMines: generateMines, 
  generateNumbersArr: generateNumbersArr,
  convertFrom1Dto2D: convertFrom1Dto2D,
  unhideSurroundingSquaresWithZero: unhideSurroundingSquaresWithZero,
  isFlaggedComplete: isFlaggedComplete,
  unhideAllSurroundingSquares: unhideAllSurroundingSquares
} 