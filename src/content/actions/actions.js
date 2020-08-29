import {
  NEW_GAME,
  SHOW_SQUARE,
  FLAG_SQUARE
} from "./actionTypes";

export function newGame() {
  return {
    type: NEW_GAME,
  }
}

export function showSquare(row, cols) {
  return {
    type: SHOW_SQUARE,
    row: row,
    cols: cols
  }
}

export function flagSquare(row, cols) {
  return {
    type: FLAG_SQUARE,
    row: row,
    cols: cols
  }
}