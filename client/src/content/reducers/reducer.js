import {
  NEW_GAME,
  SHOW_SQUARE,
  FLAG_SQUARE,
  CHANGE_MODE,
  GENERATE_GAME,
  SOLVE
} from "../actions/actionTypes";

import {generateMines, generateNumbersArr, unhideSurroundingSquaresWithZero, isFlaggedComplete, unhideAllSurroundingSquares} from "../../utilities/functions";

const initialState = {
  mines: [[]],
  visible: [[]],
  activeGame: false,
  firstClick: false,
  numRows: 30,
  numColumns: 16,
  numMines: 99,
  gameMode: "normal",
  hello: false
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
        visible: new Array(state.numRows).fill("hidden").map(() => Array(state.numColumns).fill("hidden")),
        gameMode: "normal",
        activeGame: true,
        firstClick: false
      }
    //on first click
    case GENERATE_GAME:
      let number = state.mines[action.row][action.cols];
      let newMines2 = state.mines;
      while (number !== 0) {
        const newMines = generateMines(state.numMines, state.numRows, state.numColumns);
        newMines2 = generateNumbersArr(newMines, state.numRows, state.numColumns);
        number =  newMines2[action.row][action.cols]
      }
      //unhide the "0" patch
      const indexSet2 = unhideSurroundingSquaresWithZero(newVisible, newMines2, action.row, action.cols, state.numRows, state.numColumns);
      for (let item of indexSet2) {
        const coords = item.split(",").map(x=>+x);
        newVisible[coords[0]][coords[1]]="show";
      }
      return {
        ...state,
        firstClick: true,
        visible: newVisible,
        mines: newMines2
      }
  
    case SHOW_SQUARE:
      const currVisibleState = newVisible[action.row][action.cols];

      //if hit a hidden mine, display all mines and set activeGame to false
      if (state.mines[action.row][action.cols]===9 && currVisibleState !== "flag") {
        newVisible[action.row][action.cols]="show";
        return {
          ...state,
          activeGame: false,
          visible: newVisible
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

            //lose game if an incorrect cell was flagged
            if (currMines[coords[0]][coords[1]]===9) {
              newVisible[coords[0]][coords[1]]="show";
              return {
                ...state,
                activeGame: false,
                visible: newVisible
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
    case CHANGE_MODE:
      return {
        ...state,
        gameMode: state.gameMode === "normal" ? "flagging" : "normal"
      }
    case SOLVE:
      return {
        ...state,
        hello: action.h
      }
    default:
      return state;
  }
}