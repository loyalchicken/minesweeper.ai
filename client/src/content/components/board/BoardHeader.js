import React from "react";
import { bindActionCreators } from "redux";
import { connect } from "react-redux";
import { newGame, changeMode, testing } from "../../actions/actions";

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

  handleTest = e => {
    this.props.testing();
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
          onClick={this.handleTest}
        >
          Test
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
  hello: state.hello
});

const matchDispatchToProps = dispatch =>
  bindActionCreators(
    {
      newGame,
      changeMode,
      testing
    },
    dispatch
  );

export default connect(
  mapStateToProps, matchDispatchToProps
)(BoardHeader);
  