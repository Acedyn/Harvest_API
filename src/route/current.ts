import {Request, Response, Application } from 'express';

import { getBladeUsage } from '../query/blade';
import { getProjectUsage } from '../query/project';

export function getCurrentBladeUsage(app: Application) {
  app.get('/current/blade-usage', async (req: Request, res: Response) => {
    res.send(await getBladeUsage());
  });
}

export function getCurrentProjectUsage(app: Application) {
  app.get('/current/project-usage', async (req: Request, res: Response) => {
    res.send(await getProjectUsage());
  });
}
