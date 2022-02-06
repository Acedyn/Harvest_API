import { createProjectRecord } from "../db/project";
import { createBladeRecord } from "../db/blade";
import { getProjectUsage } from "../query/project";
import { getBladeUsage } from "../query/blade";

interface HistoryRecordBuffer {
  bladeUsage: {
    busy: number;
    off: number;
    nimby: number;
    free: number;
  };
  projectUsage: {
    [name: string]: number;
  };
  queryCounter: number;
}

async function storeProjectUsage(historyBuffer: HistoryRecordBuffer) {
  const projectUsage = await getProjectUsage();

  for (const [projectName, projectData] of Object.entries(projectUsage)) {
    // Defaults to 0
    if (!(projectName in historyBuffer.projectUsage)) {
      historyBuffer.projectUsage[projectName] = 0;
    }

    historyBuffer.projectUsage[projectName] += projectData;
  }
}

async function storeBladeUsage(historyBuffer: HistoryRecordBuffer) {
  const bladeUsage = await getBladeUsage();

  let bladeStatus: keyof typeof historyBuffer.bladeUsage;
  for (bladeStatus in bladeUsage) {
    historyBuffer.bladeUsage[bladeStatus] += bladeUsage[bladeStatus];
  }
}

/**
 * Queries different data from Tractor and put it in the history buffer
 */
async function queryDataIntoBuffer(historyBuffer: HistoryRecordBuffer) {
  storeProjectUsage(historyBuffer);
  storeBladeUsage(historyBuffer);
  historyBuffer.queryCounter++;
}

/**
 * Stores the history buffer by averaging values over the number of requests made
 */
async function storeHistoryBuffer(historyBuffer: HistoryRecordBuffer) {
  if (historyBuffer.queryCounter <= 0) {
    return;
  }

  const historyBufferCopy: HistoryRecordBuffer = JSON.parse(
    JSON.stringify(historyBuffer)
  );

  historyBuffer.queryCounter = 0;
  historyBuffer.projectUsage = {};
  historyBuffer.bladeUsage = { nimby: 0, off: 0, busy: 0, free: 0 };

  // Store a record for every project
  for (const [projectName, projectData] of Object.entries(
    historyBufferCopy.projectUsage
  )) {
    await createProjectRecord(
      projectName,
      projectData / historyBufferCopy.queryCounter
    );
  }

  const bladeUsage = historyBufferCopy.bladeUsage;

  let bladeStatus: keyof typeof historyBuffer.bladeUsage;
  for (bladeStatus in bladeUsage) {
    historyBufferCopy.bladeUsage[bladeStatus] =
      bladeUsage[bladeStatus] / historyBufferCopy.queryCounter;
  }

  await createBladeRecord(historyBufferCopy.bladeUsage);
}

/**
 * Starts the data fetching interval for storing the history of different metrics
 * It samples data every queryInterval and store them every storeInterval in the database
 * @param queryInterval the interval in ms between sample queries
 * @param storeInterval the interval in ms between store operations (it averages values over that period)
 */
export function startDataRecord(queryInterval: number, storeInterval: number) {
  const historyBuffer: HistoryRecordBuffer = {
    bladeUsage: {
      nimby: 0,
      off: 0,
      busy: 0,
      free: 0,
    },
    projectUsage: {},
    queryCounter: 0,
  };

  setInterval(() => queryDataIntoBuffer(historyBuffer), queryInterval);
  setInterval(() => storeHistoryBuffer(historyBuffer), storeInterval);
}
