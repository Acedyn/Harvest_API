import axios from "axios";
import { Blade } from "../types/tractor";
import { tractorAPIURL } from "../utils/tractor";

/**
 * Queries Tractor about blades
 */
export function queryBlades() {
  return axios.get<{ blades: Blade[] }>(tractorAPIURL("monitor?q=blades"));
}

export async function getBladeUsage() {
  const bladesResponse = await queryBlades();

  let busyCount = 0;
  let freeCount = 0;
  let nimbyCount = 0;
  let offCount = 0;
  let noFreeSlotsCount = 0;

  bladesResponse.data.blades.forEach((blade) => {
    const lastPulse = new Date(blade.t * 1000);

    // The blade is busy
    if (blade.owners && blade.owners.length) {
      busyCount++;
      return;
    }

    // The blade has its nimby on
    if (blade.nimby.length > 0) {
      nimbyCount++;
      return;
    }

    // The blade is in idle
    if (Date.now() - lastPulse.getTime() < 500000) {
      if (blade.note === "no free slots (1)") {
        noFreeSlotsCount++;
      } else {
        freeCount++;
      }
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
    noFreeSlots: noFreeSlotsCount,
  };
}
