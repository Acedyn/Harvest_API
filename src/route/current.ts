import { Application } from "express";

import { getBladeUsage } from "../query/blade";
import { getProjectUsage } from "../query/project";
import { cacheResult } from "../utils/cache";

export function getCurrentBladeUsage(app: Application) {
  app.get("/current/blade-usage", async (req, res) => {
    res.send(await cacheResult("/current/blade-usage", 5000, getBladeUsage));
  });
}

export function getCurrentProjectUsage(app: Application) {
  app.get("/current/project-usage", async (req, res) => {
    res.send(
      await cacheResult("/current/project-usage", 5000, getProjectUsage)
    );
  });
}
