import React from 'react';
import './styles/App.css';
import UIContainer from './content/components/UIContainer'

class App extends React.Component {
  render() {
    return (
      <div className="app" >
        <UIContainer> </UIContainer>
      </div>
    )
  }
}

export default App;
