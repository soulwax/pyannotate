// File: tests/sample_web_files/legacy/legacy-component.js
// Author: Legacy Developer
// Created: 2022-01-01
// Version: 1.0.0

class LegacyComponent {
  constructor(props) {
    this.props = props;
    this.state = {
      count: 0
    };
  }
  
  incrementCount() {
    this.state.count++;
    console.log(`Count is now ${this.state.count}`);
  }
  
  render() {
    return `<div class="legacy-component">
      <h2>${this.props.title}</h2>
      <p>Count: ${this.state.count}</p>
      <button onClick="this.incrementCount()">Increment</button>
    </div>`;
  }
}

export default LegacyComponent;
