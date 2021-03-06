import React, { Component } from "react";
import styled from "styled-components";
import ListSubheader from "@material-ui/core/ListSubheader";
import List from "@material-ui/core/List";
import Exporter from "./Exporter";
import { get } from "./api";
import Dialog from "./Dialog";
import LoadingDialog from "./LoadingDialog";

const INTERVAL = 3000;
let refreshInterval = null;

export default class Exporters extends Component {
  constructor(props) {
    super(props);
    this.state = { exporters: null, error: null };
  }

  render() {
    const { exporters, error } = this.state;
    if (exporters !== null) {
      this.maybeTriggerUpdates();
      return (
        <Container className="Exporters">
          {error && this.renderWarningDialog()}
          <List
            component="nav"
            subheader={<ListSubheader component="div">Exporter</ListSubheader>}
          >
            {Object.keys(exporters).map(exporterId => (
              <Exporter
                key={exporterId}
                runExporter={() => this.runExporter(exporterId)}
                id={exporterId}
                {...exporters[exporterId]}
              />
            ))}
          </List>
        </Container>
      );
    } else {
      this.getExporters();
      return <LoadingDialog text="Lade Daten..." />;
    }
  }

  renderWarningDialog() {
    const { error } = this.state;
    const messages = {
      RELOADING:
        "Der Server wird gerade aktualisiert. Bitte später neu laden und erneut versuchen.",
      RUNNING: "Der Exporter wird bereits ausgeführt",
      SCHEDULED: "Der Exporter wurde bereits zur Warteschlange hinzugefügt"
    };
    const message = `${messages[error]}. Sie können den Exporter erneut starten, wenn der aktuelle Durchlauf beendet ist.`;
    const actions = [
      {
        name: "Schließen",
        onClick: () => {
          this.setState({ error: null });
        }
      }
    ];
    return (
      <Dialog title="Exporter läuft bereits" actions={actions}>
        {message}
      </Dialog>
    );
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
    }).then(response => {
      if (response.error) {
        this.setState({ error: response.code, exporters: response.exporters });
      } else {
        this.setState({ exporters: response });
      }
    });
  }
}

const Container = styled.div`
  margin: 24px;
`;
