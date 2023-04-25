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
  const res = await fetch("/api/programmer", {
    method: "PATCH",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  });
  const programmer = (await res.json()) as Playback;
  return programmer;
}

export async function clearProgrammer() {
  const res = await fetch("/api/programmer", { method: "DELETE" });
  const programmer = (await res.json()) as Playback;
  return programmer;
}

export async function sendBPM(bpm: number) {
  const data = {
    bpm,
  };
  const res = await fetch("/api/bpm", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  });
  return;
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
  return (await res.json()) as Playback;
}

export async function playPlayback(id: number, newstate: boolean) {
  const action = newstate ? "on" : "off";
  const res = await fetch(`/api/playback/${id}/${action}`, {
    method: "POST",
  });
  return (await res.json()) as number[];
}
