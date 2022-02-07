import express from "express";
import cors from "cors";

import { getProjectHistory, getBladeHistory } from "./history";
import { getCurrentProjectUsage, getCurrentBladeUsage } from "./current";
import { getProjects, getComputeTime, getBlades } from "./info";

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

export function startRestServer(port: number) {
  app.listen(port, () => {
    return console.log(`Harvest is listening on port ${port}`);
  });
}
