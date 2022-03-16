import axios from "axios";
import { Command, Job, Task } from "../types/tractor";
import { tractorAPIURL } from "../utils/tractor";
import { getAuthenticationTsid } from "./authentication";

type TractorSelectResponse<T> = {
  rc: number;
  msg: string;
  rows: T[];
};

const OWNER_EXCLUDE = [
  "3d4",
  "3D4",
  "josephhenry",
  "Olivier",
  "td",
  "td@artfx.fr",
  "root",
  "Joseph HENRY",
  "jhenry",
  "Joseph",
  "etudiant",
  "slambin@artfx.fr",
  "jhenry@artfx.fr",
  "oargentieri",
  "groeder",
  "slambin",
  "gfbnd,;",
];

const PROJECT_EXCLUDE = ["TD", "3D4", "default"];
const DEFAULT_OPTS = {
  fields: [],
  filter: "",
  includeArchived: true,
  limit: 10000,
};

type TractorSelectOptions = {
  includeArchived: boolean;
  filter: string;
  fields: string[];
  limit: number;
};

export async function tractorSelect<T>(
  entity: "Job" | "Task" | "Command",
  opts: Partial<TractorSelectOptions> = {}
) {
  const tsid = await getAuthenticationTsid();
  const options = { ...DEFAULT_OPTS, ...opts };
  const flds = options.fields.map((f) => `${entity}.${f}`).join(",");

  const req = await axios.get<TractorSelectResponse<T>>(
    tractorAPIURL(
      `db?q=tractorselect('${entity.toLowerCase()}', '${
        options.filter
      }', '${flds}', '', ${options.limit}, '${
        options.includeArchived ? "t" : "f"
      }', '')&tsid=${tsid}`
    )
  );

  return req;
}

export async function getJobs(opts: Partial<TractorSelectOptions> = {}) {
  return await tractorSelect<Job>("Job", opts);
}

export async function getJobsFilteredByOwnerAndProject(fields: string[] = []) {
  const jobs = await getJobs({ fields });

  return {
    ...jobs.data,
    rows: jobs.data.rows.filter(
      (j) =>
        !OWNER_EXCLUDE.includes(j.owner) &&
        !j.projects.some((p) => PROJECT_EXCLUDE.includes(p))
    ),
  };
}

export async function getTasks(opts: Partial<TractorSelectOptions> = {}) {
  return await tractorSelect<Task>("Task", opts);
}

export async function getCommands(opts: Partial<TractorSelectOptions> = {}) {
  return await tractorSelect<Command>("Command", opts);
}
