import React, { Component } from "react";
import styled from "styled-components";
import Exporter from "./Exporter";
import { get } from "./api";

export default class Exporters extends Component {
  constructor(props) {
    super(props);
    this.state = { exporters: null };
  }

  render() {
    const { exporters } = this.state;
    if (exporters !== null) {
      return (
        <Container className="Exporters">
          {Object.keys(exporters).map(exporterId => (
            <Exporter
              key={exporterId}
              runExporter={() => this.runExporter(exporterId)}
              {...exporters[exporterId]}
            />
          ))}
        </Container>
      );
    } else {
      get("/exporters").then(exporters => this.setState({ exporters }));
      return null;
    }
  }

  runExporter(exporterId) {
    const { manufacturers } = this.props;
    get("/run", { exporter: exporterId, manufacturers }).then(exporters =>
      this.setState({ exporters })
    );
  }
}

const Container = styled.div`
  margin: 10px;
`;
