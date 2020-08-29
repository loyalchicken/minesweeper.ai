const utilitiesFunctions = require('../../src/utilities/functions');

test('generateMines returns a set of distinct numbers', () => {
  const numMines = 5;
  const rows = 5;
  const cols = 1;
  const minesArr = utilitiesFunctions.generateMines(numMines, rows, cols);
  expect((new Set(minesArr)).size).toEqual(minesArr.length);
});

test('generateMines returns a set of distinct numbers', () => {
  const numMines = 480;
  const rows = 30;
  const cols = 16;
  const minesArr = utilitiesFunctions.generateMines(numMines, rows, cols);
  expect((new Set(minesArr)).size).toEqual(minesArr.length);
});

test('convertFrom1Dto2D', () => {
  const mine = 7;
  const cols = 4;
  const coords = utilitiesFunctions.convertFrom1Dto2D(mine, cols);
  expect(coords[0]).toEqual(3);
  expect(coords[1]).toEqual(1);
});

test('convertFrom1Dto2D', () => {
  const mine = 3;
  const cols = 4;
  const coords = utilitiesFunctions.convertFrom1Dto2D(mine, cols);
  expect(coords[0]).toEqual(3);
  expect(coords[1]).toEqual(0);
});

test('convertFrom1Dto2D', () => {
  const mine = 0;
  const cols = 4;
  const coords = utilitiesFunctions.convertFrom1Dto2D(mine, cols);
  expect(coords[0]).toEqual(0);
  expect(coords[1]).toEqual(0);
});

test('convertFrom1Dto2D', () => {
  const mine = 8;
  const cols = 4;
  const coords = utilitiesFunctions.convertFrom1Dto2D(mine, cols);
  expect(coords[0]).toEqual(0);
  expect(coords[1]).toEqual(2);
});

test('generateNumbersArr is correct', () => {
  const mines = [0,3, 7,8];
  const rows = 4;
  const cols = 5;
  const numbersArr = utilitiesFunctions.generateNumbersArr(mines, rows, cols);
  const expected = [
    [ 9, 2, 3, 9, 2 ],
    [ 1, 2, 9, 9, 2 ],
    [ 0, 1, 2, 2, 1 ],
    [ 0, 0, 0, 0, 0 ]
  ];
  expect(numbersArr).toEqual(expected);
});

test('unhideSurroundingSquares unhides correct squares', () => {
  const hidden = [
    [true, true, true],
    [true, true, true],
    [true, true, true],
    [true, true, true]
  ];
  const mines = [
    [0, 0, 0],
    [0, 1, 1],
    [2, 3, 9],
    [9, 9, 2]
  ];
  const row_index = 0;
  const cols_index = 0;
  const rows = 4;
  const cols = 3;
  const setIndices = utilitiesFunctions.unhideSurroundingSquaresWithZero(hidden, mines, row_index, cols_index, rows, cols);
  const arr = ['0,0', '0,1', '0,2', '1,1', '1,2', '1,0', '2,0', '2,1'];
  let expected = new Set(arr)
  expect(setIndices).toEqual(expected);
});

test('isFlaggedComplete checks number of flagged neighbors correctly', () => {
  const visible = [
    ["flag", "hidden", "show"],
    ["hidden", "flag", "hidden"],
    ["flag", "show", "hidden"],
    ["show", "flag", "hidden"]
  ];
  const row_index = 2;
  const cols_index = 1;
  const rows = 4;
  const cols = 3;
  const isComplete = utilitiesFunctions.isFlaggedComplete(3, visible, row_index, cols_index, rows, cols);
  let expected = true;
  expect(isComplete).toEqual(expected);
});

test('unhideAllSurroundingSquares barebones is correct', () => {
  const visible = [
    ["flag", "hidden", "show"],
    ["hidden", "flag", "hidden"],
    ["flag", "show", "hidden"],
    ["show", "flag", "hidden"]
  ];
  const mines = [
    [1, 1, 1],
    [2, 9, 1],
    [9, 3, 2],
    [2, 9, 1]
  ];
  const row_index = 2;
  const cols_index = 1;
  const rows = 4;
  const cols = 3;
  const setIndices = utilitiesFunctions.unhideAllSurroundingSquares(visible, mines, row_index, cols_index, rows, cols);
})

test('unhideAllSurroundingSquares with invoking helper function to unhide "0" patches is correct', () => {
  const visible = [
    ["hidden", "hidden", "hidden"],
    ["hidden", "hidden", "hidden"],
    ["flag", "show", "show"],
    ["show", "flag", "show"]
  ];
  const mines = [
    [0, 0, 0],
    [1, 1, 0],
    [9, 2, 1],
    [2, 9, 1]
  ];
  const row_index = 2;
  const cols_index = 2;
  const rows = 4;
  const cols = 3;
  const setIndices = utilitiesFunctions.unhideAllSurroundingSquares(visible, mines, row_index, cols_index, rows, cols);
  console.log(setIndices);
})