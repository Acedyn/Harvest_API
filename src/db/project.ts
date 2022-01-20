import { prisma } from "./client"

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
      usage: usage
    }
  });
}
