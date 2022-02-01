import { createProjectRecord } from "../db/project";
import { createBladeRecord } from "../db/blade";
import { getProjectUsage } from "../query/project";
import { getBladeUsage } from "../query/blade";

interface HistoryRecordBuffer {
  bladeUsage: {
    busy: number,
    off: number,
    nimby: number,
    free: number,
  },
  projectUsage: {
    [name: string]: number
  },
  queryCounter: number,
}


export function startDataRecord(queryInterval: number, storeInterval: number) {
  const historyBuffer: HistoryRecordBuffer = {
    bladeUsage: {
      nimby: 0,
      off: 0,
      busy: 0,
      free: 0,
    },
    projectUsage: {},
    queryCounter: 0
  }

  setInterval(async () => {
    for (const [projectName, projectData] of Object.entries(await getProjectUsage())) {
      if(!(projectName in historyBuffer.projectUsage)) {
        historyBuffer.projectUsage[projectName] = 0
      }
      historyBuffer.projectUsage[projectName] += projectData
    }
    let bladeStatus: keyof typeof historyBuffer.bladeUsage
    const bladeUsage = await getBladeUsage()
    for (bladeStatus in bladeUsage) {
      historyBuffer.bladeUsage[bladeStatus] += bladeUsage[bladeStatus]
    }
    historyBuffer.queryCounter++;
  }, queryInterval);


  setInterval(async () => {
    const historyBufferCopy: HistoryRecordBuffer = JSON.parse(JSON.stringify(historyBuffer))
    historyBuffer.queryCounter = 0
    historyBuffer.projectUsage = {}
    historyBuffer.bladeUsage = {nimby: 0, off: 0, busy: 0, free: 0}

    if(!historyBufferCopy.queryCounter) {
      return
    }

    for (const [projectName, projectData] of Object.entries(historyBufferCopy.projectUsage)) {
      await createProjectRecord(projectName, projectData / historyBufferCopy.queryCounter);
    }

    let bladeStatus: keyof typeof historyBuffer.bladeUsage
    const bladeUsage = historyBufferCopy.bladeUsage
    for (bladeStatus in bladeUsage) {
      historyBufferCopy.bladeUsage[bladeStatus] = bladeUsage[bladeStatus] / historyBufferCopy.queryCounter
    }
    await createBladeRecord(historyBufferCopy.bladeUsage);
  }, storeInterval);
}
