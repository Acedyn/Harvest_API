import { BladeStatuses } from "../types/tractor";
import logger from "../utils/logger";
import { prisma } from "./client";

// Create a record that stores the blade usage at a given point
export async function createBladeRecord(usage: BladeStatuses) {
  logger.info("Saving Blade usage record...");

  return await prisma.bladeUsageRecord.create({
    data: usage,
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
      noFreeSlots: true,
      bug: true,
      createdAt: true,
    },
  });
}
