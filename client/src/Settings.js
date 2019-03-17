import React, { Component } from "react";
import Drawer from "@material-ui/core/Drawer";

export default class Settings extends Component {
  render() {
    const { open, manufacturers, close } = this.props;
    return (
      <Drawer open={open} anchor="right" onClose={close} className="Settings">
        {manufacturers.map(this.renderManufacturer.bind(this))}
      </Drawer>
    );
  }

  renderManufacturer(manufacturer) {
    // TODO: Show tickboxes
    // TODO: Set selected manufacturers in App
    // TODO: Select all
    return manufacturer.name;
  }
}
