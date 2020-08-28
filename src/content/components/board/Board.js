import React from "react";
import BoardHeader from "./BoardHeader";
import Grid from "./Grid";
import GridTest from "../testboard/GridTest";
import { connect } from "react-redux";

export class Board extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="board">
        <BoardHeader numColumns = {this.props.numColumns}/>
        <br/>
        <div className="inline">
          <Grid 
            numRows = {this.props.numRows} 
            numColumns = {this.props.numColumns}
          />
          <div className="divider"></div>
          <GridTest 
            numRows = {this.props.numRows} 
            numColumns = {this.props.numColumns}
          />
        </div>
      </div>
    );
  }
}

const mapStateToProps = state => ({
  numRows: state.numRows,
  numColumns: state.numColumns
});

export default connect(
  mapStateToProps
)(Board);
