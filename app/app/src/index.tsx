import * as React from "react";
import { createRoot } from 'react-dom/client';

//import { TextEditor } from "./textEditor";
import { ListExample } from "./list";

const root = createRoot(document.getElementById("root"));

root.render(
  <div>
    <h3>Welcome to RTC experiments app</h3>
    {/* <TextEditor/> */}
    <ListExample/>
  </div>
);
