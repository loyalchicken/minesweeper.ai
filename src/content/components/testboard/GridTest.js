import React from "react";
import RowTest from "./RowTest";

export default class GridTest extends React.Component {
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
            <RowTest
              row={index} 
              numColumns={this.props.numColumns}
            /> 
          </div>
        )}
      </div>
    );
  }
}