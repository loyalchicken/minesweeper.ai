import React from "react";
import BoardHeader from "./BoardHeader";
import Grid from "./Grid";

export default class Board extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      numRows: 30,
      numColumns: 16
    };
  }
  render() {
    return (
      <div className="board">
        <BoardHeader></BoardHeader>
        <Grid 
          numRows = {this.state.numRows} 
          numColumns = {this.state.numColumns}
        />
      </div>
    );
  }
}