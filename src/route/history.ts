import { Application } from "express";

import { getProjectRecords } from "../db/project";
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
      const projectRecords = await getProjectRecords(
        new Date(start),
        new Date(end),
        req.query.project
      );
      const groupedProjectRecords: {
        [time: string]: { [name: string]: number };
      } = {};
      projectRecords.forEach((projectRecord) => {
        // We have to round the creation time to the closest hour to reduce the amount of records
        const roundDate = projectRecord.createdAt;
        roundDate.setHours(
          roundDate.getHours() + Math.round(roundDate.getMinutes() / 60)
        );
        roundDate.setMinutes(0, 0, 0);

        const index = roundDate.getTime().toString();
        if (!groupedProjectRecords[index]) {
          groupedProjectRecords[index] = {};
        }
        groupedProjectRecords[index][projectRecord.projectName] =
          projectRecord.usage;
      });

      const formattedProjectRecords: { [key: string]: number | Date }[] = [];
      for (const [key, value] of Object.entries(groupedProjectRecords)) {
        formattedProjectRecords.push({
          ...value,
          createdAt: new Date(parseInt(key)),
        });
      }
      res.send(formattedProjectRecords);
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
