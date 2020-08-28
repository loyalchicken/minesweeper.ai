import React from "react";
import { bindActionCreators } from "redux";
import { connect } from "react-redux";
import { newGame } from "../../actions/actions";

export class BoardHeader extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  handleOnClick = e => {
    this.props.newGame();
  }

  render() {
    return (
      <div>
        <button 
          onClick={this.handleOnClick}
        >
          New Game
        </button>
      </div>
    );
  }
}

const matchDispatchToProps = dispatch =>
  bindActionCreators(
    {
      newGame
    },
    dispatch
  );

export default connect(
  null, matchDispatchToProps
)(BoardHeader);
  