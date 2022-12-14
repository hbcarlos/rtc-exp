use std::sync::Arc;
use tokio::select;
use tokio::sync::RwLock;
use warp::ws::{WebSocket, Ws};
use warp::{Filter, Rejection, Reply};
use yrs::{Doc, Transaction};
use yrs::types::array::ArrayEvent;
use yrs_warp::awareness::{Awareness, AwarenessRef};
use yrs_warp::broadcast::BroadcastGroup;
use yrs_warp::ws::WarpConn;


#[tokio::main]
async fn main() {
    println!("Yrs Client:");

    // We're using a single static document shared among all the peers.
    let awareness: AwarenessRef = {
        let doc = Doc::new();
        {
            // pre-initialize code mirror document with some text
            let mut txn = doc.transact();
            let mut test = txn.get_array("test");
            println!("Test array: {}", test.to_json());
            test.observe(observe);
        }
        Arc::new(RwLock::new(Awareness::new(doc)))
    };

    //let awareness = Arc::new(RwLock::new(Awareness::new(doc)));
    // open a broadcast group that listens to awareness and document updates
    // and has a pending message buffer of up to 32 updates
    let bcast = Arc::new(BroadcastGroup::open(awareness.clone(), 32).await);

    // pass dependencies to awareness and broadcast group to every new created connection
    let ws = warp::path("rtc_yjs_test")
        .and(warp::ws())
        .and(warp::any().map(move || awareness.clone()))
        .and(warp::any().map(move || bcast.clone()))
        .and_then(ws_handler);
    
    warp::serve(ws).run(([127, 0, 0, 1], 8888)).await;
}

fn observe(_txn: &Transaction, e: &ArrayEvent) -> () {
    println!("Event: {}", e.target().to_json());
    //for d in e.delta(txn).to_vec().iter() {
    //    println!("Event: {}", <&Change as Into<Any>>::into(d));
    //}
}

async fn ws_handler(
    ws: Ws,
    awareness: AwarenessRef,
    bcast: Arc<BroadcastGroup>,
) -> Result<impl Reply, Rejection> {
    println!("ws_handler:");
    Ok(ws.on_upgrade(move |socket| peer(socket, awareness, bcast)))
}

async fn peer(ws: WebSocket, awareness: AwarenessRef, bcast: Arc<BroadcastGroup>) {
    println!("peer:");
    // create new web socket connection wrapper that communicates via y-sync protocol
    let conn = WarpConn::new(awareness, ws);
    // subscribe a new connection to the broadcast group
    let sub = bcast.join(conn.inbox().clone());
    select! {
        res = sub => {
            match res {
                Ok(_) => println!("broadcasting for channel finished successfully"),
                Err(e) => eprintln!("broadcasting for channel finished abruptly: {}", e),
            }
        }
        res = conn => {
            match res {
                Ok(_) => println!("peer disconnected"),
                Err(e) => eprintln!("peer error occurred: {}", e),
            }
        }
    }
}