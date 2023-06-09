import { useEffect, useState, MouseEvent, Fragment } from "react";
import { Playback as PlaybackData } from "../types/playback";
import {
  deletePlayback,
  listPlaybacks,
  playPlayback,
  recordPlayback,
  updatePlaybackMeta,
} from "../api/api";
import { socket } from "../socket";
import Modal from "./Modal";
import { ChaseListing } from "./Chase";

export function PlaybackEditModal({
  pb,
  onClose,
  open,
}: {
  pb?: PlaybackData;
  open: boolean;
  onClose: () => void;
}) {
  return (
    <Modal open={open} onClose={onClose}>
      {pb && (
        <div className="flex flex-row">
          <div className="mr-2 pr-2 border-r">
              <button
            className="p-1 mx-2 bg-red-300 hover:bg-red-400 rounded"
            onClick={() => deletePlayback(pb.id)}
          >
            Delete
          </button>
            <p>Name</p>
            <input
              type="text"
              className="border-b border-gray-400 outline-none focus:border-gray-700 transition duration-100"
              value={pb.name}
              onChange={(ev) =>
                updatePlaybackMeta(pb.id, { name: ev.target.value })
              }
            ></input>
            <p className="mt-2">Priority</p>
            <input
              type="number"
              value={pb.priority}
              step={1}
              className="border-b border-gray-400 outline-none focus:border-gray-700 transition duration-100"
              onChange={(ev) =>
                updatePlaybackMeta(pb.id, { priority: Number(ev.target.value) })
              }
            ></input>
            <p className="mt-2">Keytype</p>
            <select
              value={pb.key}
              className="border-b border-gray-400 outline-none focus:border-gray-700 transition duration-100"
              onChange={(ev) => {
                updatePlaybackMeta(pb.id, {
                  key: ev.target.value as "flash" | "toggle",
                });
              }}
            >
              <option value="toggle">toggle</option>
              <option value="flash">flash</option>
            </select>
            <p className="mt-2">
              Sync
              <input
                type="checkbox"
                className="w-4 h-4 align-middle ml-2"
                checked={pb.sync}
                onChange={(ev) =>
                  updatePlaybackMeta(pb.id, { sync: ev.target.checked })
                }
              ></input>
            </p>
            <p className="mt-2">Duration (cycles)</p>
            <input
              type="number"
              value={pb.duration}
              step={1}
              className="border-b border-gray-400 outline-none focus:border-gray-700 transition duration-100"
              onChange={(ev) =>
                updatePlaybackMeta(pb.id, { duration: Number(ev.target.value) })
              }
            ></input>
            <p className="mt-2">Link multiplier</p>
            <input
              type="number"
              value={pb.link_multiplier_id}
              step={1}
              className="border-b border-gray-400 outline-none focus:border-gray-700 transition duration-100"
              onChange={(ev) =>
                updatePlaybackMeta(pb.id, { link_multiplier_id: ev.target.value })
              }
            ></input>
          </div>
          <ChaseListing pb_id={pb.id} chase={pb.chase} />
        </div>
      )}
    </Modal>
  );
}

export function Playback({
  active,
  isRecording,
  onRecord,
  setActive,
  onEditPlayback,
  pb,
}: {
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
    if (isRecording || !pb) return;

    if (pb.key === "flash") return setActive(true);
    return setActive(!active);
  };

  const mup = (ev: MouseEvent) => {
    if (ev.button !== 0) return; // Not leftclick
    if (isRecording || !pb) return;

    if (pb.key === "flash") return setActive(false);
  };

  const contextMenu = (ev: MouseEvent) => {
    ev.preventDefault();
    onEditPlayback();
  };

  return (
    <Fragment>
      <button
        className={
          "relative flex-1 m-1 flex flex-col aspect-video items-center justify-center border border-gray-400 rounded transition duration-100 " +
          color
        }
        onClick={isRecording ? () => onRecord() : undefined}
        onMouseDown={(ev) => mdown(ev)}
        onMouseUp={(ev) => mup(ev)}
        onContextMenu={contextMenu}
      >
        <span className="absolute top-0 left-0 w-min m-1">
          {(pb?.key === "toggle" && "T") || (pb?.key === "flash" && "F")}
        </span>
        <span className="absolute top-0 right-0 w-min m-1">{pb?.id}</span>
        <span className="p-2 mx-1">{pb?.name}</span>
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

  const [editPbId, setEditPbId] = useState<number | undefined>();

  const editingPb = playbacks.find((compPb) => compPb.id === editPbId);

  const onRecord = async (slot: number) => {
    await recordPlayback(slot);
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
    
    const onDeletePlayback = (pbid: number) => {
      setPlaybacks((oldPbs) => {
        return [...oldPbs.filter((val) => val.id !== pbid)];
      });
      setActivePlaybacks((oldPbs) => {
        return [...oldPbs.filter((val) => val !== pbid)];
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
    socket.on("delete_playback", onDeletePlayback);
    socket.on("update_playback", onUpdatePlayback);

    load();

    return () => {
      socket.off("playback_state", onPlaybackState);
      socket.off("new_playback", onNewPlayback);
      socket.off("update_playback", onUpdatePlayback);
      socket.off("delete_playback", onDeletePlayback);
    };
  }, []);

  const changePbState = async (id: number, newState: boolean) => {
    await playPlayback(id, newState);
  };

  return (
    <div className="flex-1 overflow-auto">
      <PlaybackEditModal
        open={editingPb !== undefined}
        pb={editingPb}
        onClose={() => setEditPbId(undefined)}
      ></PlaybackEditModal>
      <div className="grid grid-cols-12">
        {Array.from(new Array(144), (x, i) => i).map((slot) => {
          const pb = playbacks.find((pb) => pb.slot === slot);

          return (
            <Playback
              key={slot}
              isRecording={isRecording}
              onRecord={() => onRecord(slot)}
              active={(pb && activePlaybacks.indexOf(pb?.id) !== -1) || false}
              setActive={(newState) => pb && changePbState(pb?.id, newState)}
              onEditPlayback={() => setEditPbId(pb?.id)}
              pb={pb}
            ></Playback>
          );
        })}
      </div>
    </div>
  );
}
