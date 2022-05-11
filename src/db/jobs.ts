import { prisma } from "./client";
import { Project, Job, Task } from "@prisma/client";
import {LogRecordRequest} from "../types/api";

export async function getJobs(page: number, pageSize: number) {
  return await prisma.job.findMany({skip: page*pageSize, take: pageSize});
}

const createJobQueryMap: { [key: string]: Promise<Job> } = {}
// Create a job after making sure it does not already exists
export async function createJob(id: string, project: Project) {
  const queryKey = `${id}-${project.name}`
  if(!(queryKey in createJobQueryMap)) {
    createJobQueryMap[queryKey] = new Promise((resolve) => {
      prisma.job.upsert({
        where: {
          id_projectName: {
            id: id,
            projectName: project.name,
          },
        },
        update: {},
        create: {
          id: id,
          projectName: project.name,
        }
      }).then((newJob) => {
        resolve(newJob)
        delete createJobQueryMap[queryKey]
      }).catch((reason) => {
        console.log(reason)
        delete createJobQueryMap[queryKey]
      })
    })
  }

  return await createJobQueryMap[queryKey]
}

export async function getTasks(job: Job) {
  return await prisma.task.findMany({where: {jid: job.id}});
}

const createTaskQueryMap: { [key: string]: Promise<Task> } = {}
// Create a task after making sure it does not already exists
export async function createTask(id: string, job: Job) {
  const queryKey = `${id}-${job.id}`
  if(!(queryKey in createTaskQueryMap)) {
    createTaskQueryMap[queryKey] = new Promise((resolve) => {
      prisma.task.upsert({
        where: {
          id_jid_projectName: {
            id: id,
            jid: job.id,
            projectName: job.projectName,
          },
        },
        update: {},
        create: {
          id: id,
          jid: job.id,
          projectName: job.projectName
        }
      }).then((newTask) => {
        resolve(newTask)
        delete createTaskQueryMap[queryKey]
      }).catch((reason) => {
        console.log(reason)
        delete createJobQueryMap[queryKey]
      })
    })
  }

  return await createTaskQueryMap[queryKey]
}


export async function getLogRecords(task: Task) {
  return await prisma.logRecord.findMany({where: {task: task}});
}

// Create a log record
export async function createLogRecord(task: Task, data: LogRecordRequest) {
  return await prisma.logRecord.create({
    data: {
      message: data.message,
      file: data.file,
      artist: data.user,
      time: new Date(data.time),
      type: data.match.type,
      help: data.match.help,
      task: {
        connect: {
          id_jid_projectName: {
            id: task.id,
            jid: task.jid,
            projectName: task.projectName,
          }
        }
      }
    },
  });
}

