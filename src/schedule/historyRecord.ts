import { createProjectRecord } from "../db/project";
import { createBladeRecord } from "../db/blade";
import { getProjectUsage } from "../query/project";
import { getBladeUsage } from "../query/blade";

export function startDataRecord(queryInterval: number, storeInterval: number) {
  setInterval(async () => {
    for (const [projectName, projectData] of Object.entries(await getProjectUsage())) {
      await createProjectRecord(projectName, projectData);
    }
    await createBladeRecord(await getBladeUsage());
  }, storeInterval);
}
