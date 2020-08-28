import React from "react";
import BoardHeader from "./BoardHeader";
import Grid from "./Grid";
import { connect } from "react-redux";

export class Board extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="board">
        <BoardHeader numColumns = {this.props.numColumns}/>
        <Grid 
          numRows = {this.props.numRows} 
          numColumns = {this.props.numColumns}
          mines = {this.props.mines}
        />
      </div>
    );
  }
}

const mapStateToProps = state => ({
  numRows: state.numRows,
  numColumns: state.numColumns,
  mines: state.mines
});

export default connect(
  mapStateToProps
)(Board);
