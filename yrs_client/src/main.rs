use std::sync::Arc;
use tokio::select;
use tokio::sync::RwLock;
use warp::ws::{WebSocket, Ws};
use warp::{Filter, Rejection, Reply};

use y_sync::awareness::Awareness;

use y_sync::awareness::Awareness;
use y_sync::sync::{DefaultProtocol, Error, MessageReader, Protocol, SyncMessage};

use yrs::{Doc, Array, Observable, Transact};
use yrs::types::ToJson;
use yrs_warp::broadcast::BroadcastGroup;
use yrs_warp::ws::WarpConn;
use yrs_warp::AwarenessRef;


use tungstenite::{ connect, Message };
use url::Url;


#[tokio::main]
async fn main() {
    println!("Yrs Client:");

    // Create YDoc
    let doc = Doc::new();
    let awareness = Awareness::new(doc);

    // Connect to the WS server locally
    let (mut socket, _response) = connect(Url::parse("ws://localhost:8889/rtc_yjs_test").unwrap()).expect("Can't connect");

    // Create SYNC_1 message
    let payload = {
        let mut encoder = EncoderV1::new();
        protocol.start(&awareness, &mut encoder)?;
        encoder.to_vec()
    };

    // Send SYNC_1 message
    socket.write_message(Message::Binary(payload)).unwrap();
    
    // Loop forever, handling parsing each message
    loop {
        let msg = socket.read_message().expect("Error reading message");
        //let payload = Message::into_data(msg);
        let payload = msg.into_data();
        
        match msg {
            SyncMessage::SyncStep1(sv) => {
                let result = protocol.handle_sync_step1(&awareness, sv).unwrap();

                // Create SYNC_2 message

                // Send SYNC_2 message
                socket.write_message(Message::Binary(result)).unwrap();
            }
            SyncMessage::SyncStep2(sv) => {
                let result = protocol.handle_sync_step2(&awareness, sv).unwrap();

                // Create SYNC_2 message

                // Send SYNC_2 message
                socket.write_message(Message::Binary(result)).unwrap();
            }
            tungstenite::Message::Text(s) => { s }
            _ => { panic!() }
        };
        let parsed: serde_json::Value = serde_json::from_str(&msg).expect("Can't parse to JSON");
        println!("{:?}", parsed["result"]);
    }



    // We're using a single static document shared among all the peers.
    /* let awareness: AwarenessRef = {
        let doc = Doc::new();
        {
            let mut test = doc.get_or_insert_array("test");
            test.observe(|txn, e| {
                println!("Event: {}", e.target().to_json(txn));
            });

            let mut txn = doc.transact_mut();
            println!("Test array: {}", test.to_json(&mut txn));

            test.insert_range(&mut txn, 0, [0,1,2,3,4]);
            println!("Test array: {}", test.to_json(&mut txn));
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
    
    warp::serve(ws).run(([0, 0, 0, 0], 8889)).await; */
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