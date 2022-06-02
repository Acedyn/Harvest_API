import { Blade } from "../types/tractor";
import { BUG_PROFILES } from "../utils/constants";
import { tractorQuery } from "../utils/tractor";

/**
 * Queries Tractor about blades
 */
export function queryBlades() {
  return tractorQuery<{ blades: Blade[] }>("monitor?q=blades");
}

export async function getNoFreeSlots() {
  const bladesResponse = await queryBlades();

  if (!bladesResponse) {
    return [];
  }

  const noFreeSlotBlades: Blade[] = [];

  bladesResponse.data.blades.forEach((blade: Blade) => {
    const lastPulse = new Date(blade.t * 1000);

    // Exclude all busy blade
    if (blade.owners && blade.owners.length) {
      return;
    }

    // blade is active
    if (Date.now() - lastPulse.getTime() < 500000) {
      if (blade.note !== "no free slots (1)") return;
      noFreeSlotBlades.push(blade);
      return;
    }
  });
  return noFreeSlotBlades;
}

export async function getBladeUsage() {
  const bladesResponse = await queryBlades();

  if (!bladesResponse) {
    return undefined;
  }

  let busyCount = 0;
  let freeCount = 0;
  let nimbyCount = 0;
  let offCount = 0;
  let noFreeSlotsCount = 0;
  let bugCount = 0;

  for (const blade of bladesResponse.data.blades) {
    // It's in a bug pool so not usable
    if (
      BUG_PROFILES.includes(blade.profile) ||
      blade.note.startsWith("MinDisk")
    ) {
      bugCount++;
      continue;
    }

    const lastPulse = new Date(blade.t * 1000);

    // The blade is busy
    if (blade.owners && blade.owners.length) {
      busyCount++;
      continue;
    }

    // The blade is active
    if (Date.now() - lastPulse.getTime() < 500000) {
      if (blade.note === "no free slots (1)") {
        noFreeSlotsCount++;
        continue;
      }

      // It's not in nimby
      if (blade.nimby.length === 0) {
        freeCount++;
        continue;
      }
    } else {
      // It's off
      offCount++;
      continue;
    }

    // The blade has its nimby on
    if (blade.nimby.length > 0) {
      nimbyCount++;
      continue;
    }
  }

  return {
    busy: busyCount,
    free: freeCount,
    nimby: nimbyCount,
    off: offCount,
    noFreeSlots: noFreeSlotsCount,
    bug: bugCount,
  };
}
