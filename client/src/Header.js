import React from "react";
import styled from "styled-components";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import IconButton from "@material-ui/core/IconButton";
import SettingsIcon from "@material-ui/icons/Settings";

export default props => {
  const { showSettings } = props;
  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Title>BSVP CSV Export</Title>
        <Actions>
          <IconButton onClick={showSettings}>
            <SettingsIcon style={{ color: "white" }} />
          </IconButton>
        </Actions>
      </Toolbar>
    </AppBar>
  );
};

const Title = styled.div`
  font-weight: normal;
  font-size: 22px;
  flex: 1;
`;

const Actions = styled.div``;
