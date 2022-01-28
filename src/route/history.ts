import {Request, Response, Application } from 'express';

import { getProjectRecords, getProjectComputeTime } from '../db/project';
import { getBladeRecords } from '../db/blade';

function getTimeRange(req: Request<{}, {}, {}, {start?: string, end?: string}>) {
  let start: number = 0
  if(req.query.start) {
    start = parseInt(req.query.start)
  }
  let end: number = Date.now()
  if(req.query.end) {
    end = parseInt(req.query.end)
  }
  return [start, end]
}

export function getProjectHistory(app: Application) {
  app.get('/stats/projects-history', async (req: Request<{}, {}, {}, {start?: string, end?: string}>, res: Response) => {
    const [start, end] = getTimeRange(req)
    res.send(await getProjectRecords(new Date(start), new Date(end)));
  });
}

export function getBladeHistory(app: Application) {
  app.get('/graphics/blade-status', async (req: Request<{}, {}, {}, {start?: string, end?: string}>, res: Response) => {
    const [start, end] = getTimeRange(req)
    console.log(getBladeRecords())
    res.send(await getBladeRecords(new Date(start), new Date(end)));
  });
}

export function getTotalComputeTime(app: Application) {
  app.get('/stats/total-computetime', async (req: Request<{}, {}, {}, {start?: string, end?: string}>, res: Response) => {
    const [start, end] = getTimeRange(req)
    res.send(await getProjectComputeTime(new Date(start), new Date(end)));
  });
}
