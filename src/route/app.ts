import express from "express";
import cors from "cors";

import { getProjectHistory, getBladeHistory } from "./history";
import { getCurrentProjectUsage, getCurrentBladeUsage } from "./current";
import {
  getProjects,
  getComputeTime,
  getBlades,
  getJobsPerOwner,
  getJobsPerProject,
} from "./info";
import { getGroups } from "./fog";
import logger from "../utils/logger";

const app = express();
app.use(cors());

// /history
getProjectHistory(app);
getBladeHistory(app);

// /current
getCurrentBladeUsage(app);
getCurrentProjectUsage(app);

// /info
getComputeTime(app);
getProjects(app);
getBlades(app);

getJobsPerOwner(app);
getJobsPerProject(app);

// /fog
getGroups(app);

export function startRestServer(port: number) {
  app.listen(port, () => {
    logger.info(`Server listening on port ${port}`);
  });
}
