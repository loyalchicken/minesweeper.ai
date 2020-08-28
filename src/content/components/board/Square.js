import React from "react";

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

  render() {
    return (
      <button 
        className="square" 
        onClick={this.handleClickSquare}
      >
        {this.props.mines.length > 1 && (
          this.props.mines[this.props.row][this.props.column]
        )}
      </button>
    );
  }
}