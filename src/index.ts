import dotenv from "dotenv";

import { startDataRecord } from "./schedule/history";
import { startRestServer } from "./route/app";

dotenv.config();

startRestServer(3000);
startDataRecord(60000);
