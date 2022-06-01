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

export interface BladeStatuses {
  busy: number;
  off: number;
  nimby: number;
  free: number;
  noFreeSlots: number;
  bug: number;
}

export interface Job {
  comment: string;
  maxslots: number;
  numblocked: number;
  pil: number;
  spoolcwd: string;
  numerror: number;
  editpolicy: string;
  elapsedsecs: number;
  owner: string;
  numdone: number;
  spoolhost: string;
  maxtid: number;
  spooladdr: string;
  jid: number;
  maxactive: number;
  service: string;
  title: string;
  priority: number;
  spooltime: string;
  numtasks: number;
  crews: string[];
  maxcid: number;
  metadata: string;
  numready: number;
  tags: string[];
  lastnoteid: number;
  stoptime: string;
  envkey: [];
  tier: string;
  etalevel: number;
  projects: string[];
  dirmap: null;
  serialsubtasks: false;
  afterjids: number[];
  numactive: number;
  aftertime: null;
  assignments: string;
  spoolfile: string;
  esttotalsecs: number;
  starttime: string;
  pausetime: null;
  minslots: number;
  deletetime: null;
}

export interface Task {
  maxslots: number;
  resumeblock: boolean;
  id: string;
  jid: number;
  activetime: string;
  service: string;
  title: string;
  state: string;
  ptids: string[];
  tid: number;
  progress: number;
  chaser: [];
  preview: [];
  metadata: string;
  statetime: string;
  haslog: boolean;
  retrycount: number;
  cids: string[];
  currcid: number;
  serialsubtasks: boolean;
  readytime: string;
  attached: boolean;
  minslots: number;
}

export interface Command {
  maxslots: number | null;
  jid: number;
  maxrunsecs: number;
  service: string;
  cid: number;
  minrunsecs: number;
  tags: string[];
  retryrcodes: number[];
  argv: string[];
  resumepin: boolean;
  runtype: string;
  metadata: string;
  envkey: string[];
  refersto: string;
  resumewhile: number[];
  tid: number;
  minslots: number | null;
  local: boolean;
  id: string;
  expand: boolean;
  msg: string;
}
