export interface Blade {
  profile: string;
  vers: string;
  gpulabel: string;
  nimby: string;
  mem: number;
  bladeid: string;
  osname: string;
  ncpu: number;
  as: number;
  osversion: string;
  disk: number;
  numcmd: number;
  owners: string[];
  udi: number;
  addr: string;
  siu: number;
  hnm: string;
  t0: number;
  note: string;
  t: number;
  lp: number;
  ns: number;
  cpu: number;
}

export interface LoginData {
  rc: number;
  login: string;
  host: string;
  user: string;
  tsid: string;
  crews: string[];
  access: { jnotes: number; bnotes: number };
  engine: string;
  protocol: string;
}
