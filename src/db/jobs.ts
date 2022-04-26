import { prisma } from "./client";
import { Project, Job, Task } from "@prisma/client";
import {LogRecordRequest} from "../types/api";
import logger from "../utils/logger";

export async function getJobs(page: number, pageSize: number) {
  return await prisma.job.findMany({skip: page*pageSize, take: pageSize});
}

// Create a job after making sure it does not already exists
export async function createJob(name: string, project: Project) {
  const job = await prisma.job.findUnique({
    where: {
      name: name,
    },
  });

  // If the job already exists, just return it
  if (job !== null) {
    return job;
  }

  logger.info("Storing new job ID...");
  return await prisma.job.create({
    data: {
      name: name,
      project: {
        connect: {
          name: project.name,
        },
      },
    },
  });
}

export async function getTasks(job: Job) {
  return await prisma.task.findMany({where: {jobName: job.name}});
}

// Create a task after making sure it does not already exists
export async function createTask(name: string, job: Job) {
  const task = await prisma.task.findUnique({
    where: {
      name_jobName: {
        name: name,
        jobName: job.name,
      },
    },
  });

  // If the job already exists, just return it
  if (task !== null) {
    return task;
  }

  logger.info("Storing new task ID...");
  return await prisma.task.create({
    data: {
      name: name,
      job: {
        connect: {
          name: job.name,
        },
      },
    },
  });
}


export async function getLogRecords(task: Task) {
  return await prisma.logRecord.findMany({where: {task: task}});
}

// Create a log record
export async function createLogRecord(task: Task, data: LogRecordRequest) {
  return await prisma.logRecord.create({
    data: {
      ...data,
      time: new Date(data.time),
      task: {
        connect: {
          name_jobName: {
            name: task.name,
            jobName: task.jobName,
          },
        },
      },
    },
  });
}

