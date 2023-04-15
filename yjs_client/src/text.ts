import { Doc } from 'yjs';
import { WebsocketProvider } from 'y-websocket';

const doc = new Doc();
const test = doc.getText('codemirror');
const provider = new WebsocketProvider('ws://localhost:8000', 'my-room', doc, { disableBc: true });

provider.on('status', event => console.debug("STATUS:", event.status));
provider.on('sync', (isSynced) => console.debug("SYNC:", isSynced));
provider.on('connection-close', event => console.debug("CONNECTION CLOSED:", event.message));
provider.on('connection-error', event => console.debug("CONNECTION ERROR:", event.message));

doc.on('update', (update, origin, doc, tr) => console.debug("UPDATE:", update, origin, doc, tr));

const observe = (event) => console.log("OBSERVER:", event.changes);
test.observe(observe);
window['rtc'] = { doc, test };
window.onclose = () => test.unobserve(observe);
