import React, { Component } from "react";
import Card from "@material-ui/core/Card";
import IconButton from "@material-ui/core/IconButton";
import PlayIcon from "@material-ui/icons/PlayArrow";
import styled from "styled-components";

export default class Exporter extends Component {
  render() {
    const { name, scheduled, running, runExporter } = this.props;
    return (
      <Container className="Exporter">
        <StyledCard>
          <ContentContainer>
            <Name>{name}</Name>
            {scheduled.toString()}
            <Actions>
              <IconButton onClick={runExporter}>
                <PlayIcon />
              </IconButton>
            </Actions>
          </ContentContainer>
        </StyledCard>
      </Container>
    );
  }
}

const StyledCard = styled(Card)`
  border-radius: 1px !important;
`;

const Container = styled.div`
  margin: 10px 0px;
`;

const ContentContainer = styled.div`
  padding: 5px;
  display: flex;
`;

const Name = styled.div`
  flex: 1;
  display: flex;
  align-items: center;
  font-size: 18px;
  padding-left: 10px;
`;

const Actions = styled.div``;
