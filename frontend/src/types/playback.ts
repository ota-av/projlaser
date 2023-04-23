
export type AllowedParams = "opacity" | "hue" | "saturation" | "value" | "x" | "y" | "sizex" | "sizey" | "rotation" | "type";

export type FxFuncs = "static" | "sine" | "linear" | "flash";

export interface FxParam {
    value: number;
    func: FxFuncs;
    phase: number;
    speed: number;
    scale: number;
}

export interface Playback {
    layervalues: Record<string, Record<AllowedParams, FxParam>>;
    id: string;
    name: string;
    priority: number;
}