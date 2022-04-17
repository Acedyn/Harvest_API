class Log {
  private log(level: string, msg: string) {
    // eslint-disable-next-line no-console
    console.log(
      `[${new Date().toISOString()}] [${level.toUpperCase()}] ${msg}`
    );
  }

  info(msg: string) {
    this.log("info", msg);
  }

  warning(msg: string) {
    this.log("warning", msg);
  }

  error(msg: string) {
    this.log("error", msg);
  }
}

const logger = new Log();
export default logger;
