import { prisma } from "./client";
import { Prisma } from "@prisma/client";
import logger from "../utils/logger";

export async function getProjectNames() {
  const projectNames: string[] = [];
  const projects = await prisma.project.findMany();

  projects.forEach((project) => {
    projectNames.push(project.name);
  });

  return projectNames;
}

// Create a project after making sure it does not already exists
export async function createProject(name: string) {
  const project = await prisma.project.findUnique({
    where: {
      name: name,
    },
  });

  // If the project already exists, just return it
  if (project !== null) {
    return project;
  }

  return await prisma.project.create({
    data: {
      name: name,
    },
  });
}

// Create a project record after making sure the given project exists
export async function createProjectRecord(name: string, usage: number) {
  logger.info("Saving project usage record...");
  const project = await createProject(name);

  return await prisma.projectUsageRecord.create({
    data: {
      project: {
        connect: {
          name: project.name,
        },
      },
      usage: Math.round(usage),
    },
  });
}

// Get the all the history of the project's usage of the renderfarm
export async function getProjectRecords(
  start: Date = new Date(0),
  end: Date = new Date(),
  project = ""
) {
  const query: Prisma.ProjectUsageRecordFindManyArgs = {
    where: {
      createdAt: {
        gte: start,
        lte: end,
      },
    },
    orderBy: {
      createdAt: "asc",
    },
    select: {
      projectName: true,
      createdAt: true,
      usage: true,
    },
  };

  if (project && query.where) {
    query.where.projectName = { equals: project };
  }

  return await prisma.projectUsageRecord.findMany(query);
}

export async function gatherProjectUsageHistory(
  start: Date,
  end: Date,
  project = ""
) {
  const projectRecords = await getProjectRecords(start, end, project);

  const groupedProjectRecords: {
    [time: string]: { [name: string]: number };
  } = {};

  projectRecords.forEach((projectRecord) => {
    // We have to round the creation time to the closest hour to reduce the amount of records
    const roundDate = projectRecord.createdAt;
    roundDate.setHours(
      roundDate.getHours() + Math.round(roundDate.getMinutes() / 60)
    );
    roundDate.setMinutes(0, 0, 0);

    const index = roundDate.getTime().toString();
    if (!groupedProjectRecords[index]) {
      groupedProjectRecords[index] = {};
    }
    groupedProjectRecords[index][projectRecord.projectName] =
      projectRecord.usage;
  });

  type ProjectSample = { [key: string]: number } & { createdAt: Date };
  const formattedProjectRecords: ProjectSample[] = [];

  for (const [key, value] of Object.entries(groupedProjectRecords)) {
    formattedProjectRecords.push({
      ...value,
      createdAt: new Date(parseInt(key)),
    } as ProjectSample);
  }

  return formattedProjectRecords;
}

export async function getProjectComputeTime(
  start: Date = new Date(0),
  end: Date = new Date(),
  project = ""
): Promise<Date> {
  // Get project usage records
  const projectRecords = await gatherProjectUsageHistory(start, end, project);
  let totalComputeTime = 0;

  if (!projectRecords[0]) {
    return new Date(0);
  }

  let lastRecordDate = projectRecords[0].createdAt;

  // For each project record compute timeDiff * number of computers used
  projectRecords.forEach((projectRecord) => {
    const { createdAt, ...rest } = projectRecord;

    const timestampSpan = createdAt.getTime() - lastRecordDate.getTime();

    lastRecordDate = createdAt;

    // Sum up all projects active tasks
    const allProjectsUsage = Object.values(rest).reduce((a, b) => a + b, 0);

    totalComputeTime += allProjectsUsage * timestampSpan;
  });

  return new Date(totalComputeTime);
}
