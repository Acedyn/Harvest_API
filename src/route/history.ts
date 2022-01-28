import {Request, Response, Application } from 'express';

import { getProjectRecords } from '../db/project';
import { getBladeRecords } from '../db/blade';

export function getProjectHistory(app: Application) {
  app.get('/stats/projects-history', async (req: Request<{}, {}, {}, {start: string, end: string}>, res: Response) => {
    let start: number = 0
    if(req.query.start) {
      start = parseInt(req.query.start)
    }
    let end: number = Date.now()
    if(req.query.end) {
      end = parseInt(req.query.end)
    }
    res.send(await getProjectRecords(new Date(start), new Date(end)));
  });
}

export function getBladeHistory(app: Application) {
  app.get('/stats/farm-history/hours', async (req: Request<{}, {}, {}, {start?: string, end?: string}>, res: Response) => {
    let start: number = 0
    if(req.query.start) {
      start = parseInt(req.query.start)
    }
    let end: number = Date.now()
    if(req.query.end) {
      end = parseInt(req.query.end)
    }
    res.send(await getBladeRecords(new Date(start), new Date(end)));
  });
}
