import axios from "axios";
import { LoginData } from "../types/tractor";
import { tractorAPIURL } from "../utils/tractor";

let TSID: string | undefined = undefined;

/**
 * Converts a string into hexadecimal
 */
function asciiToHexa(str: string) {
  const arr1 = [];

  for (let n = 0; n < str.length; n++) {
    const hex = Number(str.charCodeAt(n)).toString(16);
    arr1.push(hex);
  }

  return arr1.join("");
}

/**
 * Authenticate to the Tractor API and return the TSID token
 * See: https://rmanwiki.pixar.com/display/TRA/Login+Management#LoginManagement-ImplementingAuthenticationinExternalScripts
 */
export async function getAuthenticationTsid(): Promise<string> {
  if (TSID) {
    return TSID;
  }

  const chalenge = await axios.get<{ challenge: string }>(
    tractorAPIURL("monitor?q=gentoken")
  );

  const challengeEncoded = asciiToHexa(
    chalenge.data.challenge + "|" + process.env.TRACTOR_PASSWORD
  );

  const loginResponse = await axios.get<LoginData>(
    tractorAPIURL(
      `monitor?q=login&user=${process.env.TRACTOR_LOGIN}&c=${challengeEncoded}`
    )
  );

  TSID = loginResponse.data.tsid;
  return TSID;
}
