import { prisma } from "./client"

export async function getProjectNames() {
  const projectNames: string[] = []
  const projects = await prisma.project.findMany()
  projects.forEach((project) => {
    projectNames.push(project.name)
  })

  return projectNames
}

// Create a project after making sure it does not already exists
export async function createProject(name: string) {
  const project = await prisma.project.findUnique({
    where: {
      name: name
    }
  });

  // If the project already exists, just return it
  if(project !== null) {
    return project;
  }
  
  return await prisma.project.create({
    data: {
      name: name,
    }
  });
}

// Create a project record after making sure the given project exists
export async function createProjectRecord(name: string, usage: number) {
  const project = await createProject(name);

  return await prisma.projectUsageRecord.create({
    data: {
      project: {
        connect: {
          name: project.name
        }
      },
      usage: Math.round(usage)
    }
  });
}

// Get the all the history of the project's usage of the renderfarm
export async function getProjectRecords(start: Date = new Date(0), end: Date = new Date(), project: string = "") {
  let query: any = {
    where: {
      createdAt: {
        gte: start,
        lte: end,
      },
    },
    orderBy: {
      createdAt: "asc"
    },
    select: {
      projectName: true,
      createdAt: true,
      usage: true,
    }
  }

  if(project) {
    query.where.projectName = {equals: project}
  }
  return await prisma.projectUsageRecord.findMany(query);
}

export async function getProjectComputeTime(start: Date = new Date(0), end: Date = new Date(), project: string = ""): Promise<Date> {
  const projectRecords = await getProjectRecords(start, end, project)
  let totalComputeTime = new Date(0);
  if(!projectRecords[0]) { return totalComputeTime; }

  let lastRecordDate = projectRecords[0].createdAt
  projectRecords.forEach((projectRecord) => {
    const timestampSpan = projectRecord.createdAt.getTime() - lastRecordDate.getTime()
    lastRecordDate = projectRecord.createdAt
    totalComputeTime = new Date(totalComputeTime.getTime() + projectRecord.usage * timestampSpan)
  })

  return totalComputeTime
}
