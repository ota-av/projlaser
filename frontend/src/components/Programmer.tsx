import { getProgrammer, modifyProgrammer, clearProgrammer } from "../api/playback";

import {useState, useEffect} from "react"
import { Playback } from "../types/playback";

export function LayerButton({n}: {n: string}) {
    return (
        <button className="rounded p-2 m-1 bg-blue-400 hover:bg-blue-600 transition duration-100">{n}</button>
    )
}

export function Programmer({className}: {className?: string}) {
    const [prorammer, setProgrammer] = useState<Playback>();
    const [error, setError] = useState<string>();

    useEffect(() => {
        const load = async () => {
            try {
                setProgrammer(await getProgrammer())
            } catch (error: any) {
                if (error && error instanceof Error) {
                    setError((olderr) => {
                        return olderr + error.message + "\n";
                    })
                }

            }
        }
    }, []);

    const defaultClass = "bg-slate-200 h-40"

    return (
        <div className={className ? className + " " + defaultClass : defaultClass}>
          {error && <p className="bg-red-200 p-2">{error}</p>}
          Programmer
          <div>
            {["123", "1233"].map((layer) => <LayerButton n={layer} /> )}
          </div>
        </div>
    );
}