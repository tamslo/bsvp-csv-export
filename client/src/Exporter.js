import React, { Component, Fragment } from "react";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Collapse from "@material-ui/core/Collapse";
import ExpandLess from "@material-ui/icons/ExpandLess";
import ExpandMore from "@material-ui/icons/ExpandMore";
import IconButton from "@material-ui/core/IconButton";
import PlayIcon from "@material-ui/icons/PlayArrowOutlined";
import LogIcon from "@material-ui/icons/DescriptionOutlined";
import ResultIcon from "@material-ui/icons/GetAppOutlined";
import CircularProgress from "@material-ui/core/CircularProgress";
import styled from "styled-components";
import { backendUrl } from "./api";

const unixTimestamp = () => {
  return new Date().getTime();
};

export default class Exporter extends Component {
  constructor(props) {
    super(props);
    const { scheduled, running } = props;
    this.state = { open: scheduled || running, downloadId: unixTimestamp() };
  }

  toggleLog() {
    const { open } = this.state;
    this.setState({ open: !open });
  }

  render() {
    const { name, last } = this.props;
    const { open } = this.state;
    const disabled = !this.hasLog();
    return (
      <Fragment>
        <ListItem
          button
          onClick={disabled ? () => {} : this.toggleLog.bind(this)}
          className="Exporter"
        >
          <ListItemText primary={name} secondary={last} />
          <Actions>
            {this.renderDownloadButtons()}
            {this.renderRunButton()}
            {this.renderExpandButton()}
          </Actions>
        </ListItem>
        <Collapse in={open} timeout="auto" unmountOnExit>
          {this.renderLog()}
        </Collapse>
      </Fragment>
    );
  }

  renderRunButton() {
    const { scheduled, running } = this.props;
    if (running) {
      return <StyledCircularProgress />;
    } else {
      return (
        <IconButton onClick={this.runExporter.bind(this)} disabled={scheduled}>
          <PlayIcon />
        </IconButton>
      );
    }
  }

  renderExpandButton() {
    const { open } = this.state;
    const disabled = !this.hasLog();
    return (
      <IconButton
        onClick={disabled ? this.toggleLog.bind(this) : () => {}}
        disabled={disabled}
      >
        {open && !disabled ? <ExpandLess /> : <ExpandMore />}
      </IconButton>
    );
  }

  runExporter(event) {
    const { runExporter } = this.props;
    event.stopPropagation();
    this.setState({ open: true }, runExporter);
  }

  downloadDisabled() {
    const { last, scheduled, running } = this.props;
    return last === null || scheduled || running;
  }

  downloadPath(downloadType) {
    // Use downloadId to avoid caching
    const { downloadId } = this.state;
    const { id } = this.props;
    const disabled = this.downloadDisabled();
    return (
      (disabled && "") ||
      `${backendUrl}/${downloadType}?exporter=${id}&id=${downloadId}`
    );
  }

  renderDownloadButtons() {
    const disabled = this.downloadDisabled();
    const handleDownload = event => {
      event.stopPropagation();
      this.setState({ downloadId: unixTimestamp() });
    };

    return (
      <Fragment>
        <IconButton
          href={this.downloadPath("result")}
          onClick={event => handleDownload(event)}
          disabled={disabled}
        >
          <ResultIcon />
        </IconButton>
        <IconButton
          href={this.downloadPath("log")}
          onClick={event => handleDownload(event)}
          disabled={disabled}
        >
          <LogIcon />
        </IconButton>
      </Fragment>
    );
  }

  hasLog() {
    const { log } = this.props;
    return log.length !== 0;
  }

  renderLog() {
    const { log } = this.props;
    if (log.length > 0) {
      return (
        <LogContainer>
          {log.map((message, index) => (
            <LogEntry key={`entry-${index}`}>{message}</LogEntry>
          ))}
        </LogContainer>
      );
    }
  }
}

const LogContainer = styled.div`
  padding: 5px 20px;
`;

const LogEntry = styled.div`
  font-family: monospace;
  font-size: 12px;
  line-height: 18px;
`;

const Actions = styled.div`
  display: flex;
`;

const StyledCircularProgress = styled(CircularProgress)`
  height: 24px !important;
  width: 24px !important;
  margin: 12px;
`;
