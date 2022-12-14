import { YDoc } from 'ywasm';
import { WebsocketProvider } from 'y-websocket';

const doc = new YDoc();
const test = doc.getArray('test');
const provider = new WebsocketProvider('ws://localhost:8888', 'rtc_yjs_test', doc);

provider.on('status', event => console.debug("STATUS:", event.status));
provider.on('sync', (isSynced) => console.debug("SYNC:", isSynced));
provider.on('connection-close', event => console.debug("CONNECTION CLOSED:", event.message));
provider.on('connection-error', event => console.debug("CONNECTION ERROR:", event.message));

doc.onUpdate((update, origin, doc, tr) => console.debug("UPDATE:", update, origin, doc, tr));

const observe = (event) => console.log("OBSERVER:", event.changes);
test.observe(observe);
window['rtc'] = { doc, test };
