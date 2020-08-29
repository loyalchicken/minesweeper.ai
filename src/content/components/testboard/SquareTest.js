import React from "react";
import {numberToColorMap} from "../../../utilities/data";
import mineImg from '../../../images/mine.png';
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { showSquare } from "../../actions/actions";

export class SquareTest extends React.Component {
  constructor(props) {
    super(props);
    this.state = {

    };
  }

  handleClickSquare = e => {
    if (this.props.visible.length === 1) return;
    this.props.showSquare(this.props.row, this.props.column);
  }

  handleRightClickSquare = e => {
    if (this.props.visible.length === 1) return;
  }

  display = (number, visibleState) => {
    switch (visibleState) {
      case "hidden":
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
          return null;
        default:
          return null;
    }
  }

  show = () => {
    if (this.props.visible.length === 1) return false;
    return true;
  }

  render() {
    const squareStyle = this.show() ? "squareHide" : "squareShow"; 
    return (
      <button 
        className={squareStyle}
        onClick={this.handleClickSquare}
        onContextMenu={this.handleRightClickSquare}
      >
        {this.show() && (
          this.display(this.props.mines[this.props.row][this.props.column], "show")
        )}
      </button>
    );
  }
}

const matchDispatchToProps = dispatch =>
  bindActionCreators(
    {
      showSquare
    },
    dispatch
  );

const mapStateToProps = state => ({
  mines: state.mines,
  visible: state.visible
});

export default connect(
  mapStateToProps,
  matchDispatchToProps
)(SquareTest);