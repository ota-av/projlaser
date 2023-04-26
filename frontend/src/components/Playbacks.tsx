import { useEffect, useState } from "react";
import { Playback as PlaybackData } from "../types/playback";
import { listPlaybacks, playPlayback, recordPlayback } from "../api/playback";
import { socket } from "../socket";

export function Playback({
  id,
  active,
  isRecording,
  onRecord,
  setActive,
  pb,
}: {
  id: number;
  active: boolean;
  setActive: (newActive: boolean) => void;
  isRecording: boolean;
  onRecord: () => void;
  pb?: PlaybackData;
}) {
  let color = "bg-gray-100";

  if (pb) color = "bg-blue-300 hover:bg-blue-400";

  if (isRecording) color = "bg-green-200 hover:bg-green-300";

  if (isRecording && pb) color = "bg-blue-300 hover:bg-blue-400";

  const mdown = () => {
    pb && setActive(true);
  };

  const mup = () => {
    pb && setActive(false);
  };

  return (
    <button
      className={
        "flex-1 p-2 aspect-square m-1 border border-gray-400 rounded transition duration-100 " +
        color
      }
      onClick={isRecording ? () => onRecord() : undefined}
      onMouseDown={() => mdown()}
      onMouseUp={() => mup()}
    >
      {pb?.name}
    </button>
  );
}

export function Playbacks({
  isRecording,
  onRecorded,
}: {
  isRecording: boolean;
  onRecorded: () => void;
}) {
  const [playbacks, setPlaybacks] = useState<PlaybackData[]>([]);
  const [activePlaybacks, setActivePlaybacks] = useState<number[]>([]);

  const onRecord = async (id: number) => {
    await recordPlayback(id);
    onRecorded();
  };

  useEffect(() => {
    const load = async () => {
      const { playbacks, active_ids } = await listPlaybacks();
      setPlaybacks(playbacks);
      setActivePlaybacks(active_ids);
    };

    const onPlaybackState = (ev: { id: number; action: "on" | "off" }) => {
      if (ev.action === "off") {
        setActivePlaybacks((oldActives) => {
          return [...oldActives.filter((compid) => compid !== ev.id)];
        });
      }
      if (ev.action === "on") {
        setActivePlaybacks((oldActives) => {
          return [...oldActives, ev.id];
        });
      }
    };

    const onNewPlayback = (pb: PlaybackData) => {
      setPlaybacks((oldPbs) => {
        return [...oldPbs, pb];
      });
    };

    socket.on("playback_state", onPlaybackState);
    socket.on("new_playback", onNewPlayback);

    load();

    return () => {
      socket.off("playback_state", onPlaybackState);
      socket.off("new_playback", onNewPlayback);
    };
  }, []);

  const changePbState = async (id: number, newState: boolean) => {
    await playPlayback(id, newState);
  };

  return (
    <div className="flex-1 overflow-auto">
      <div className="grid grid-cols-12">
        {Array.from(new Array(144), (x, i) => i).map((id) => {
          const pb = playbacks.find((pb) => pb.id === id);

          return (
            <Playback
              key={id}
              id={id}
              isRecording={isRecording}
              onRecord={() => onRecord(id)}
              active={activePlaybacks.indexOf(id) !== -1}
              setActive={(newState) => changePbState(id, newState)}
              pb={pb}
            ></Playback>
          );
        })}
      </div>
    </div>
  );
}
