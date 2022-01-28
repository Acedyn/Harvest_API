import express from 'express';

import { getProjectHistory, getBladeHistory } from './history';

const app = express();

// Start the routes
getProjectHistory(app);
getBladeHistory(app);

export function startRestServer(port: number) {
  app.listen(port, () => {
    return console.log(`Harvest is listening on port ${port}`);
  });
}
