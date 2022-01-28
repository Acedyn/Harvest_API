import express from 'express';

import { getProjectHistory, getBladeHistory } from './history';
import { getCurrentProjectUsage, getCurrentBladeUsage } from './active';

const app = express();

// Register the routes
getProjectHistory(app);
getBladeHistory(app);
getCurrentBladeUsage(app);
getCurrentProjectUsage(app);

export function startRestServer(port: number) {
  app.listen(port, () => {
    return console.log(`Harvest is listening on port ${port}`);
  });
}
