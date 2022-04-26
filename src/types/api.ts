import { Request } from "express";
import { Query } from "express-serve-static-core";

export type RequestQuery<Q extends Query> = Request<
  unknown,
  unknown,
  unknown,
  Q
>;

export interface LogRecordRequest {
  message: string,
  time: number,
  file: string,
  user: string,
  tid: string,
  jid: string,
  type: string,
  help: string,
}
