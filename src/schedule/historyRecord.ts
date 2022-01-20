import { createProjectRecord } from "../db/project";

export function startDataRecord(queryInterval: number, storeInterval: number) {
  setInterval(() => {createProjectRecord("TEST_PIPE", 4)}, queryInterval);
}
