import React, { Component }  from 'react';


import { Button } from 'reactstrap';

class TeamFilter extends React.Component {
  // This syntax ensures `this` is bound within handleClick.
  // Warning: this is *experimental* syntax.
  handleClick = () => {
    console.log('this is:', this);

    if (this.button == "All") {
      
    }

  }

  render() {
    return (
      <button onClick={this.handleClick}>
        Click me
      </button>

    );
  }
}