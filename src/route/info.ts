import { Application } from "express";

import { getProjectNames } from "../db/project";
import { getProjectComputeTime } from "../db/project";
import { queryBlades } from "../query/blade";
import { getJobsFilteredByOwnerAndProject } from "../query/jobs";
import { getRunningJobs } from "../query/project";
import { RequestQuery } from "../types/api";
import { cacheResult } from "../utils/cache";
import { IGNORE_PROJECTS } from "../utils/constants";
import { getTimeRange } from "../utils/time";

export function getProjects(app: Application) {
  app.get("/info/projects", async (req, res) => {
    const projects = (await getProjectNames()).filter(
      (p) => !IGNORE_PROJECTS.includes(p)
    );
    res.send(projects);
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
    const response = await queryBlades();

    if (response) {
      res.send(response.data);
    } else {
      res.status(500);
    }
  });
}

export function getRunningJobsRoute(app: Application) {
  app.get("/info/running-jobs", async (req, res) => {
    const jobs = await getRunningJobs();
    res.send(jobs);
  });
}

function getCachedJobs() {
  return cacheResult("jobs", 1000 * 60 * 10, getJobsFilteredByOwnerAndProject);
}

export function getJobsPerOwner(app: Application) {
  app.get("/info/jobs-per-owner", async (req, res) => {
    const jobs = await getCachedJobs();
    const frequency: { [owner: string]: number } = {};

    for (const job of jobs.rows) {
      if (!frequency[job.owner]) {
        frequency[job.owner] = 0;
      }
      frequency[job.owner]++;
    }

    res.send(frequency);
  });
}

export function getJobsPerProject(app: Application) {
  app.get("/info/jobs-per-project", async (req, res) => {
    const jobs = await getCachedJobs();
    const frequency: { [project: string]: { jobs: number; tasks: number } } =
      {};

    for (const job of jobs.rows) {
      for (const project of job.projects) {
        if (!frequency[project]) {
          frequency[project] = { jobs: 0, tasks: 0 };
        }
        frequency[project].jobs++;
        frequency[project].tasks += job.numtasks;
      }
    }

    res.send(frequency);
  });
}
