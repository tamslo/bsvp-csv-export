import React, { Component } from "react";
import styled from "styled-components";
import ListSubheader from "@material-ui/core/ListSubheader";
import List from "@material-ui/core/List";
import Exporter from "./Exporter";
import { get } from "./api";

const INTERVAL = 3000;
let refreshInterval = null;

export default class Exporters extends Component {
  constructor(props) {
    super(props);
    this.state = { exporters: null };
  }

  render() {
    const { exporters } = this.state;
    if (exporters !== null) {
      this.maybeTriggerUpdates();
      return (
        <Container className="Exporters">
          <List
            component="nav"
            subheader={<ListSubheader component="div">Exporter</ListSubheader>}
          >
            {Object.keys(exporters).map(exporterId => (
              <Exporter
                key={exporterId}
                runExporter={() => this.runExporter(exporterId)}
                {...exporters[exporterId]}
              />
            ))}
          </List>
        </Container>
      );
    } else {
      this.getExporters();
      return null;
    }
  }

  maybeTriggerUpdates() {
    const { exporters } = this.state;
    const scheduledAndRunning = [
      ...Object.keys(exporters).map(
        exporterId => exporters[exporterId].scheduled
      ),
      ...Object.keys(exporters).map(exporterId => exporters[exporterId].running)
    ];
    const needsUpdates = scheduledAndRunning.some(scheduled => scheduled);
    if (needsUpdates && refreshInterval === null) {
      refreshInterval = setInterval(() => {
        this.getExporters();
      }, INTERVAL);
    } else if (!needsUpdates && refreshInterval !== null) {
      clearInterval(refreshInterval);
      refreshInterval = null;
    }
  }

  getExporters() {
    get("/exporters").then(exporters => this.setState({ exporters }));
  }

  runExporter(exporterId) {
    const { manufacturers } = this.props;
    const manufacturersParameter = Object.keys(manufacturers).reduce(
      (selectedManufacturers, manufacturer) =>
        manufacturers[manufacturer]
          ? [...selectedManufacturers, manufacturer]
          : selectedManufacturers,
      []
    );
    get("/run", {
      exporter: exporterId,
      manufacturers: manufacturersParameter
    }).then(exporters => this.setState({ exporters }));
  }
}

const Container = styled.div`
  margin: 24px;
`;
