import {Request, Response, Application } from 'express';

import { getBladeUsage } from '../query/blade';
import { getProjectUsage } from '../query/project';

export function getCurrentBladeUsage(app: Application) {
  app.get('/stats/blade-status', async (req: Request, res: Response) => {
    res.send(await getBladeUsage());
  });
}

export function getCurrentProjectUsage(app: Application) {
  app.get('/stats/project-usage', async (req: Request, res: Response) => {
    res.send(await getProjectUsage());
  });
}
