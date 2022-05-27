import axios from "axios";
import logger from "./logger";

/**
 * Constructs a kill process URL route
 * Ex: gokillprocessURL("192.168.2.100", "monitor?q=blades") -> "http://192.168.2.100:5119/processes"
 */
export function gokillprocessURL(bladeIp: string, route: string) {
  return `http://${bladeIp}:${process.env.GOKILLPROCESS_PORT}/${route}`;
}

export async function getProcessesQuery(bladeIp: string) {
  try {
    return await axios.get(gokillprocessURL(bladeIp, "processes"));
  } catch (err) {
    logger.error(`${err} for ${bladeIp}`);
  }
}

export async function killProcessesQuery(bladeIp: string, pid: number) {
  try {
    return await axios.post(gokillprocessURL(bladeIp, `kill/${pid}`));
  } catch (err) {
    logger.error(`${err} killing ${pid} for ${bladeIp}`);
  }
}

export async function restartServiceQuery(bladeIp: string, serviceName: string) {
  try {
    return await axios.post(gokillprocessURL(bladeIp, 'restartservice'), serviceName);
  } catch (err) {
    logger.error(`${err} restarting service ${serviceName} for ${bladeIp}`);
  }
}

export async function getServicesQuery(bladeIp: string) {
  try {
    return await axios.get(gokillprocessURL(bladeIp, "services"));
  } catch (err) {
    logger.error(`${err} for ${bladeIp}`);
  }
}
