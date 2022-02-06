import { RequestQuery } from "../types/api";

export function getTimeRange(
  req: RequestQuery<{ start?: string; end?: string }>
) {
  let start = 0;
  if (req.query.start) {
    start = parseInt(req.query.start);
  }

  let end: number = Date.now();
  if (req.query.end) {
    end = parseInt(req.query.end);
  }

  return [start, end];
}
