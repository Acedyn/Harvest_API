import { Request } from "express";

export function getTimeRange(
  req: Request<{}, {}, {}, { start?: string; end?: string }>
) {
  let start: number = 0;
  if (req.query.start) {
    start = parseInt(req.query.start);
  }
  let end: number = Date.now();
  if (req.query.end) {
    end = parseInt(req.query.end);
  }
  return [start, end];
}
