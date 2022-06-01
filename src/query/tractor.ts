import { TractorConfigFiles } from "../types/tractor";
import { tractorQuery } from "../utils/tractor";

export function getTractorConfigFile<F extends keyof TractorConfigFiles>(
  file: F
) {
  return tractorQuery<TractorConfigFiles[F]>(`config?q=get&file=${file}`);
}
