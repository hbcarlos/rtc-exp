import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';
import * as React from "react";

export class TextEditor extends React.Component {
  private _doc = new Y.Doc();
  private _source = this._doc.getText('source');
  private _provider = new WebsocketProvider('ws://localhost:8888/doc/', 'test_room_id', this._doc);

  constructor(props) {
    super(props);
    this.state = { txt: "" }

    this._provider.on('status', event => {
      console.debug("TextEditor:");
      console.log(event.status);
    });
  }

  componentDidMount(): void {
    this._source.observe(this._observer);
  }

  componentWillUnmount(): void {
    this._source.unobserve(this._observer);
  }

  private _observer = (event: Y.YTextEvent) => {
    console.log(event.delta);
    this.forceUpdate();
  }

  render() {
    return <span>{this._source.toJSON()}</span>;
  }
}