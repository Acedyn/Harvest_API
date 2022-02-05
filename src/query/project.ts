import axios from "axios";
import { getAuthentificationTsid } from "./authentification";

async function createRunningJobFilter(filterName: string = "running_jobs") {
  const filterFullName = `${filterName}.joblist`;
  const existingFilters: any = `${process.env.TRACTOR_URL}/monitor?q=getfilter&user=${process.env.TRACTOR_LOGIN}&key=${filterFullName}`;
  if (existingFilters.data) {
    return filterFullName;
  }
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

export async function getProjectUsage() {
  const runningJobsFilter = await createRunningJobFilter();
  const tsid = await getAuthentificationTsid();
  const running_jobs: any = await axios.get(
    `${process.env.TRACTOR_URL}/monitor?q=jobs&metadata=0&filter=${runningJobsFilter}&tsid=${tsid}`
  );

  const userJobs = Object.values(running_jobs.data.users).map((user: any) =>
    Object.values(user)
  );
  const runningJobs = userJobs.flat().map((job: any) => job.data);

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
