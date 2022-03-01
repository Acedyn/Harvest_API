import axios from "axios";
import { tractorAPIURL } from "../utils/tractor";
import { getAuthenticationTsid } from "./authentication";

async function createRunningJobFilter(filterName = "running_jobs") {
  const filterFullName = `${filterName}.joblist`;
  const tsid = await getAuthenticationTsid();

  const filterData = {
    Filtername: filterName,
    Mode: "All",
    Rules: [
      {
        calls: "jobMatchState",
        data: null,
        mode: "Active",
        polarity: "is",
        title: "State",
      },
    ],
  };

  const queryUrl = tractorAPIURL(
    `monitor?q=putfilter&user=${process.env.TRACTOR_LOGIN}&key=${filterFullName}&tsid=${tsid}`
  );
  await axios.post(new URL(queryUrl, process.env.TRACTOR_URL).href, filterData);
  return filterFullName;
}

type RunningJobs = {
  users: {
    [user: string]: {
      [jid: string]: {
        data: {
          projects: string[];
          nTasks: number[];
          user: string;
        };
      };
    };
  };
};

export async function getRunningJobs() {
  const runningJobsFilter = await createRunningJobFilter();
  const tsid = await getAuthenticationTsid();

  const response = await axios.get<RunningJobs>(
    tractorAPIURL(
      `monitor?q=jobs&metadata=0&filter=${runningJobsFilter}&tsid=${tsid}`
    )
  );

  return Object.values(response.data.users)
    .map((user) => Object.values(user).map((job) => job.data))
    .flat();
}

/**
 * Returns a dictionnary with the number of tasks per project
 */
export async function getProjectUsage() {
  const runningJobs = await getRunningJobs();

  const projectUsage: { [project: string]: number } = {};

  runningJobs.forEach((runningJob) => {
    const taskCount = runningJob.nTasks[1];
    runningJob.projects.forEach((project: string) => {
      projectUsage[project] =
        project in projectUsage ? taskCount + projectUsage[project] : taskCount;
    });
  });

  return projectUsage;
}
