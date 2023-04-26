import { HTMLAttributes, PropsWithChildren, Fragment } from "react";
import {
  AllowedParams,
  FxParam,
  AllowedTypes,
  FxFuncs,
} from "../types/playback";

import { SketchPicker } from "react-color";

export const paramGroups = ["color", "pos", "type"] as const;

let hsl2hsv = (
  h: number,
  s: number,
  l: number,
  v = s * Math.min(l, 1 - l) + l
) => [h, v ? 2 - (2 * l) / v : 0, v];

let hsv2hsl = (
  h: number,
  s: number,
  v: number,
  l = v - (v * s) / 2,
  m = Math.min(l, 1 - l)
) => [h, m ? (v - l) / m : 0, l];

function Slider({
  value,
  className,
  ...props
}: HTMLAttributes<HTMLInputElement> & { value: number }) {
  return <input type="range"></input>;
}

function defaultParam(initial = 0) {
  const param: FxParam = {
    value: initial,
    func: "static",
    phase: 0,
    speed: 0,
    scale: 0,
    start: 0,
    end: 1,
  };

  return param;
}

function FxAdjust({
  param,
  onChange,
}: {
  param: FxParam;
  onChange: (value: FxParam) => void;
}) {
  return (
    <Fragment>
      <p className="m-1">Func</p>
      <select
        value={param.func}
        onChange={(ev) => {
          onChange({
            ...param,
            func: ev.target.value as FxFuncs,
          });
        }}
      >
        <option>static</option>
        <option>flash</option>
        <option>sine</option>
        <option>cos</option>
        <option>linear</option>
        <option>square</option>
        <option>cubic</option>
        <option>sqrt</option>
        <option>cbrt</option>
      </select>
      <p className="m-1">Phase</p>
      <input
        type="number"
        className="w-14"
        min={0}
        max={1}
        step={0.05}
        value={param.phase}
        onChange={(ev) => {
          onChange({
            ...param,
            phase: Number(ev.target.value),
          });
        }}
      ></input>
      <p className="m-1">Speed</p>
      <input
        type="number"
        className="w-14"
        min={-4}
        max={4}
        step={0.125}
        value={param.speed}
        onChange={(ev) => {
          onChange({
            ...param,
            speed: Number(ev.target.value),
          });
        }}
      ></input>
      <p className="m-1">Scale</p>
      <input
        type="number"
        className="w-14"
        min={0}
        max={1}
        step={0.05}
        value={param.scale}
        onChange={(ev) => {
          onChange({
            ...param,
            scale: Number(ev.target.value),
          });
        }}
      ></input>
      <p className="m-1">Start</p>
      <input
        type="number"
        className="w-14"
        min={0}
        max={1}
        step={0.125}
        value={param.start}
        onChange={(ev) => {
          onChange({
            ...param,
            start: Number(ev.target.value),
          });
        }}
      ></input>
      <p className="m-1">End</p>
      <input
        type="number"
        className="w-14"
        min={0}
        max={1}
        step={0.125}
        value={param.end}
        onChange={(ev) => {
          onChange({
            ...param,
            end: Number(ev.target.value),
          });
        }}
      ></input>
    </Fragment>
  );
}

export function OpacityGroup({
  currentParams,
  onChange,
}: {
  currentParams: Record<AllowedParams, FxParam> & Record<"type", AllowedTypes>;
  onChange: (param: AllowedParams, value: FxParam) => void;
}) {
  const dimParam =
    currentParams["opacity"] !== undefined
      ? currentParams["opacity"]
      : defaultParam();

  const isModified = currentParams["opacity"] !== undefined;

  return (
    <div
      className={
        "flex flex-row border border-slate-300 p-2 rounded" +
        (isModified ? " bg-blue-300" : "")
      }
    >
      <div className="flex flex-col items-center">
        <input
          type="range"
          className="w-10 h-80 "
          // @ts-ignore
          orient="vertical"
          min={0}
          max={1}
          step={0.01}
          value={dimParam.value}
          onChange={(ev) => {
            onChange("opacity", {
              ...dimParam,
              value: Number(ev.target.value),
            });
          }}
        ></input>
        <input
          className="w-12 mt-2"
          type="number"
          min={0}
          max={1}
          step={0.1}
          value={dimParam.value}
          onChange={(ev) => {
            onChange("opacity", {
              ...dimParam,
              value: Number(ev.target.value),
            });
          }}
        ></input>
        <p className="mb-0">Dimmer</p>
      </div>
      <div className="flex flex-col">
        <FxAdjust
          param={dimParam}
          onChange={(newParam) => onChange("opacity", newParam)}
        />
      </div>
    </div>
  );
}

export function ColorGroup({
  currentParams,
  onChange,
}: {
  currentParams: Record<AllowedParams, FxParam> & Record<"type", AllowedTypes>;
  onChange: (param: AllowedParams, value: FxParam) => void;
}) {
  const hParam =
    currentParams["hue"] !== undefined ? currentParams["hue"] : defaultParam(1);

  const sParam =
    currentParams["saturation"] !== undefined
      ? currentParams["saturation"]
      : defaultParam(1);

  const vParam =
    currentParams["value"] !== undefined
      ? currentParams["value"]
      : defaultParam(1);

  const onChangeColor = (color: {
    hsl: { h: number; s: number; l: number };
  }) => {
    const hsvColor = hsl2hsv(color.hsl.h / 360, color.hsl.s, color.hsl.l);
    onChange("hue", { ...hParam, value: hsvColor[0] });
    onChange("saturation", { ...sParam, value: hsvColor[1] });
    onChange("value", { ...vParam, value: hsvColor[2] });
  };

  const hslColor = hsv2hsl(hParam.value, sParam.value, vParam.value);

  return (
    <div className="flex flex-1 flex-col items-center">
      <SketchPicker
        color={{ h: hslColor[0] * 360, s: hslColor[1], l: hslColor[2] }}
        onChange={onChangeColor}
      ></SketchPicker>
      <p className="mt-auto mb-0">Color</p>
    </div>
  );
}

export function PosGroup({
  currentParams,
  onChange,
}: {
  currentParams: Record<AllowedParams, FxParam> & Record<"type", AllowedTypes>;
  onChange: (param: AllowedParams, value: FxParam) => void;
}) {
  const xParam =
    currentParams["x"] !== undefined ? currentParams["x"] : defaultParam(0.5);

  const yParam =
    currentParams["y"] !== undefined ? currentParams["y"] : defaultParam(0.5);

  const sizexParam =
    currentParams["sizex"] !== undefined
      ? currentParams["sizex"]
      : defaultParam(0.5);

  const rotParam =
    currentParams["rotation"] !== undefined
      ? currentParams["rotation"]
      : defaultParam(0);

  const sizeyParam =
    currentParams["sizey"] !== undefined
      ? currentParams["sizey"]
      : defaultParam(0.5);

  function isModified(x: AllowedParams) {
    return currentParams[x] !== undefined;
  }

  return (
    <div className="flex">
      <div>
        <div
          className={
            "mx-2 items-center border border-slate-300 p-1 rounded" +
            (isModified("x") ? " bg-blue-300" : "")
          }
        >
          <div className="flex flex-row items-center m-1">
            <p className="mr-1">Pos x</p>
            <input
              type="range"
              className="w-80 mx-1"
              min={0}
              max={1}
              step={0.01}
              value={xParam.value}
              onChange={(ev) => {
                onChange("x", { ...xParam, value: Number(ev.target.value) });
              }}
            ></input>
            <input
              className="w-12 mx-1"
              type="number"
              min={0}
              max={1}
              step={0.1}
              value={xParam.value}
              onChange={(ev) => {
                onChange("x", {
                  ...xParam,
                  value: Number(ev.target.value),
                });
              }}
            ></input>
          </div>
          <div className="flex flex-row items-center m-1">
            <FxAdjust
              param={xParam}
              onChange={(newParam) => onChange("x", newParam)}
            />
          </div>
        </div>

        <div
          className={
            "mx-2 items-center border border-slate-300 p-1 rounded" +
            (isModified("sizex") ? " bg-blue-300" : "")
          }
        >
          <div className="flex flex-row items-center m-1">
            <p className="mr-1">Size x</p>
            <input
              type="range"
              className="w-80 mx-1"
              min={0}
              max={1}
              step={0.01}
              value={sizexParam.value}
              onChange={(ev) => {
                onChange("sizex", {
                  ...sizexParam,
                  value: Number(ev.target.value),
                });
              }}
            ></input>
            <input
              className="w-12 mx-1"
              type="number"
              min={0}
              max={1}
              step={0.1}
              value={sizexParam.value}
              onChange={(ev) => {
                onChange("sizex", {
                  ...sizexParam,
                  value: Number(ev.target.value),
                });
              }}
            ></input>
          </div>
          <div className="flex flex-row items-center m-1">
            <FxAdjust
              param={sizexParam}
              onChange={(newParam) => onChange("sizex", newParam)}
            />
          </div>
        </div>
        <div
          className={
            "mx-2 items-center border border-slate-300 p-1 rounded" +
            (isModified("rotation") ? " bg-blue-300" : "")
          }
        >
          <div className="flex flex-row items-center m-1">
            <p className="mr-1">Rotation</p>
            <input
              type="range"
              className="w-80 mx-1"
              min={0}
              max={1}
              step={0.01}
              value={rotParam.value}
              onChange={(ev) => {
                onChange("rotation", {
                  ...rotParam,
                  value: Number(ev.target.value),
                });
              }}
            ></input>
            <input
              className="w-12 mx-1"
              type="number"
              min={0}
              max={1}
              step={0.1}
              value={rotParam.value}
              onChange={(ev) => {
                onChange("rotation", {
                  ...rotParam,
                  value: Number(ev.target.value),
                });
              }}
            ></input>
          </div>
          <div className="flex flex-row items-center m-1">
            <FxAdjust
              param={rotParam}
              onChange={(newParam) => onChange("rotation", newParam)}
            />
          </div>
        </div>
      </div>

      <div
        className={
          "flex flex-row border border-slate-300 p-2 rounded" +
          (isModified("y") ? " bg-blue-300" : "")
        }
      >
        <div className="flex flex-col">
          <input
            type="range"
            className="w-12 h-80"
            // @ts-ignore
            orient="vertical"
            min={0}
            max={1}
            step={0.01}
            value={yParam.value}
            onChange={(ev) => {
              onChange("y", { ...yParam, value: Number(ev.target.value) });
            }}
          ></input>
          <input
            className="w-12 mt-2"
            type="number"
            min={0}
            max={1}
            step={0.1}
            value={yParam.value}
            onChange={(ev) => {
              onChange("y", {
                ...yParam,
                value: Number(ev.target.value),
              });
            }}
          ></input>
          <p>Pos y</p>
        </div>
        <div className="flex flex-col">
          <FxAdjust
            param={yParam}
            onChange={(newParam) => onChange("y", newParam)}
          />
        </div>
      </div>
      <div
        className={
          "flex flex-row mx-2 border border-slate-300 p-2 rounded" +
          (isModified("sizey") ? " bg-blue-300" : "")
        }
      >
        <div className="flex flex-col">
          <input
            type="range"
            className="w-12 h-80 "
            // @ts-ignore
            orient="vertical"
            min={0}
            max={1}
            step={0.01}
            value={sizeyParam.value}
            onChange={(ev) => {
              onChange("sizey", {
                ...sizeyParam,
                value: Number(ev.target.value),
              });
            }}
          ></input>
          <input
            className="w-12 mt-2"
            type="number"
            min={0}
            max={1}
            step={0.1}
            value={sizeyParam.value}
            onChange={(ev) => {
              onChange("sizey", {
                ...sizeyParam,
                value: Number(ev.target.value),
              });
            }}
          ></input>
          Size y
        </div>

        <div className="flex flex-col">
          <FxAdjust
            param={sizeyParam}
            onChange={(newParam) => onChange("sizey", newParam)}
          />
        </div>
      </div>
    </div>
  );
}
