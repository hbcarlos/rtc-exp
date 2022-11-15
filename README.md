# RTC experiments

You can use this package as an interactive way of testing/debugging new feature in the Y-CRDT ecosystem. For example, you can try the new move feature moving an element from a javascript client and seen the update on a python client as follows:

1- Launch a websocket server:
		* Run a JavaScript server with: `cd yjs_client && yarn && yarn server`
		* or run a Python server with: `python ypy_client/server.py`
2- Launch a Yjs client: `cd yjs_client && yarn && yarn build:array && yarn start:http`
3- Launch a Ypy client: `jupyter-notebook client.ipynb` and run the first three cells
4- Initialize the document:
		1- Go to the empty webpage you launched in the step 2.
		2- Open the dev console in your browser.
		3- Access the YArray from the dev console by running: `const test = window.rtc.test;`.
		4- Add some items to the array from the dev console by running: `test.push([0,1,2,3,4,5,6,7,8,9]);`.
		6- Check the Ypy client was updated by running `print(test)` in the client.ipynb.
		5- Move an element from the dev console by running: `test.move(0, 3);`.
		6- Check again the Ypy client by running `print(test)` in the client.ipynb.

## Environment

```bash
# Create conda env and install dep
micromamba create -n rtc-exp -c python=3.10 nodejs=16 yarn rust maturin ypy-websocket
micromamba activate rtc-exp

# Install prerelease dependencies
pip install notebook --pre
pip install ypy-websocket

# Install Ypy from source
git clone https://github.com/y-crdt/ypy.git
cd ypy
maturin build
pip install .
```

## yjs_client package
This is a TypeScript package that creates an empty webpage with a YDoc an a YType inserted into the window object.
Once you open the webpage you can open the dev console of your browser and access the YType as follows:
`const test = window.rtc.test;`

For now, this package contains only one example. The example is a YDoc connected to `ws://localhost:8888/rtc_yjs_test` with a YArray called `test`.

### Build and run the example client
```bash
cd yjs_client
# install dependencies
yarn
# build example
yarn build:array
# start an http server to serve the empty webpage with a yjs client
yarn start:http
```

### Run a JavaScript websocket server for Y-CRDTs
To be able to sync clients we need a websocket server. The yjs_client includes a command to launch a server based on `y-websocket`.
```bash
cd yjs_client
# install dependencies
yarn
# run a server on 'localhost:8888'
yarn server
```


## ypy_client
This folder contains a python script to launch a websocket server based on `ypy-websocket` that runs on `localhost:8888` and a notebook with an example of a python client for Y-CRDTs (the counterpart to the yjs_client).

### Open the client
`jupyter-notebook client.ipynb`

### Launch the server
`python ypy_client/server.py`

