import React from "react";
import {numberToColorMap} from "../../../utilities/data";
import mineImg from '../../../images/mine.png';
import { connect } from "react-redux";

export class SquareTest extends React.Component {
  constructor(props) {
    super(props);
    this.state = {

    };
  }

  display = number => {
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
  }

  show = () => {
    if (this.props.mines.length === 1) return false;
    return true;
  }

  render() {
    return (
      <button 
        className="square" 
        onClick={this.handleClickSquare}
      >
        {this.show() && (
          this.display(this.props.mines[this.props.row][this.props.column])
        )}
      </button>
    );
  }
} 

const mapStateToProps = state => ({
  mines: state.mines
});

export default connect(
  mapStateToProps
)(SquareTest);