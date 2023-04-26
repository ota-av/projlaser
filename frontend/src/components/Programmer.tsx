import {
  getProgrammer,
  modifyProgrammer,
  clearProgrammer,
  getLayers,
} from "../api/api";

import {
  useState,
  useEffect,
  ReactNode,
  EventHandler,
  MouseEventHandler,
  HTMLProps,
  ButtonHTMLAttributes,
} from "react";
import { AllowedParams, FxParam, Playback } from "../types/playback";

import { ColorGroup, OpacityGroup, PosGroup, paramGroups } from "./Param";
import { socket } from "../socket";

export function SelectButton({
  children,
  onClick,
  className,
  active,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { active: boolean }) {
  return (
    <button
      className={
        `rounded p-2 m-1 ${
          active ? "bg-blue-600" : "bg-blue-400"
        } hover:bg-blue-600 transition duration-100 text-white text-lg` +
        (className ? " " + className : "")
      }
      onClick={onClick}
    >
      {children}
    </button>
  );
}

export function Programmer({
  className,
  onRecord,
  isRecording,
}: {
  className?: string;
  onRecord: () => void;
  isRecording: boolean;
}) {
  const [programmer, setProgrammer] = useState<Playback>();
  const [error, setError] = useState<string>();

  const [layers, setLayers] = useState<string[]>([]);
  const [selectedLayer, setSelectedLayer] = useState<string>();
  const [selectedGroup, setSelectedGroup] =
    useState<(typeof paramGroups)[number]>();

  useEffect(() => {
    const load = async () => {
      try {
        setProgrammer(await getProgrammer());
        const layers = await getLayers();
        setLayers(layers);
        setSelectedLayer(layers[0]);
      } catch (error: any) {
        if (error && error instanceof Error) {
          setError((olderr) => {
            return olderr + error.message + "\n";
          });
        }
      }
    };

    const onProgrammer = (val: Playback) => {
      setProgrammer(val);
    };

    socket.on("programmer", onProgrammer);

    load();

    return () => {
      socket.off("programmer", onProgrammer);
    };
  }, []);

  const defaultClass = "bg-slate-200";

  return (
    <div className={className ? className + " " + defaultClass : defaultClass}>
      {error && (
        <p className="bg-red-200 p-2 whitespace-pre-line fixed top-0 w-full">
          {error}
        </p>
      )}
      <div className="flex flex-row m-2">
        <div>
          <p>Layer</p>
          <div>
            {layers.map((layer) => (
              <SelectButton
                className="w-10 h-10"
                active={layer === selectedLayer}
                onClick={() => setSelectedLayer(layer)}
              >
                {layer}
              </SelectButton>
            ))}
          </div>
          <p>Param</p>
          <div>
            {paramGroups.map((param) => (
              <SelectButton
                active={param === selectedGroup}
                onClick={() => setSelectedGroup(param)}
              >
                {param}
              </SelectButton>
            ))}
          </div>
        </div>
        <div className="border-l border-slate-400 ml-4 pl-4">
          {selectedLayer && programmer && (
            <OpacityGroup
              currentParams={programmer.layervalues[selectedLayer] || {}}
              onChange={(param, value) =>
                modifyProgrammer(selectedLayer, param, value)
              }
            ></OpacityGroup>
          )}
        </div>
        <div className="border-l border-slate-400 ml-4 pl-4 flex">
          {programmer && selectedLayer && selectedGroup === "color" && (
            <ColorGroup
              currentParams={programmer.layervalues[selectedLayer] || {}}
              onChange={(param, value) =>
                modifyProgrammer(selectedLayer, param, value)
              }
            ></ColorGroup>
          )}
          {programmer && selectedLayer && selectedGroup === "pos" && (
            <PosGroup
              currentParams={programmer.layervalues[selectedLayer] || {}}
              onChange={(param, value) =>
                modifyProgrammer(selectedLayer, param, value)
              }
            ></PosGroup>
          )}
        </div>
        <div className="flex justify-self-end ml-auto flex-col">
          <button
            className={
              "h-full m-1  text-lg transition duration-100 rounded p-2 px-4" +
              (isRecording
                ? " bg-green-600 hover:bg-green-400"
                : " hover:bg-green-600 bg-green-400")
            }
            onClick={() => onRecord()}
          >
            Record
          </button>
          <button
            className="h-full bg-red-400 m-1 hover:bg-red-600 text-white text-xl transition duration-100 rounded p-2 px-4"
            onClick={() => clearProgrammer()}
          >
            Clear
          </button>
        </div>
      </div>
    </div>
  );
}
