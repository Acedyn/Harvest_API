import { BladeStatuses } from "../types/tractor";
import { prisma } from "./client";

// Create a record that stores the blade usage at a given point
export async function createBladeRecord(usage: BladeStatuses) {
  return await prisma.bladeUsageRecord.create({
    data: {
      busy: Math.round(usage.busy),
      free: Math.round(usage.free),
      nimby: Math.round(usage.nimby),
      off: Math.round(usage.off),
      noFreeSlots: Math.round(usage.noFreeSlots),
    },
  });
}

// Get the all the history of the project's usage of the renderfarm
export async function getBladeRecords(
  start: Date = new Date(0),
  end: Date = new Date()
) {
  return await prisma.bladeUsageRecord.findMany({
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
      busy: true,
      nimby: true,
      off: true,
      free: true,
      createdAt: true,
    },
  });
}
