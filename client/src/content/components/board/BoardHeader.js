import React from "react";
import { bindActionCreators } from "redux";
import { connect } from "react-redux";
import { newGame, changeMode, solve } from "../../actions/actions";

export class BoardHeader extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  handleNewGame = e => {
    this.props.newGame();
  }

  handleChangeMode = e => {
    this.props.changeMode();
  }

  handleSolve = e => {
    this.props.solve(this.props.numRows, this.props.numColumns, this.props.numMines);
  }


  render() {
    return (
      <div>
        <button 
          onClick={this.handleNewGame}
        >
          New Game
        </button>
        <button 
          onClick={this.handleChangeMode}
        >
          Mode
        </button>
        <button 
          onClick={this.handleSolve}
        >
          Solve
        </button>
        {this.props.hello && (
          <button>
            Works 
          </button>
        )}
      </div>
    );
  }
}

const mapStateToProps = state => ({
  hello: state.hello,
  mines: state.mines,
  numRows: state.numRows,
  numColumns: state.numColumns,
  numMines: state.numMines 
});

const matchDispatchToProps = dispatch =>
  bindActionCreators(
    {
      newGame,
      changeMode,
      solve
    },
    dispatch
  );

export default connect(
  mapStateToProps, matchDispatchToProps
)(BoardHeader);
  