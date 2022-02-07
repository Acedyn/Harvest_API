import { Application } from "express";

import { getBladeUsage } from "../query/blade";
import { getProjectUsage } from "../query/project";

export function getCurrentBladeUsage(app: Application) {
  app.get("/current/blade-usage", async (req, res) => {
    res.send(await getBladeUsage());
  });
}

export function getCurrentProjectUsage(app: Application) {
  app.get("/current/project-usage", async (req, res) => {
    res.send(await getProjectUsage());
  });
}
