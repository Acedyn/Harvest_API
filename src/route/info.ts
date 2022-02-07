import { Application } from "express";

import { getProjectNames } from "../db/project";
import { getProjectComputeTime } from "../db/project";
import { queryBlades } from "../query/blade";
import { RequestQuery } from "../types/api";
import { getTimeRange } from "../utils/time";

export function getProjects(app: Application) {
  app.get("/info/projects", async (req, res) => {
    res.send(await getProjectNames());
  });
}

export function getComputeTime(app: Application) {
  app.get(
    "/info/compute-time",
    async (
      req: RequestQuery<{ start?: string; end?: string; project?: string }>,
      res
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

export function getBlades(app: Application) {
  app.get("/info/blades", async (req, res) => {
    res.send((await queryBlades()).data);
  });
}
