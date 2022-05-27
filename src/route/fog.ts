import { Application } from "express";
import { cacheResult } from "../utils/cache";
import logger from "../utils/logger";
import { queryFogHosts, queryFogGroups } from "../query/fog"


export function getGroups(app: Application) {
  app.get("/fog/groups", async (req, res) => {
    try {
      const groups = await cacheResult(
        "/fog/groups",
        1000 * 60 * 60,
        queryFogGroups
      );

      res.send(groups);
    } catch (err) {
      const error = err as Error;
      logger.error(`Error when getting FOG groups: ${error.message}`);
      res.status(400).send({ route: "/fog/groups", error: error.message });
    }
  });
}

export function getHosts(app: Application) {
  app.get("/fog/hosts", async (req, res) => {
    try {
      const hosts = await cacheResult(
        "fog/hosts",
        1000 * 60 * 60,
        queryFogHosts
      );

      res.send(hosts);
    } catch(err) {
      const error = err as Error
      logger.error(`Error when getting FOG hosts: ${error.message}`);
      res.status(400).send({ route: "/fog/hosts", error: error.message});
    }
  })
}
