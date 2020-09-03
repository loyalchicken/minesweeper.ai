import {
  NEW_GAME,
  SHOW_SQUARE,
  FLAG_SQUARE,
  CHANGE_MODE,
  GENERATE_GAME,
  SOLVE
} from "./actionTypes";
import axios from "axios";

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

export function changeMode() {
  return {
    type: CHANGE_MODE,
  }
}

export function generateGame(row, cols) {
  return {
    type: GENERATE_GAME,
    row: row,
    cols: cols
  }
}

export const solve = (num_rows, num_cols, num_mines) => dispatch => {
  var qs = require('qs')
  axios
    .get('solver/?' + qs.stringify({'num_rows': num_rows, 'num_cols': num_cols, 'num_mines': num_mines}))
    .then(response => {
      dispatch({
        type: SOLVE,
        h: response.data.response_text
      })
    })
}


