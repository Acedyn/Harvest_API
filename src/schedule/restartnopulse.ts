import { queryFogGroups } from "../query/fog";
import { restartServiceQuery, getServicesQuery } from "../utils/killprocess";
import { Service } from "../types/gokillprocess";

/**
 * try to clear no pulse blade using restart blade service
 */
export async function restartNoPulse() {
  const groups = await queryFogGroups();
  const salleInfos2022 = groups["99"]; // 99

  const hosts = [];
  for (const computer in salleInfos2022.hosts) {
    hosts.push(salleInfos2022.hosts[computer].name);
  }
  // types for services

  for (const name of hosts) {
    const result =  await getServicesQuery(name);
    if(!result) continue;

    const service: Service = result?.data.find(
      (tp: Service) => tp.Name.includes("Pixar Tractor Blade Service 2.4")
    )
    if (service && service.Status === "Running") console.log(`running on ${name}`)
    if (service && service.Status !== "Running") restartServiceQuery(name, "Pixar Tractor Blade Service 2.4")
  }
  // get services from
}

/**
 * startRestartNoPulse start and call restartNoPulse
 * @param queryInterval the interval in ms between sample queries
 */
export function startRestartNoPulse(queryInterval: number) {
  restartNoPulse();
  setInterval(restartNoPulse, queryInterval);
}
