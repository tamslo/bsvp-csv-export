import React from "react";
import Dialog from "@material-ui/core/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContent from "@material-ui/core/DialogContent";
import DialogActions from "@material-ui/core/DialogActions";
import Button from "@material-ui/core/Button";

export default props => {
  const { title, actions } = props;
  return (
    <Dialog open={true}>
      {title && <DialogTitle>{title}</DialogTitle>}
      <DialogContent>{props.children}</DialogContent>
      {actions && <DialogActions>{actions.map(renderAction)}</DialogActions>}
    </Dialog>
  );
};

const renderAction = action => {
  return (
    <Button
      key={`action-${action.name}`}
      onClick={action.onClick}
      color={action.color || "default"}
    >
      {action.name}
    </Button>
  );
};
