import {
  NEW_GAME,
  SHOW_SQUARE,
  FLAG_SQUARE,
  CHANGE_MODE,
  GENERATE_GAME,
  TESTING
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

export const testing = () => dispatch => {
  console.log("hin  ");
  axios
    .get('/solver/')
    .then(response => {
      console.log(response);
      dispatch({
        type: TESTING,
        h: response.data.response_text
      })
    })
}


