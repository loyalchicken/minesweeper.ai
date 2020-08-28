import {
  NEW_GAME
} from "../actions/actionTypes";

import {generateMines, generateNumbersArr} from "../../utilities/functions";

const initialState = {
  mines: [[]],
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
        mines: numbersArr
      };
    default:
      return state;
  }
}