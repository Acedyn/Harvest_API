import {LogRecord} from "@prisma/client";
import { Application, Request, Response } from "express";
import { createJob, createTask, createLogRecord } from "../db/jobs";
import { createProject } from "../db/project";
import { LogRecordRequest } from "../types/api";

export function postLogRecord(app: Application) {
  app.post(
    "/logs/record",
    async (req: Request<{}, {}, LogRecordRequest[]>, res: Response) => {
      const logRecords: LogRecord[] = []
      req.body.forEach(async (record) => {
        const job = await createJob(record.jid, await createProject("toto"))
        const task = await createTask(record.tid, job)
        logRecords.push(await createLogRecord(task, record))
      })
      res.json(logRecords)
    }
  );
}
