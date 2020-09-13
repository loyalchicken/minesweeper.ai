import React from "react";
import { bindActionCreators } from "redux";
import { connect } from "react-redux";
import { newGame, changeMode, solve, displayMoves } from "../../actions/actions";

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

  handleGenerate = e => {
    this.props.solve(this.props.numRows, this.props.numColumns, this.props.numMines);
  }

  handleSolve = e => {
    this.props.displayMoves(this.props.moves)
  }

  render() {
    return (
      <div>
        {
          this.props.numFlagsRemaining
        }
        <br />
        <br />
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
          onClick={this.handleGenerate}
        >
          Generate
        </button>
        {this.props.moves && (
          <button
            onClick={this.handleSolve}
          >
            Solve 
          </button>
        )}

      </div>
    );
  }
}

const mapStateToProps = state => ({
  moves: state.moves,
  mines: state.mines,
  numRows: state.numRows,
  numColumns: state.numColumns,
  numMines: state.numMines,
  segments: state.segments,
  numFlagsRemaining: state.numFlagsRemaining
});

const matchDispatchToProps = dispatch =>
  bindActionCreators(
    {
      newGame,
      changeMode,
      solve,
      displayMoves
    },
    dispatch
  );

export default connect(
  mapStateToProps, matchDispatchToProps
)(BoardHeader);
  