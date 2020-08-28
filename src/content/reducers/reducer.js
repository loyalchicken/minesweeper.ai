import {
  NEW_GAME,
  SHOW_SQUARE
} from "../actions/actionTypes";

import {generateMines, generateNumbersArr, unhideSurroundingSquares} from "../../utilities/functions";

const initialState = {
  mines: [[]],
  hidden: [[]],
  numRows: 30,
  numColumns: 16,
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
      var newHidden = JSON.parse(JSON.stringify(state.hidden));
      newHidden[action.row][action.cols]=false;
      const number = state.mines[action.row][action.cols];
      if (number===0) {
        const indexSet = unhideSurroundingSquares(newHidden, state.mines, action.row, action.cols, state.numRows, state.numColumns);
        for (let item of indexSet) {
          const coords = item.split(",").map(x=>+x);
          newHidden[coords[0]][coords[1]]=false;
        }
      }
      console.log(newHidden);
      return {
        ...state,
        hidden: newHidden
      }
    default:
      return state;
  }
}