import React, { Component } from "react";
import styled from "styled-components";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import IconButton from "@material-ui/core/IconButton";
import SettingsIcon from "@material-ui/icons/SettingsOutlined";
import RefreshIcon from "@material-ui/icons/Refresh";
import Dialog from "./Dialog";
import LoadingDialog from "./LoadingDialog";
import { get } from "./api";

export default class extends Component {
  constructor(props) {
    super(props);
    this.state = { reloading: false, reloaded: null };
  }

  render() {
    const { showSettings } = this.props;
    const { reloading, reloaded } = this.state;
    return (
      <AppBar position="static" color="primary">
        {reloading && this.renderLoadingDialog()}
        {reloaded === true && this.renderSuccessDialog()}
        {reloaded === false && this.renderErrorDialog()}
        <Toolbar>
          <Title>BSVP CSV Export</Title>
          <Actions>
            <IconButton
              onClick={() => {
                this.reload();
              }}
            >
              <RefreshIcon style={{ color: "white" }} />
            </IconButton>
            <IconButton onClick={showSettings}>
              <SettingsIcon style={{ color: "white" }} />
            </IconButton>
          </Actions>
        </Toolbar>
      </AppBar>
    );
  }

  reload() {
    this.setState({ reloading: true }, () => {
      get("/reload").then(response => {
        this.setState({ reloading: false, reloaded: response.success });
      });
    });
  }

  renderLoadingDialog() {
    return <LoadingDialog text="Server wird aktualisiert..." />;
  }

  renderSuccessDialog() {
    const actions = [
      {
        name: "Neu laden",
        onClick: () => {
          window.location.reload();
        },
        color: "primary"
      }
    ];
    return (
      <Dialog actions={actions} title="Aktualisierung erfolgreich">
        Der Server wurde erfolgreich aktualisiert.
        <br />
        Bitte neu laden.
      </Dialog>
    );
  }

  renderErrorDialog() {
    const actions = [
      {
        name: "Schließen",
        onClick: () => {
          this.setState({ reloaded: null });
        }
      }
    ];
    return (
      <Dialog actions={actions} title="Aktualisierung fehlgeschlagen">
        Der Server konnte nicht aktualisiert werden.
        <br />
        Bitte die Seite neu laden und erneut versuchen.
        <br />
        Beachten Sie, dass der Server nur aktualisiert werden kann, wenn kein
        Export läuft.
      </Dialog>
    );
  }
}

const Title = styled.div`
  font-weight: normal;
  font-size: 22px;
  flex: 1;
`;

const Actions = styled.div``;
