import React from "react";
import Row from "./Row";

export default class Grid extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }
  render() {
    const rows = Array.from(Array(this.props.numRows).keys());
    return (
      <div>
        {rows.map((row, index)=> 
          <div className="row" key={index} >
            <Row 
              row={index} 
              numColumns={this.props.numColumns}
            /> 
          </div>
        )}
      </div>
    );
  }
}