import { useEffect, useState, MouseEvent, Fragment } from "react";
import { Playback as PlaybackData } from "../types/playback";
import { listPlaybacks, playPlayback, recordPlayback } from "../api/api";
import { socket } from "../socket";

export function PlaybackEditModal({
  pb,
  onClose,
}: {
  pb?: PlaybackData;
  onClose: () => void;
}) {
  return <div></div>;
}

export function Playback({
  id,
  active,
  isRecording,
  onRecord,
  setActive,
  onEditPlayback,
  pb,
}: {
  id: number;
  active: boolean;
  setActive: (newActive: boolean) => void;
  isRecording: boolean;
  onRecord: () => void;
  onEditPlayback: () => void;
  pb?: PlaybackData;
}) {
  let color = "bg-gray-100";

  if (pb) color = "bg-blue-300 hover:bg-blue-400";

  if (active) color = "bg-violet-300 hover:bg-violet-400";

  if (!pb && !active && isRecording) color = "bg-green-200 hover:bg-green-300";

  const mdown = (ev: MouseEvent) => {
    if (ev.button !== 0) return; // Not leftclick
    !isRecording && pb && setActive(true);
  };

  const mup = (ev: MouseEvent) => {
    if (ev.button !== 0) return; // Not leftclick
    !isRecording && pb && setActive(false);
  };

  const contextMenu = (ev: MouseEvent) => {
    ev.preventDefault();
    onEditPlayback();
  };

  return (
    <Fragment>
      <button
        className={
          "flex-1 p-2 aspect-square m-1 border border-gray-400 rounded transition duration-100 " +
          color
        }
        onClick={isRecording ? () => onRecord() : undefined}
        onMouseDown={(ev) => mdown(ev)}
        onMouseUp={(ev) => mup(ev)}
        onContextMenu={contextMenu}
      >
        {pb?.name}
      </button>
    </Fragment>
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

    const onUpdatePlayback = (pb: PlaybackData) => {
      setPlaybacks((oldPbs) => {
        const cp = [...oldPbs];
        const i = cp.findIndex((comppb) => comppb.id === pb.id);
        cp[i] = pb;
        return cp;
      });
    };

    socket.on("playback_state", onPlaybackState);
    socket.on("new_playback", onNewPlayback);
    socket.on("update_playback", onUpdatePlayback);

    load();

    return () => {
      socket.off("playback_state", onPlaybackState);
      socket.off("new_playback", onNewPlayback);
      socket.off("update_playback", onUpdatePlayback);
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
              onEditPlayback={() => {}}
              pb={pb}
            ></Playback>
          );
        })}
      </div>
    </div>
  );
}
