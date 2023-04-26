export type AllowedParams =
  | "opacity"
  | "hue"
  | "saturation"
  | "value"
  | "x"
  | "y"
  | "sizex"
  | "sizey"
  | "rotation";

export type AllowedTypes = "rect" | "tri" | "star" | "circ";

export type FxFuncs =
  | "static"
  | "sine"
  | "linear"
  | "flash"
  | "square"
  | "cubic"
  | "cos"
  | "sqrt"
  | "cbrt";

export interface FxParam {
  value: number;
  func: FxFuncs;
  phase: number;
  speed: number;
  scale: number;
  start: number;
  end: number;
}

export interface Playback {
  layervalues: Record<
    string,
    Record<AllowedParams, FxParam> & Record<"type", AllowedTypes>
  >;
  id: number;
  name: string;
  priority: number;
  key: "flash" | "toggle";
  sync: boolean;
  duration: number;
}
