import axios from "axios";
import { LoginData } from "../types/tractor";

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
export async function getAuthentificationTsid(): Promise<string> {
  const chalenge = await axios.get<{ challenge: string }>(
    `${process.env.TRACTOR_URL}/monitor?q=gentoken`
  );

  const challengeEncoded = asciiToHexa(
    chalenge.data.challenge + "|" + process.env.TRACTOR_PASSWORD
  );

  const loginResponse = await axios.get<LoginData>(
    `${process.env.TRACTOR_URL}/monitor?q=login&user=${process.env.TRACTOR_LOGIN}&c=${challengeEncoded}`
  );

  return loginResponse.data.tsid;
}
