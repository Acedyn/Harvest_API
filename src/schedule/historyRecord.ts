import { createProjectRecord } from "../db/project";
import { createBladeRecord } from "../db/blade";

export function startDataRecord(queryInterval: number, storeInterval: number) {
  setInterval(() => {createProjectRecord("TEST_PIPE", 4)}, queryInterval);
  // setInterval(() => {createBladeRecord({busy: 2, free: 5, nimby: 29, off: 21})}, queryInterval);
}
