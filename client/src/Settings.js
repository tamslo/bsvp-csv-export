import React, { Component } from "react";
import styled from "styled-components";
import Drawer from "@material-ui/core/Drawer";
import Button from "@material-ui/core/Button";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";

export default class Settings extends Component {
  render() {
    const { open, manufacturers, close } = this.props;
    return (
      <Drawer open={open} anchor="right" onClose={close} className="Settings">
        <Container>
          <h3>Hersteller Auswahl</h3>
          <Text>
            Hersteller werden nicht auf den Konfigurator Export angewendet.
          </Text>
          <StyledButton
            variant="contained"
            color="primary"
            onClick={this.toggleAll.bind(this)}
          >
            {this.buttonText()}
          </StyledButton>
          <Manufacturers>
            {Object.keys(manufacturers).map(this.renderManufacturer.bind(this))}
          </Manufacturers>
        </Container>
      </Drawer>
    );
  }

  buttonText() {
    const { selectAll } = this.props;
    return selectAll ? "Alle auswählen" : "Alle abwählen";
  }

  toggleAll() {
    const { toggleAll, selectAll } = this.props;
    toggleAll(selectAll);
  }

  renderManufacturer(manufacturer) {
    const { manufacturers, toggleManufacturer } = this.props;
    return (
      <FormControlLabel
        key={manufacturer}
        control={
          <Checkbox
            color="primary"
            checked={manufacturers[manufacturer]}
            onChange={() => toggleManufacturer(manufacturer)}
            value={manufacturer}
          />
        }
        label={manufacturer}
      />
    );
  }
}

const StyledButton = styled(Button)`
  align-self: baseline;
`;

const Text = styled.div`
  text-wrap: wrap;
  margin: 15px 0;
`;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  padding: 10px;
  max-width: 25vw;
`;

const Manufacturers = styled.div`
  margin: 10px;
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
`;
