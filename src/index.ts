import dotenv from "dotenv";

import { startDataRecord } from "./schedule/history";
import { initializeRoutes, startRestServer } from "./route/app";

// Read env file for configuration
dotenv.config();

initializeRoutes();
startRestServer(3000);
startDataRecord(60000);
