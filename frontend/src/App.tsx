import React, { useEffect, useState } from "react";
import { Programmer } from "./components/Programmer";
import { BPMTapper } from "./components/BPMTapper";
import { Playbacks } from "./components/Playbacks";
import { socket } from "./socket";
import { getInfo, load, save } from "./api/api";
import { Multipliers } from "./components/Multipliers";

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [info, setInfo] = useState<{ showname?: string, multipliers: Record<string, number> }>();

  const [showProgrammer, setShowProgrammer] = useState(true);

  const [editingShowName, setEditingShowName] = useState("");

  useEffect(() => {
    const onTriggerReload = () => {
      window.location.reload();
    };

    const onMultiplierUpdate = (multipliers: Record<string, number>) => {
      setInfo((oldinfo) => {
        return {...oldinfo, multipliers}
      })
    }
    socket.on("reload", onTriggerReload);
    socket.on("multipliers", onMultiplierUpdate);

    const load = async () => {
      const info = await getInfo();
      setEditingShowName(info.showname);
      setInfo(info);
    };

    load();

    return () => {
      socket.off("reload", onTriggerReload);
      socket.off("multipliers", onMultiplierUpdate);
    };
  }, []);

  return (
    <div className="w-[100vw] h-[100vh] flex flex-col overflow-hidden">
      <p>{info?.showname}</p>
      <div className="flex-1 flex-row flex border-b border-slate-400 overflow-hidden ">
        <Playbacks
          isRecording={isRecording}
          onRecorded={() => setIsRecording(false)}
        />
        <div className="flex flex-col mx-2">
          <BPMTapper></BPMTapper>
          <div className="mt-2 flex flex-col border-t pt-2">
            <input
              type="text"
              className="border-b border-gray-400 outline-none focus:border-gray-700 transition duration-100"
              defaultValue={info?.showname}
              onChange={(ev) => setEditingShowName(ev.target.value)}
              value={editingShowName}
            ></input>
            <button
              className="p-2 mt-1 bg-blue-400 hover:bg-blue-600 transition duration-100 text-white rounded flex-1"
              onClick={() => save(editingShowName)}
            >
              Save show
            </button>
            <button
              className="p-2 mt-1 bg-blue-400 hover:bg-blue-600 transition duration-100 text-white rounded flex-1"
              onClick={() => load(editingShowName)}
            >
              Load show
            </button>
          </div>
          {info && <Multipliers multipliers={info?.multipliers}></Multipliers>}
          <button className="p-2 mt-1 bg-blue-400 hover:bg-blue-600 transition duration-100 text-white rounded flex-1" onClick={() => setShowProgrammer(!showProgrammer)}>{showProgrammer ? 'hide' : 'show'} programmer</button>
        </div>
      </div>

      <Programmer
        show={showProgrammer}
        isRecording={isRecording}
        onRecord={() => setIsRecording(!isRecording)}
      ></Programmer>
    </div>
  );
}

export default App;
