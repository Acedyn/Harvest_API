import axios from "axios";

interface BladeStatus {
  profile: string,
  nimby: string,
  owners: string[]
  t: number

}

interface BladeQuery {
  blades: BladeStatus[]
}

export async function getBladeUsage() {
  const bladesStatuses: BladeQuery = await axios.get("http://tractor/Tractor/monitor?q=blades");
  
  let busyCount = 0 ;
  let freeCount = 0 ;
  let nimbyCount = 0 ;
  let offCount = 0 ;

  bladesStatuses.blades.forEach((blade) => {
    const lastPulse = new Date(blade.t * 1000)

    // The blade is busy
    if(blade.owners.length) {
      busyCount++;
      return;
    }
    // The blade has its nimby on
    if(blade.nimby) {
      nimbyCount++;
      return;
    }
    // The blade is in idle
    if(Date.now() - lastPulse.getTime() < 500000) {
      freeCount++;
      return
    }

    // The blade is off
    offCount++;
  })
}
