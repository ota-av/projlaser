import {
  chaseEntryDelete,
  chaseEntryUpsert,
  createUpdateChase,
  deleteChase,
} from "../api/api";
import { Chase, ChaseEntry, Playback } from "../types/playback";

export function ChaseEntryEditor({
  pb_id,
  entry,
}: {
  pb_id: number;
  entry: ChaseEntry;
}) {
  return (
    <div className="my-1 border-t border-b py-1">
      Target pb id:
      <input
        type="number"
        className="mx-2 w-14 border-b border-gray-400 outline-none focus:border-gray-700 transition duration-100"
        value={entry.playback_id}
        onChange={(ev) =>
          chaseEntryUpsert(pb_id, {
            ...entry,
            playback_id: Number(ev.target.value),
          })
        }
      ></input>
      Start:
      <input
        type="number"
        className="mx-2 w-14 border-b border-gray-400 outline-none focus:border-gray-700 transition duration-100"
        value={entry.start}
        step={0.1}
        onChange={(ev) =>
          chaseEntryUpsert(pb_id, {
            ...entry,
            start: Number(ev.target.value),
          })
        }
      ></input>
      End:
      <input
        type="number"
        className="mx-2 w-14 border-b border-gray-400 outline-none focus:border-gray-700 transition duration-100"
        step={0.1}
        value={entry.end}
        onChange={(ev) =>
          chaseEntryUpsert(pb_id, {
            ...entry,
            end: Number(ev.target.value),
          })
        }
      ></input>
      <button
        className="p-1 mx-2 bg-red-300 hover:bg-red-400 rounded"
        onClick={() => chaseEntryDelete(pb_id, entry.id)}
      >
        Delete
      </button>
    </div>
  );
}

export function ChaseListing({
  pb_id,
  chase,
}: {
  pb_id: number;
  chase?: Chase;
}) {
  const newEntry: ChaseEntry = {
    start: 0,
    end: 1,
    id: chase ? chase.entries.length : 0,
  };

  if (!chase)
    return (
      <div>
        <p className="text-lg">Chase editor</p>
        <button
          className="p-1 bg-blue-300 hover:bg-blue-400 rounded"
          onClick={() =>
            createUpdateChase(pb_id, {
              duration: 1,
            })
          }
        >
          Create chase
        </button>
      </div>
    );
  return (
    <div>
      <p className="text-lg">Chase editor</p>
      <p>
        Duration:{" "}
        <input
          className="border-b border-gray-400 outline-none focus:border-gray-700 transition duration-100"
          type="number"
          value={chase.duration}
          onChange={(ev) =>
            createUpdateChase(pb_id, {
              duration: Number(ev.target.value),
            })
          }
        ></input>
      </p>
      {chase.entries.map((entry) => (
        <ChaseEntryEditor pb_id={pb_id} entry={entry}></ChaseEntryEditor>
      ))}
      <button
        className="p-1 my-2 bg-blue-300 hover:bg-blue-400 rounded"
        onClick={() => chaseEntryUpsert(pb_id, newEntry)}
      >
        New entry
      </button>
      <br></br>
      <button
        className="p-1 my-2 bg-red-300 hover:bg-red-400 rounded"
        onClick={() => deleteChase(pb_id)}
      >
        Delete chase
      </button>
    </div>
  );
}
