import { getNoFreeSlots } from "../query/blade";
import { getProcessesQuery, killProcessesQuery } from "../utils/killprocess";

type ResultGoKillProcess = {
    NAME: string;
    RAM: number;
    PID: number;
  };
  
/**
 * clear blade in no free slots state
 */
 export async function clearNoFreeSlots() {
    const blades = await getNoFreeSlots()

    blades.forEach(async(b) => {
        const result = await getProcessesQuery(b.addr);
        const processesToKill = ["rez", "maya", "hrender", "kick", "vray"];

        processesToKill.forEach(async(p) => {
            const process:ResultGoKillProcess = result?.data.find((tp: { Name: string; })=> tp.Name.toLowerCase().includes(p));
            if (process) await killProcessesQuery(b.addr, process.PID);
        })
    })
  }

/**
 * 
 * startClearNoFreeSlots start and call ClearNoFreeSlots
 * @param queryInterval the interval in ms between sample queries
 */
export function startClearNoFreeSlots(queryInterval: number) {
    clearNoFreeSlots()
    setInterval(clearNoFreeSlots, queryInterval);
}
