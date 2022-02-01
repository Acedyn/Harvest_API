import express from 'express';
import cors from 'cors';

import { getProjectHistory, getBladeHistory, } from './history';
import { getCurrentProjectUsage, getCurrentBladeUsage } from './current';
import { getProjects, getComputeTime } from './info';

const app = express();
app.use(cors());

// Register the routes
getProjectHistory(app);
getBladeHistory(app);
getCurrentBladeUsage(app);
getCurrentProjectUsage(app);
getComputeTime(app);
getProjects(app);

export function startRestServer(port: number) {
  app.listen(port, () => {
    return console.log(`Harvest is listening on port ${port}`);
  });
}
