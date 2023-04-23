import { Playback, AllowedParams, FxParam } from "../types/playback";

interface PlaybackListRes {
  playbacks: Playback[];
  active_ids: string[];
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
    const res = await fetch('/api/programmer', {method: 'DELETE'})
    const programmer = (await res.json()) as Playback;
    return programmer
}