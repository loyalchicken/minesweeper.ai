import React from "react";
import {numberToColorMap} from "../../../utilities/data";
import mineImg from '../../../images/mine.png';
export default class Square extends React.Component {
  constructor(props) {
    super(props);
    this.state = {

    };
  }

  handleClickSquare = e => {
    console.log(this.props.row);
    console.log(this.props.column);
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

  render() {
    return (
      <button 
        className="square" 
        onClick={this.handleClickSquare}
      >
        {this.props.mines.length > 1 && (
          this.display(this.props.mines[this.props.row][this.props.column])
        )}
      </button>
    );
  }
}