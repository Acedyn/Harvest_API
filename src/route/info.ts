import { Application } from "express";

import { getProjectNames } from "../db/project";
import { getProjectComputeTime } from "../db/project";
import { queryBlades } from "../query/blade";
import { getJobsFilteredByOwnerAndProject } from "../query/jobs";
import { getRunningJobs } from "../query/project";
import { RequestQuery } from "../types/api";
import { Job } from "../types/tractor";
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

function numberOfJobsPerUser(jobs: Job[]) {
  const frequency: { [owner: string]: number } = {};

  for (const job of jobs) {
    if (!frequency[job.owner]) {
      frequency[job.owner] = 0;
    }
    frequency[job.owner]++;
  }

  return frequency;
}

export function getJobsPerOwner(app: Application) {
  app.get("/info/jobs-per-owner", async (req, res) => {
    const jobs = await getCachedJobs();
    res.send(numberOfJobsPerUser(jobs.rows));
  });
}

export function getJobsPerOwnerHistory(app: Application) {
  app.get(
    "/history/jobs-per-owner",
    async (req: RequestQuery<{ resolution?: string }>, res) => {
      const jobs = (await getCachedJobs()).rows;
      const slices = req.query.resolution ? parseInt(req.query.resolution) : 50;

      const spoolTimes = jobs.map((job) => new Date(job.spooltime).getTime());
      const minTime = Math.min(...spoolTimes);
      const maxTime = Math.max(...spoolTimes);
      const timeSlice = Math.round((maxTime - minTime) / slices);

      const history: { [date: string]: { [owner: string]: number } } = {};

      for (const job of jobs) {
        const dateRounded =
          Math.floor(
            (new Date(job.spooltime).getTime() - minTime) / timeSlice
          ) *
            timeSlice +
          minTime;

        if (!history[dateRounded]) {
          history[dateRounded] = {};
        }

        if (!history[dateRounded][job.owner]) {
          history[dateRounded][job.owner] = 0;
        }

        history[dateRounded][job.owner]++;
      }

      const dateSorted = Object.keys(history).map((k) => parseInt(k));
      dateSorted.sort((a, b) => a - b);

      const accumulate: { [owner: string]: number } = {};
      for (let i = 0; i < dateSorted.length; i++) {
        for (const [owner, njobs] of Object.entries(history[dateSorted[i]])) {
          if (!accumulate[owner]) accumulate[owner] = 0;

          accumulate[owner] += njobs;
          history[dateSorted[i]][owner] = accumulate[owner];
        }

        for (const owner of Object.keys(accumulate)) {
          if (!history[dateSorted[i]][owner]) {
            history[dateSorted[i]][owner] = accumulate[owner];
          }
        }
      }

      res.send(
        dateSorted.map((key: number) => ({
          ...history[key],
          createdAt: new Date(key),
        }))
      );
    }
  );
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
