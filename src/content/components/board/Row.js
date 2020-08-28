import React from "react";
import Square from "./Square";

export default class Row extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const elementsInRow = Array.from(Array(this.props.numColumns).keys());
    return (
      elementsInRow.map((element, index) => 
        <Square 
          column={index} 
          row={this.props.row}
          elementsInRow={elementsInRow} 
          index={index}
          mines={this.props.mines}
        /> 
      )
    );
  }
}