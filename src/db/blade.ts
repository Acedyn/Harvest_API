import { prisma } from "./client"

// Create a record that stores the blade usage at a given point
export async function createBladeRecord(usage: {busy: number, free: number, nimby: number, off: number}) {
  return await prisma.bladeUsageRecord.create({
    data: {
      busy: usage.busy,
      free: usage.free,
      nimby: usage.nimby,
      off: usage.off,
    }
  });
}
