import React from "react";
import SquareTest from "./SquareTest";

export default class RowTest extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const elementsInRow = Array.from(Array(this.props.numColumns).keys());
    return (
      elementsInRow.map((element, index) => 
        <SquareTest 
          column={index} 
          row={this.props.row}
        /> 
      )
    );
  }
}