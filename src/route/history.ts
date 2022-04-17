import { Application } from "express";

import { gatherProjectUsageHistory } from "../db/project";
import { getBladeRecords } from "../db/blade";
import { getTimeRange } from "../utils/time";
import { RequestQuery } from "../types/api";

export function getProjectHistory(app: Application) {
  app.get(
    "/history/project-usage",
    async (
      req: RequestQuery<{ start?: string; end?: string; project?: string }>,
      res
    ) => {
      const [start, end] = getTimeRange(req);
      res.send(
        await gatherProjectUsageHistory(
          new Date(start),
          new Date(end),
          req.query.project
        )
      );
    }
  );
}

export function getBladeHistory(app: Application) {
  app.get(
    "/history/blade-usage",
    async (req: RequestQuery<{ start?: string; end?: string }>, res) => {
      const [start, end] = getTimeRange(req);
      res.send(await getBladeRecords(new Date(start), new Date(end)));
    }
  );
}
