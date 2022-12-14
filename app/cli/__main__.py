import typer
from typing import List

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import BufferControl

import asyncio
import y_py as Y
from websockets import connect
from ypy_websocket import WebsocketProvider

app = typer.Typer()

@app.command()
def read(host: str = "localhost", port: int = 8888, path: str = "test_room_id"):
    print("Reading client")
    change = asyncio.Event()

    def callbackText(event):
        print(str(event.target))
    
    def callbackArray(event):
        print(event.target.to_json())

    async def client():
        ydoc = Y.YDoc()
        text = ydoc.get_text('source')
        idText = text.observe(callbackText)
        todo = ydoc.get_array('todo')
        idTodo = todo.observe(callbackArray)

        ws = await connect(f"ws://{host}:{port}/doc/{path}")
        WebsocketProvider(ydoc, ws)
        
        #await asyncio.Future()
        await asyncio.wait_for(change.wait(), timeout=9999999)

        text.unobserve(idText)
        todo.unobserve(idTodo)

    asyncio.run(client())

@app.command()
def write(host: str = "localhost", port: int = 8888, path: str = "test_room_id"):
    print("Writing client")

    kb = KeyBindings()
    @kb.add('c-q')
    def exit_(event):
        event.app.exit()
    
    def on_text_changed(event):
        #print("on_text_changed:", event)
        with ydoc.begin_transaction() as t:
            text.delete_range(t, 0, len(text))
            text.insert(t, 0, event.text)

    def on_text_insert(event):
        #print("on_text_insert:", event)
        pass

    # Define application.
    buffer = Buffer(on_text_changed=on_text_changed, on_text_insert=on_text_insert)
    window = Window(content=BufferControl(buffer=buffer))
    application = Application(layout=Layout(window), key_bindings=kb, full_screen=True)
    application.layout.focus(window)

    print("Client")
    ydoc = Y.YDoc()
    text = ydoc.get_text('source')

    async def client():
        print("Connect")
        ws = await connect(f"ws://{host}:{port}/doc/{path}")
        WebsocketProvider(ydoc, ws)

        print("Input")
        await application.run_async()
        
        print("Done:")
        print(str(text))
    
    asyncio.run(client())

@app.command()
def list(host: str = "localhost", port: int = 8888, path: str = "todo_room_id", initialize: bool = True):
    print("List client")

    async def client():
        doc = Y.YDoc()
        todo = doc.get_array('todo')
        print("prelim:", todo.prelim)

        print("connect")
        ws = await connect(f"ws://{host}:{port}/doc/{path}")
        WebsocketProvider(doc, ws)
        
        if initialize :
            print("clean")
            with doc.begin_transaction() as t:
                todo.delete_range(t, 0, len(todo))
            print(len(todo))
            print(todo.to_json())

            await asyncio.sleep(2)
        
        else :
            change = asyncio.Event()
            def callbackArray(event):
                print("Synced:", event.target.to_json())
                change.set()
            
            idTodo = todo.observe(callbackArray)
            await asyncio.wait_for(change.wait(), timeout=60)
            todo.unobserve(idTodo)

            await asyncio.sleep(2)

        

        print("FORWARD:")
        print("*"*100)
        print("Move 1-2 to 4")
        with doc.begin_transaction() as t:
            todo.delete_range(t, 0, len(todo))
            todo.extend(t, [1,2,3,4])
        print(todo.to_json())
        with doc.begin_transaction() as t:
            todo.move_range_to(t, 1, 2, 4)
        print(todo.to_json())
        print()

        await asyncio.sleep(2)

        print("Move 0-0 to 10")
        with doc.begin_transaction() as t:
            todo.delete_range(t, 0, len(todo))
            todo.extend(t, [0,1,2,3,4,5,6,7,8,9])
        print(todo.to_json())
        with doc.begin_transaction() as t:
            todo.move_range_to(t, 0, 0, 10)
        print(todo.to_json())
        print()

        await asyncio.sleep(2)

        print("Move 0-1 to 10")
        with doc.begin_transaction() as t:
            todo.delete_range(t, 0, len(todo))
            todo.extend(t, [0,1,2,3,4,5,6,7,8,9])
        print(todo.to_json())
        with doc.begin_transaction() as t:
            todo.move_range_to(t, 0, 1, 10)
        print(todo.to_json())
        print()

        await asyncio.sleep(2)

        print("Move 3-5 to 7")
        with doc.begin_transaction() as t:
            todo.delete_range(t, 0, len(todo))
            todo.extend(t, [0,1,2,3,4,5,6,7,8,9])
        print(todo.to_json())
        with doc.begin_transaction() as t:
            todo.move_range_to(t, 3, 5, 7)
        print(todo.to_json())
        print()

        await asyncio.sleep(2)

        print("Move 1-0 to 10")
        with doc.begin_transaction() as t:
            todo.delete_range(t, 0, len(todo))
            todo.extend(t, [0,1,2,3,4,5,6,7,8,9])
        print(todo.to_json())
        with doc.begin_transaction() as t:
            todo.move_range_to(t, 1, 0, 10)
        print(todo.to_json())
        print("Nothing")
        print()

        await asyncio.sleep(2)

        print("Move 3-5 to 5")
        with doc.begin_transaction() as t:
            todo.delete_range(t, 0, len(todo))
            todo.extend(t, [0,1,2,3,4,5,6,7,8,9])
        print(todo.to_json())
        with doc.begin_transaction() as t:
            todo.move_range_to(t, 3, 5, 5)
        print(todo.to_json())
        print("Nothing")
        print()

        await asyncio.sleep(2)


        print("BACKWARD:")
        print("*"*100)
        print("Move 9-9 to 0")
        with doc.begin_transaction() as t:
            todo.delete_range(t, 0, len(todo))
            todo.extend(t, [0,1,2,3,4,5,6,7,8,9])
        print(todo.to_json())
        with doc.begin_transaction() as t:
            todo.move_range_to(t, 9, 9, 0)
        print(todo.to_json())
        print()

        await asyncio.sleep(2)

        print("Move 8-9 to 0")
        with doc.begin_transaction() as t:
            todo.delete_range(t, 0, len(todo))
            todo.extend(t, [0,1,2,3,4,5,6,7,8,9])
        print(todo.to_json())
        with doc.begin_transaction() as t:
            todo.move_range_to(t, 8, 9, 0)
        print(todo.to_json())
        print()

        await asyncio.sleep(2)

        print("Move 4-6 to 3")
        with doc.begin_transaction() as t:
            todo.delete_range(t, 0, len(todo))
            todo.extend(t, [0,1,2,3,4,5,6,7,8,9])
        print(todo.to_json())
        with doc.begin_transaction() as t:
            todo.move_range_to(t, 4, 6, 3)
        print(todo.to_json())
        print()

        await asyncio.sleep(2)

        print("Move 3-5 to 3")
        with doc.begin_transaction() as t:
            todo.delete_range(t, 0, len(todo))
            todo.extend(t, [0,1,2,3,4,5,6,7,8,9])
        print(todo.to_json())
        with doc.begin_transaction() as t:
            todo.move_range_to(t, 3, 5, 3)
        print(todo.to_json())
        print("Nothing")
        print()

        await asyncio.sleep(2)

        print("FAIL FORWARD:")
        print("*"*100)
        print("Move -1-2 to 5")
        try :
            with doc.begin_transaction() as t:
                todo.delete_range(t, 0, len(todo))
                todo.extend(t, [0,1,2,3,4,5,6,7,8,9])
            print(todo.to_json())
            with doc.begin_transaction() as t:
                todo.move_range_to(t, -1, 2, 5)
            print(todo.to_json())
            print()
        except:
            print("Failed")
            print()

        await asyncio.sleep(2)

        print("Move 0--1 to 3")
        try :
            with doc.begin_transaction() as t:
                todo.delete_range(t, 0, len(todo))
                todo.extend(t, [0,1,2,3,4,5,6,7,8,9])
            print(todo.to_json())
            with doc.begin_transaction() as t:
                todo.move_range_to(t, 0, -1, 3)
            print(todo.to_json())
            print()
        except:
            print("Failed")
            print()

        await asyncio.sleep(2)

        print("Move 0-1 to 11")
        try :
            with doc.begin_transaction() as t:
                todo.delete_range(t, 0, len(todo))
                todo.extend(t, [0,1,2,3,4,5,6,7,8,9])
            print(todo.to_json())
            with doc.begin_transaction() as t:
                todo.move_range_to(t, 0, 1, 11)
            print(todo.to_json())
            print()
        except:
            print("Failed")
            print()

        await asyncio.sleep(2)


        print("FAIL BACKWARD:")
        print("*"*100)

    asyncio.run(client())

@app.command()
def test(host: str = "localhost", port: int = 8888, path: str = "test_room_id"):
    print("Test client:")

    def callback(event):
        print("Event:")
        print("\tDelta:", str(event.delta))
        print("\tText:", str(event.target))

    async def client():
        print("Client 1:")
        ydoc_1 = Y.YDoc()
        text_1 = ydoc_1.get_text('source')
        print("\tconnect")
        ws_1 = await connect(f"ws://{host}:{port}/doc/{path}")
        WebsocketProvider(ydoc_1, ws_1)

        with ydoc_1.begin_transaction() as t:
            text_1.insert(t, 0, "Inserted at 0")
        print("\ttext 1:", str(text_1))

        with ydoc_1.begin_transaction() as t:
            text_1.delete_range(t, 0, len(text_1))
            text_1.insert(t, 0, "Inserted at 0 after deleting")
        print("\ttext 1:", str(text_1))

        print("Client 2:")
        ydoc_2 = Y.YDoc()
        text_2 = ydoc_2.get_text('source')
        id_text_2 = text_2.observe(callback)
        print("\tconnect")
        ws_2 = await connect(f"ws://{host}:{port}/doc/{path}")
        provider = WebsocketProvider(ydoc_2, ws_2)
        print("\ttext 2:", str(text_2))

        await asyncio.sleep(20)
        text_2.unobserve(id_text_2)
        provider.disconnect()

        print("Test client ended")
    
    asyncio.run(client())

@app.command()
def move():
    print("Move client:")


    print("FORWARD:")
    print("*"*100)
    print("Move 0-1 to 10")
    v = [0,1,2,3,4,5,6,7,8,9]
    print(v)
    print(move_range_to(v, 0, 1, 10))
    print()

    print("Move 3-5 to 7")
    v = [0,1,2,3,4,5,6,7,8,9]
    print(v)
    print(move_range_to(v, 3, 5, 7))
    print()

    print("Move 1-0 to 10")
    v = [0,1,2,3,4,5,6,7,8,9]
    print(v)
    print(move_range_to(v, 1, 0, 10))
    print("nothing")
    print()

    print("Move 3-5 to 5")
    v = [0,1,2,3,4,5,6,7,8,9]
    print(v)
    print(move_range_to(v, 3, 5, 5))
    print("nothing")
    print()


    print("BACKWARD:")
    print("*"*100)
    print("Move 9-9 to 0")
    v = [0,1,2,3,4,5,6,7,8,9]
    print(v)
    print(move_range_to(v, 9, 9, 0))
    print()

    print("Move 8-9 to 0")
    v = [0,1,2,3,4,5,6,7,8,9]
    print(v)
    print(move_range_to(v, 8, 9, 0))
    print()

    print("Move 4-6 to 3")
    v = [0,1,2,3,4,5,6,7,8,9]
    print(v)
    print(move_range_to(v, 4, 6, 3))
    print()

    print("Move 3-5 to 3")
    v = [0,1,2,3,4,5,6,7,8,9]
    print(v)
    print(move_range_to(v, 3, 5, 3))
    print("nothing")
    print()

    
    print("FAIL FORWARD:")
    print("*"*100)

    print("Move -1-2 to 5")
    v = [0,1,2,3,4,5,6,7,8,9]
    print(v)
    print(move_range_to(v, -1, 2, 5))
    print()

    print("Move 0--1 to 3")
    v = [0,1,2,3,4,5,6,7,8,9]
    print(v)
    print(move_range_to(v, -1, 2, 5))
    print()

    print("Move 0-1 to 11")
    v = [0,1,2,3,4,5,6,7,8,9]
    print(v)
    print(move_range_to(v, 0, 1, 11))
    print()


    print("FAIL BACKWARD:")
    print("*"*100)

    


def move_range_to(v: List, start: int, end: int, target: int):
    if start < 0 or end < 0 or target < 0:
        print("\tIndex out of bound")
        return v
    if start > len(v) or end > len(v) or target > len(v):
        print("\tIndex out of bound")
        return v

    if target >= start and target <= end:
        print("\tTarget within range")
        return v
    
    i = 0
    n = end - start + 1
    backwards = target > end
    while n > 0:
        item = v[start + i]
        v.remove(item)
        if backwards:
            v.insert(target - 1, item)
        else:
            v.insert(target + i, item)
            i += 1
        n -= 1
    
    return v
