import { createProjectRecord } from "../db/project";
import { createBladeRecord } from "../db/blade";
import { getProjectUsage } from "../query/project";
import { getBladeUsage } from "../query/blade";
import { BladeStatuses } from "../types/tractor";
import logger from "../utils/logger";

interface HistoryRecordBuffer {
  bladeUsage: BladeStatuses;
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

  if (!bladeUsage) return;

  let bladeStatus: keyof typeof historyBuffer.bladeUsage;
  for (bladeStatus in bladeUsage) {
    historyBuffer.bladeUsage[bladeStatus] += bladeUsage[bladeStatus];
  }
}

/**
 * Queries different data from Tractor and put it in the history buffer
 */
async function queryDataIntoBuffer(historyBuffer: HistoryRecordBuffer) {
  await storeProjectUsage(historyBuffer);
  await storeBladeUsage(historyBuffer);
  historyBuffer.queryCounter++;
  logger.info(
    `Storing queries in history buffer (count: ${historyBuffer.queryCounter})`
  );
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
  historyBuffer.bladeUsage = {
    nimby: 0,
    off: 0,
    busy: 0,
    free: 0,
    noFreeSlots: 0,
    bug: 0,
  };

  // Store a record for every project
  for (const [projectName, projectData] of Object.entries(
    historyBufferCopy.projectUsage
  )) {
    await createProjectRecord(
      projectName,
      Math.round(projectData / historyBufferCopy.queryCounter)
    );
  }

  const bladeUsage = historyBufferCopy.bladeUsage;

  let bladeStatus: keyof typeof historyBuffer.bladeUsage;
  for (bladeStatus in bladeUsage) {
    historyBufferCopy.bladeUsage[bladeStatus] = Math.round(
      bladeUsage[bladeStatus] / historyBufferCopy.queryCounter
    );
  }

  await createBladeRecord(historyBufferCopy.bladeUsage);
  logger.info("Buffers saved successfully!");
}

/**
 * Runs the provided function every full hour
 * From: https://stackoverflow.com/questions/12309019/javascript-how-to-do-something-every-full-hour/12309126
 */
const runEveryFullHours = (callbackFn: () => void) => {
  const hour = 60 * 60 * 1000;
  const currentDate = new Date();
  const firstCall =
    hour -
    (currentDate.getMinutes() * 60 + currentDate.getSeconds()) * 1000 -
    currentDate.getMilliseconds();

  setTimeout(() => {
    callbackFn();
    setInterval(callbackFn, hour);
  }, firstCall);
};

/**
 * Starts the data fetching interval for storing the history of different metrics
 * It samples data every queryInterval and store them every hour in the database
 * @param queryInterval the interval in ms between sample queries
 */
export function startDataRecord(queryInterval: number) {
  const historyBuffer: HistoryRecordBuffer = {
    bladeUsage: {
      nimby: 0,
      off: 0,
      busy: 0,
      free: 0,
      noFreeSlots: 0,
      bug: 0,
    },
    projectUsage: {},
    queryCounter: 0,
  };

  setInterval(() => queryDataIntoBuffer(historyBuffer), queryInterval);
  runEveryFullHours(() => storeHistoryBuffer(historyBuffer));
}
