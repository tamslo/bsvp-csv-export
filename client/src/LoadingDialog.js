import React from "react";
import styled from "styled-components";
import Dialog from "./Dialog";
import CircularProgress from "@material-ui/core/CircularProgress";

export default props => {
  return (
    <Dialog>
      <StyledDialogContent>
        {props.text}
        <StyledCircularProgress />
      </StyledDialogContent>
    </Dialog>
  );
};

const StyledDialogContent = styled.div`
  display: flex;
  align-items: center;
  font-size: large;
`;

const StyledCircularProgress = styled(CircularProgress)`
  height: 24px !important;
  width: 24px !important;
  margin: 12px;
`;
