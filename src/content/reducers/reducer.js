import {
  NEW_GAME,
  SHOW_SQUARE
} from "../actions/actionTypes";

import {generateMines, generateNumbersArr} from "../../utilities/functions";

const initialState = {
  mines: [[]],
  hidden: [[]],
  numRows: 16,
  numColumns: 30,
  numMines: 99
};

export default function reducer(state = initialState, action) {
  switch (action.type) {
    case NEW_GAME:
      const newMines = generateMines(state.numMines, state.numRows, state.numColumns);
      const numbersArr = generateNumbersArr(newMines, state.numRows, state.numColumns);
      return {
        ...state,
        mines: numbersArr,
        hidden: new Array(state.numRows).fill(true).map(() => Array(state.numColumns).fill(true))
      }
    case SHOW_SQUARE:
      var newHidden = state.hidden;
      newHidden[action.row][action.cols]=false;
      return {
        ...state,
        hidden: newHidden
      }
    default:
      return state;
  }
}