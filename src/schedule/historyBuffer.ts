interface HistoryBuffer {
  queryCounter: number
}

export interface BladeHistoryBuffer extends HistoryBuffer {
  bladeUsage: {
    busy: number,
    free: number,
    nimby: number,
    off: number,
  }
}

export interface ProjectHistoryBuffer extends HistoryBuffer {
  projectUsage: {
    [key: string]: number
  }
}
