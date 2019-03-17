import React, { Component } from "react";
import { createGlobalStyle } from "styled-components";
import Header from "./Header";
import Exporters from "./Exporters";
import Settings from "./Settings";
import { get } from "./api";

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = { manufacturers: null, showSettings: false };
  }

  componentDidMount() {
    get("/manufacturers").then(manufacturers =>
      this.setState({
        manufacturers: manufacturers.map(manufacturer => ({
          name: manufacturer,
          selected: true
        }))
      })
    );
  }

  render() {
    const { showSettings, manufacturers } = this.state;
    return (
      <div className="App">
        <GlobalStyle />
        <Header showSettings={this.toggleSettings.bind(this)} />
        <Exporters />
        {manufacturers && (
          <Settings
            open={showSettings}
            close={this.toggleSettings.bind(this)}
            manufacturers={manufacturers}
          />
        )}
      </div>
    );
  }

  toggleSettings() {
    const { showSettings } = this.state;
    this.setState({ showSettings: !showSettings });
  }
}

const GlobalStyle = createGlobalStyle`
  @font-face {
    font-family: "Roboto";
    src: url(./fonts/Roboto.ttf) format("truetype");
  }

  body {
    margin: 0;
    padding: 0;
    color: #141414;
    background-color: #fafafa;
    font-family: "Roboto", "Helvetica Neue", sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  code {
    font-family: source-code-pro, Menlo, Monaco, Consolas, "Courier New",
      monospace;
  }
`;
