import { prisma } from "./client"

// Create a record that stores the blade usage at a given point
export async function createBladeRecord(usage: {busy: number, free: number, nimby: number, off: number}) {
  return await prisma.bladeUsageRecord.create({
    data: {
      busy: Math.round(usage.busy),
      free: Math.round(usage.free),
      nimby: Math.round(usage.nimby),
      off: Math.round(usage.off),
    }
  });
}

// Get the all the history of the project's usage of the renderfarm
export async function getBladeRecords(start: Date = new Date(0), end: Date = new Date()) {
  return await prisma.bladeUsageRecord.findMany({
    where: {
      createdAt: {
        gte: start,
        lte: end,
      }
    },
    orderBy: {
      createdAt: "asc"
    },
  });
}
