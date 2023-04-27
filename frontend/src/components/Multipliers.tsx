import { updateMultipliers } from "../api/api";

export function Multipliers({
  multipliers
}: {
  multipliers: Record<string, number>;
}) {
  const onChange = updateMultipliers;

  return (
    <div>
      {Object.keys(multipliers).map((mid) => (
        <input
          type="number"
          className="w-14"
          min={0}
          max={1}
          step={0.05}
          value={multipliers[mid]}
          onChange={(ev) => {
            onChange({
              ...multipliers,
              [mid]: Number(ev.target.value),
            });
          }}
        ></input>
      ))}
    </div>
  );
}
