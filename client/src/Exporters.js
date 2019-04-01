import React, { Component } from "react";
import styled from "styled-components";
import Grid from "@material-ui/core/Grid";
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
          <Grid container spacing={24}>
            {Object.keys(exporters).map(exporterId => (
              <Grid key={exporterId} item xs={12} sm={12}>
                <Exporter
                  runExporter={() => this.runExporter(exporterId)}
                  {...exporters[exporterId]}
                />
              </Grid>
            ))}
          </Grid>
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
