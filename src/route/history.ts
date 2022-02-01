import {Request, Response, Application } from 'express';

import { getProjectRecords } from '../db/project';
import { getBladeRecords } from '../db/blade';
import { getTimeRange } from "../utils/time";

export function getProjectHistory(app: Application) {
  app.get('/history/project-usage', async (req: Request<{}, {}, {}, {start?: string, end?: string}>, res: Response) => {
    const [start, end] = getTimeRange(req)
    res.send(await getProjectRecords(new Date(start), new Date(end)));
  });
}

export function getBladeHistory(app: Application) {
  app.get('/history/blade-usage', async (req: Request<{}, {}, {}, {start?: string, end?: string}>, res: Response) => {
    const [start, end] = getTimeRange(req)
    console.log(getBladeRecords())
    res.send(await getBladeRecords(new Date(start), new Date(end)));
  });
}
