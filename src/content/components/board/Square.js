import React from "react";
import {numberToColorMap} from "../../../utilities/data";
import mineImg from '../../../images/mine.png';
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { showSquare } from "../../actions/actions";

export class Square extends React.Component {
  constructor(props) {
    super(props);
    this.state = {

    };
  }

  handleClickSquare = e => {
    if (this.props.hidden.length === 1) return;
    this.props.showSquare(this.props.row, this.props.column);
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
    if (this.props.hidden.length === 1) return false;
    return !this.props.hidden[this.props.row][this.props.column];
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

const matchDispatchToProps = dispatch =>
  bindActionCreators(
    {
      showSquare
    },
    dispatch
  );

const mapStateToProps = state => ({
  mines: state.mines,
  hidden: state.hidden
});

export default connect(
  mapStateToProps,
  matchDispatchToProps
)(Square);