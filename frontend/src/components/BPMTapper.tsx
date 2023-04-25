import { useEffect, useState } from "react";
import { sendBPM } from "../api/playback";

export function BPMTapper() {
  const [count, setCount] = useState(0);
  const [timeFirst, setTimeFirst] = useState(0);
  const [timePrev, setTimePrev] = useState(0);

  const [bpm, setBpm] = useState(0);

  const [onbeat, setOnBeat] = useState(false);

  const handleMouseDown = () => {
    const timeSeconds = new Date();
    const time = timeSeconds.getTime();

    //reset
    if (timePrev !== 0 && time - timePrev > 1000) {
      setCount(0);
      setTimePrev(time);
      return false;
    }
    if (count === 0) {
      setTimeFirst(time);
      setCount((c) => c + 1);
    } else {
      const bpmAvg = (60000 * count) / (time - timeFirst);
      let bpm = Math.round(bpmAvg * 100) / 100;
      setBpm(bpm);
      sendBPM(bpm);
      setCount((c) => c + 1);
      setTimePrev(time);
    }
  };

  useEffect(() => {
    const itime = (60 / bpm) * 1000;
    const i = setInterval(() => {
      setOnBeat(true);
      setTimeout(() => setOnBeat(false), 100);
    }, itime);

    return () => clearInterval(i);
  }, [bpm, timeFirst]);

  return (
    <button
      className={
        "rounded m-5 p-4 bg-blue-300 transition duration-50" +
        (onbeat ? " bg-red-300" : "")
      }
      onMouseDown={handleMouseDown}
    >
      Tap BPM {bpm}
    </button>
  );
}
