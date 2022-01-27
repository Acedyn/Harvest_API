import axios from "axios";

function asciiToHexa(str: string) {
  const arr1 = [];

  for (let n = 0; n < str.length; n++) {
    var hex = Number(str.charCodeAt(n)).toString(16);
    arr1.push(hex);
  }

  return arr1.join("");
}

export async function get_authentification_tsid(): Promise<string> {
  const chalenge = await axios.get(`${process.env.TRACTOR_URL}/monitor?q=gentoken`);
  const challengeEncoded = asciiToHexa(chalenge.data.challenge + "|" + process.env.TRACTOR_PASSWORD);
  const token = await axios.get(
    `${process.env.TRACTOR_URL}/monitor?q=login&user=${process.env.TRACTOR_LOGIN}&c=${challengeEncoded}`
  );

  return token.data.tsid
}
