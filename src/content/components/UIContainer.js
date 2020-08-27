import React from "react";
import Board from "./board/Board";
import Menu from "./Menu";

export default class UIContainer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }
  render() {
    return (
      <div>
        <Board></Board>
        <Menu></Menu>
      </div>
    );
  }
}