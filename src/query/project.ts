import axios from "axios";
import { getAuthentificationTsid } from "./authentification";

async function createRunningJobFilter(filterName = "running_jobs") {
  const filterFullName = `${filterName}.joblist`;
  const tsid = await getAuthentificationTsid();

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

  const queryUrl = `${process.env.TRACTOR_URL}/monitor?q=putfilter&user=${process.env.TRACTOR_LOGIN}&key=${filterFullName}&tsid=${tsid}`;
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
        };
      };
    };
  };
};

/**
 * Returns a dictionnary with the number of tasks per project
 */
export async function getProjectUsage() {
  const runningJobsFilter = await createRunningJobFilter();
  const tsid = await getAuthentificationTsid();

  const runningJobsResponse = await axios.get<RunningJobs>(
    `${process.env.TRACTOR_URL}/monitor?q=jobs&metadata=0&filter=${runningJobsFilter}&tsid=${tsid}`
  );

  // Flatten the into a list of running jobs
  const runningJobs = Object.values(runningJobsResponse.data.users)
    .map((user) => Object.values(user).map((job) => job.data))
    .flat();

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
