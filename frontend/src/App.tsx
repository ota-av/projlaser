import React, { useState } from "react";
import { Programmer } from "./components/Programmer";
import { BPMTapper } from "./components/BPMTapper";
import { Playbacks } from "./components/Playbacks";

function App() {
  const [isRecording, setIsRecording] = useState(false);

  return (
    <div className="w-[100vw] h-[100vh] flex flex-col overflow-hidden">
      <div className="flex-1 flex-row flex border-b border-slate-400 overflow-hidden ">
        <Playbacks
          isRecording={isRecording}
          onRecorded={() => setIsRecording(false)}
        />
        <div>
          <BPMTapper></BPMTapper>
        </div>
      </div>

      <Programmer
        isRecording={isRecording}
        onRecord={() => setIsRecording(!isRecording)}
      ></Programmer>
    </div>
  );
}

export default App;
