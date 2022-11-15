const ws = require('ws');
const Y = require('yjs');
const WebsocketProvider = require('y-websocket').WebsocketProvider;

const doc = new Y.Doc();
const todo = doc.getArray('todo');
const provider = new WebsocketProvider('ws://localhost:8888', 'rtc_test_move_feature_0', doc, { WebSocketPolyfill: ws });

provider.on('status', event => console.debug("STATUS:", event.status));
provider.on('sync', (isSynced) => console.debug("SYNC:", isSynced));
provider.on('connection-close', event => console.debug("CONNECTION CLOSED:", event.message));
provider.on('connection-error', event => console.debug("CONNECTION ERROR:", event.message));

doc.on('update', (update, origin, doc, tr) => console.debug("UPDATE:", update, origin, doc, tr));
todo.observe((event) => console.log("OBSERVER:", event.changes));

//todo.unobserve(observe);