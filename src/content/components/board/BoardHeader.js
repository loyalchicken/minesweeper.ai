import React from "react";
import { bindActionCreators } from "redux";
import { connect } from "react-redux";
import { newGame, changeMode } from "../../actions/actions";

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
      </div>
    );
  }
}

const matchDispatchToProps = dispatch =>
  bindActionCreators(
    {
      newGame,
      changeMode
    },
    dispatch
  );

export default connect(
  null, matchDispatchToProps
)(BoardHeader);
  