import {
  NEW_GAME,
  SHOW_SQUARE,
  FLAG_SQUARE
} from "../actions/actionTypes";

import {generateMines, generateNumbersArr, unhideSurroundingSquaresWithZero, isFlaggedComplete, unhideAllSurroundingSquares} from "../../utilities/functions";

const initialState = {
  mines: [[]],
  visible: [[]],
  numRows: 30,
  numColumns: 16,
  numMines: 99
};

export default function reducer(state = initialState, action) {
  var newVisible = JSON.parse(JSON.stringify(state.visible));

  switch (action.type) {
    case NEW_GAME:
      const newMines = generateMines(state.numMines, state.numRows, state.numColumns);
      const numbersArr = generateNumbersArr(newMines, state.numRows, state.numColumns);
      return {
        ...state,
        mines: numbersArr,
        visible: new Array(state.numRows).fill("hidden").map(() => Array(state.numColumns).fill("hidden"))
      }
    case SHOW_SQUARE:
      const currVisibleState = newVisible[action.row][action.cols];

      //if hit mine, restart
      if (state.mines[action.row][action.cols]===9) {
        const newMines = generateMines(state.numMines, state.numRows, state.numColumns);
        const numbersArr = generateNumbersArr(newMines, state.numRows, state.numColumns);
        return {
          ...state,
          mines: numbersArr,
          visible: new Array(state.numRows).fill("hidden").map(() => Array(state.numColumns).fill("hidden"))
        }  
      }
      
      //unhide current square
      if (currVisibleState === "hidden") {
        newVisible[action.row][action.cols]="show";
        const number = state.mines[action.row][action.cols];
        //unhide all connecting squares with zero 
        if (number===0) {
          const indexSet = unhideSurroundingSquaresWithZero(newVisible, state.mines, action.row, action.cols, state.numRows, state.numColumns);
          for (let item of indexSet) {
            const coords = item.split(",").map(x=>+x);
            newVisible[coords[0]][coords[1]]="show";
          }
        }  
      }

      //shortcut to unhide adjacent squares in flag mode
      if (currVisibleState === "show") {
        var currMines = JSON.parse(JSON.stringify(state.mines));
        const currNumber = currMines[action.row][action.cols];
        if(isFlaggedComplete(currNumber, newVisible, action.row, action.cols, state.numRows, state.numColumns)) {
          const indexSet = unhideAllSurroundingSquares(newVisible, state.mines, action.row, action.cols, state.numRows, state.numColumns);
          for (let item of indexSet) {
            const coords = item.split(",").map(x=>+x);

            //lose game if you flag incorrect cell
            if (currMines[coords[0]][coords[1]]===9) {
              const newMines = generateMines(state.numMines, state.numRows, state.numColumns);
              const numbersArr = generateNumbersArr(newMines, state.numRows, state.numColumns);
              return {
                ...state,
                mines: numbersArr,
                visible: new Array(state.numRows).fill("hidden").map(() => Array(state.numColumns).fill("hidden"))
              }
            }
            newVisible[coords[0]][coords[1]]="show";
          }
        }
      }
      return {
        ...state,
        visible: newVisible
      }
    case FLAG_SQUARE:
      const currVisibleState2 = newVisible[action.row][action.cols];
      if (currVisibleState2 === "show") newVisible[action.row][action.cols]="show";
      if (currVisibleState2 === "hidden") newVisible[action.row][action.cols]="flag";
      if (currVisibleState2 === "flag") newVisible[action.row][action.cols]="hidden";
      return {
        ...state,
        visible: newVisible
      }
    default:
      return state;
  }
}