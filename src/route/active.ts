import {Request, Response, Application } from 'express';

import { getBladeUsage } from '../query/blade';
import { getProjectUsage } from '../query/project';

export function getCurrentBladeUsage(app: Application) {
  app.get('/stats/blades-status', async (req: Request, res: Response) => {
    const bladeUsage = []
    for(const [bladeStatus, bladeData] of Object.entries(await getBladeUsage())) {
      bladeUsage.push({
        name: bladeStatus,
        value: bladeData,
      })
    }
    res.send(bladeUsage);
  });
}

export function getCurrentProjectUsage(app: Application) {
  app.get('/stats/projects-usage', async (req: Request, res: Response) => {
    const projectUsage = []
    for(const [projectName, projectData] of Object.entries(await getProjectUsage())) {
      projectUsage.push({
        name: projectName,
        value: projectData
      })
    }
    res.send(projectUsage);
  });
}
