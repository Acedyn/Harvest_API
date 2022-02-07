import axios from "axios";
import { Blade } from "../types/tractor";

export async function getBladeUsage() {
  const bladesStatuses = await axios.get<{ blades: Blade[] }>(
    `${process.env.TRACTOR_URL}/monitor?q=blades`
  );

  let busyCount = 0;
  let freeCount = 0;
  let nimbyCount = 0;
  let offCount = 0;

  bladesStatuses.data.blades.forEach((blade) => {
    const lastPulse = new Date(blade.t * 1000);

    // The blade is busy
    if (blade.owners && blade.owners.length) {
      busyCount++;
      return;
    }

    // The blade has its nimby on
    if (blade.nimby) {
      nimbyCount++;
      return;
    }

    // The blade is in idle
    if (Date.now() - lastPulse.getTime() < 500000) {
      freeCount++;
      return;
    }

    // The blade is off
    offCount++;
  });

  return {
    busy: busyCount,
    free: freeCount,
    nimby: nimbyCount,
    off: offCount,
  };
}
