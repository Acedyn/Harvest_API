import { Request } from "express";
import { Query } from "express-serve-static-core";

export type RequestQuery<Q extends Query> = Request<
  unknown,
  unknown,
  unknown,
  Q
>;
