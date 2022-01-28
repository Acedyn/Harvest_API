import {Request, Response, Application } from 'express';

import { getProjectRecords } from '../db/project';
import { getBladeRecords } from '../db/blade';

export function getProjectHistory(app: Application) {
  app.get('/history/project', async (req: Request, res: Response) => {
    res.send(await getProjectRecords());
  });
}

export function getBladeHistory(app: Application) {
  app.get('/history/blade', async (req: Request, res: Response) => {
    res.send(await getBladeRecords());
  });
}
