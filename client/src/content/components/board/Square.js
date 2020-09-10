import React from "react";
import {numberToColorMap} from "../../../utilities/data";
import mineImg from '../../../images/mine.png';
import flagImg from '../../../images/flag.png';
import flaggingModeFlagImg from '../../../images/final_quick_flag_mode.png';

import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { showSquare, flagSquare, generateGame } from "../../actions/actions";

export class Square extends React.Component {
  constructor(props) {
    super(props);
    this.state = {

    };
  }

  handleClickSquare = e => {
    if (!this.props.activeGame) return;
    if (!this.props.firstClick) {
      this.props.generateGame(this.props.row, this.props.column);
    };
    if (this.props.gameMode==="flagging") {
      if (this.props.visible[this.props.row][this.props.column] === "show") {
        this.props.showSquare(this.props.row, this.props.column);
      } else {
        this.props.flagSquare(this.props.row, this.props.column);
      }
    } else {
      this.props.showSquare(this.props.row, this.props.column);
    }
  }

  handleRightClickSquare = e => {
    if (!this.props.activeGame) return;
    this.props.flagSquare(this.props.row, this.props.column);
  }

  display = (number, visibleState) => {
    switch (visibleState) {
      case "hidden":
        if (this.props.gameMode==="flagging") {
          return <img src={flaggingModeFlagImg} alt="greyFlag" width="14" height="14"/>;
        }
        return null;
      case "show":
        switch (number) {
          case 0: //no neighboring mines
            return null;
          case 9: //mine 
            return <img src={mineImg} alt="mine" width="14" height="14"/>;
          default: //not a mine, but has >0 neighboring mines
            return (
              <div style={{color: `${numberToColorMap[number]}`}}>
                {number}
              </div>   
            )
          }
      case "flag":
        return <img src={flagImg} alt="flag" width="14" height="14"/>;        
      default:
        return null;
    }
  }

  initialized = () => {
    return this.props.visible.length > 1;
  }

  render() {
    const hidden = !this.initialized() || (this.initialized() && this.props.visible[this.props.row][this.props.column] !== "show");
    const squareStyle = hidden ? "squareHide" : "squareShow";
    return (
      <button 
        className={squareStyle}
        onClick={this.handleClickSquare}
        onContextMenu={this.handleRightClickSquare}
      >
        {this.initialized() && (
          this.display(this.props.mines[this.props.row][this.props.column], this.props.visible[this.props.row][this.props.column])
        )}
      </button>
    );
  }
}

const matchDispatchToProps = dispatch =>
  bindActionCreators(
    {
      showSquare,
      flagSquare,
      generateGame
    },
    dispatch
  );

const mapStateToProps = state => ({
  mines: state.mines,
  visible: state.visible,
  gameMode: state.gameMode,
  activeGame: state.activeGame,
  firstClick: state.firstClick,
  segments: state.segments
});

export default connect(
  mapStateToProps,
  matchDispatchToProps
)(Square);