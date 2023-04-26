import { socket } from "../socket";
import { Playback, AllowedParams, FxParam } from "../types/playback";

interface PlaybackListRes {
  playbacks: Playback[];
  active_ids: number[];
}

export async function listPlaybacks() {
  const res = await fetch("/api/playbacks");
  const playbacks = (await res.json()) as PlaybackListRes;
  return playbacks;
}

export async function getLayers() {
  const res = await fetch("/api/layers");
  const layers = (await res.json()) as string[];
  return layers;
}

export async function getProgrammer() {
  const res = await fetch("/api/programmer");
  const programmer = (await res.json()) as Playback;
  return programmer;
}

export async function modifyProgrammer(
  layer: string,
  param: AllowedParams,
  value: FxParam
) {
  const data = {
    layer,
    param,
    value,
  };
  socket.emit("programmer", data);
}

export async function clearProgrammer() {
  const res = await fetch("/api/programmer", { method: "DELETE" });
}

export async function sendBPM(bpm: number) {
  socket.emit("bpm", { bpm });
}

export async function recordPlayback(id: number) {
  const data = {
    id,
  };
  const res = await fetch("/api/record", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  });
}

export async function playPlayback(id: number, newstate: boolean) {
  const action = newstate ? "on" : "off";
  socket.emit("playback_state", { id, action });
}

export async function getInfo() {
  const res = await fetch("/api/info");
  const info = (await res.json()) as { showname: string };
  return info;
}

export async function load(name: string) {
  const data = {
    name,
  };
  const res = await fetch("/api/load", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  });
}

export async function save(name: string) {
  const data = {
    name,
  };
  const res = await fetch("/api/save", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  });
}

export async function updatePlaybackMeta(id: number, props: Partial<Playback>) {
  const res = await fetch(`/api/playback/${id}/meta`, {
    method: "PATCH",
    body: JSON.stringify(props),
    headers: {
      "Content-Type": "application/json",
    },
  });
}
