import { Application } from "express";

import { getProjectNames } from "../db/project";
import { getProjectComputeTime } from "../db/project";
import { queryBlades } from "../query/blade";
import {
  getCommands,
  getJobs,
  getJobsFilteredByOwnerAndProject,
  getTasks,
} from "../query/jobs";
import { getRunningJobs } from "../query/project";
import { RequestQuery } from "../types/api";
import { Command, Job, Task } from "../types/tractor";
import { cacheResult } from "../utils/cache";
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

/*export function getProfileUsagePerProject(app: Application) {
  app.get("/info/profile-per-project", async (req, res) => {
    const rJobs = await getJobs({
      includeArchived: false,
      filter: "numactive > 0",
      fields: ["jid"],
    });

    const jobs: {
      [jid: string]: Job & {
        tasks: { [tid: string]: Task & { commands: Command[] } };
      };
    } = {};

    for (const job of rJobs.data.rows) {
      const tasks = await getTasks({
        filter: `jid=${job.jid}`,
        fields: ["tid"],
      });
      jobs[job.jid] = { ...job, tasks: {} };

      for (const task of tasks.data.rows) {
        const commands = await getCommands({
          filter: `jid=${job.jid} and tid=${task.tid}`,
          fields: ["cid"],
        });

        jobs[job.jid].tasks[task.tid] = {
          ...task,
          commands: commands.data.rows,
        };
      }
    }

    res.send(jobs);
  });
}*/

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
