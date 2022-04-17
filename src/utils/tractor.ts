import axios from "axios";
import logger from "./logger";

/**
 * Constructs a Tractor URL route
 * Ex: tractorAPIURL("monitor?q=blades") -> "http://tractor/Tractor/monitor?q=blades"
 */
export function tractorAPIURL(route: string) {
  return `${process.env.TRACTOR_URL}/${route}`;
}

export function tractorQuery<T>(route: string) {
  try {
    const result = axios.get<T>(tractorAPIURL(route));
    return result;
  } catch (err) {
    logger.error(`${err}`);
  }
}
