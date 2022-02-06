import { Request, Response, Application } from "express";

import { getProjectNames } from "../db/project";
import { getProjectComputeTime } from "../db/project";
import { RequestQuery } from "../types/api";
import { getTimeRange } from "../utils/time";

export function getProjects(app: Application) {
  app.get("/info/projects", async (req: Request, res: Response) => {
    res.send(await getProjectNames());
  });
}

export function getComputeTime(app: Application) {
  app.get(
    "/info/compute-time",
    async (
      req: RequestQuery<{ start?: string; end?: string; project?: string }>,
      res: Response
    ) => {
      const [start, end] = getTimeRange(req);
      const totalComputeTime = await getProjectComputeTime(
        new Date(start),
        new Date(end),
        req.query.project
      );
      res.send({
        hours: Math.floor(totalComputeTime.getTime() / 1000 / 60 / 60),
        minutes: totalComputeTime.getMinutes(),
      });
    }
  );
}
