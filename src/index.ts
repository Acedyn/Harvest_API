import dotenv from "dotenv";

import { startDataRecord } from "./schedule/history";
import { startClearNoFreeSlots } from "./schedule/nofreeslots";
import { initializeRoutes, startRestServer } from "./route/app";

// Read env file for configuration
dotenv.config();

initializeRoutes();
startRestServer(3000);
startDataRecord(60000);
startClearNoFreeSlots(60000 * 60 * 3)