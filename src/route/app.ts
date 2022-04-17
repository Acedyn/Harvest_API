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
  getRunningJobsRoute,
} from "./info";
import { getGroups } from "./fog";
import logger from "../utils/logger";

const app = express();
app.use(cors());

/**
 * Initialize express routes for each category
 */
export function initializeRoutes() {
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

  getRunningJobsRoute(app);
  getJobsPerOwner(app);
  getJobsPerProject(app);

  // /fog
  getGroups(app);

  // Add route listing
  app.get("/", (req, res) => {
    type Route = { path: string };
    const layers = app._router.stack;
    const routes = layers
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .map((layer: { route: Route | undefined }) => layer.route)
      .filter((route: Route) => route !== undefined)
      .map((route: Route) => route.path);

    res.send({ routes });
  });
}

export function startRestServer(port: number) {
  app.listen(port, () => {
    logger.info(`Server listening on port ${port}`);
  });
}
