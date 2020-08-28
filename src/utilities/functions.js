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
      if (minesSet.has([col_index, row_index].toString())) return -1; 
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

module.exports = { 
  generateMines: generateMines, 
  generateNumbersArr: generateNumbersArr,
  convertFrom1Dto2D: convertFrom1Dto2D
} 