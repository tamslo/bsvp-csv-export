import React, { Component } from "react";
import Card from "@material-ui/core/Card";
import IconButton from "@material-ui/core/IconButton";
import PlayIcon from "@material-ui/icons/PlayArrow";
import CircularProgress from "@material-ui/core/CircularProgress";
import styled from "styled-components";

export default class Exporter extends Component {
  render() {
    const { name } = this.props;
    return (
      <Container className="Exporter">
        <StyledCard>
          <ContentContainer>
            <Name>{name}</Name>
            <Actions>{this.renderRunButton()}</Actions>
          </ContentContainer>
          {this.renderLog()}
        </StyledCard>
      </Container>
    );
  }

  renderRunButton() {
    const { scheduled, running, runExporter } = this.props;
    if (running) {
      return <StyledCircularProgress />;
    } else {
      return (
        <IconButton onClick={runExporter} disabled={scheduled}>
          <PlayIcon />
        </IconButton>
      );
    }
  }

  renderLog() {
    const { log } = this.props;
    if (log.length > 0) {
      return (
        <LogContainer>
          {log.map(message => (
            <LogEntry>{message}</LogEntry>
          ))}
        </LogContainer>
      );
    }
  }
}

const StyledCard = styled(Card)`
  border-radius: 1px !important;
`;

const Container = styled.div``;

const ContentContainer = styled.div`
  padding: 5px;
  display: flex;
`;

const LogContainer = styled.div`
  margin: 0 15px 15px 15px;
`;

const LogEntry = styled.div`
  font-family: monospace;
`;

const Name = styled.div`
  flex: 1;
  display: flex;
  align-items: center;
  font-size: 18px;
  padding-left: 10px;
`;

const Actions = styled.div``;

const StyledCircularProgress = styled(CircularProgress)`
  height: 24px !important;
  width: 24px !important;
  margin: 12px;
`;
