import { Doc, Array, YArrayEvent, Transaction } from 'yjs';
import { WebsocketProvider } from 'y-websocket';
import * as React from "react";

export class ListExample extends React.Component {
  private _doc = new Doc();
  private _todo: Array<number> = this._doc.getArray('todo');
  private _provider = new WebsocketProvider('ws://localhost:8888/doc/', 'todo_room_id', this._doc);

  constructor(props) {
    super(props);

    this._doc.transact(() => {
      this._todo.insert(0, [20,21,22,23,24,25]);
    });
    
    console.debug("ListExample:", this._todo.toArray());

    this._provider.on('status', event => {
      console.debug("ListExample");
      console.log(event.status);
    });

    this._doc.on('update', (update: Uint8Array, origin: any, doc: Doc, tr: Transaction) => {
      console.debug("UPDATE:", update);
    })
  }

  componentDidMount(): void {
    console.debug("componentDidMount:", this._todo.toArray());
    this._todo.observe(this._observer);
  }

  componentWillUnmount(): void {
    this._todo.unobserve(this._observer);
  }

  private _observer = (event: YArrayEvent<string>) => {
    console.log("_observer:", event.delta);
    this.forceUpdate();
  }

  render() {
    return <div>
        <h5>YArray test list</h5>
        <div>{this._todo.length}</div>
        <div>{this._todo.toArray()}</div>
        <ul>{this._todo.map(el => <li key={el}>{el}</li>)}</ul>
      </div>;
  }
}