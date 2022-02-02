import dotenv from 'dotenv';

import { startDataRecord  } from './schedule/historyRecord';
import { startRestServer  } from './route/app';

dotenv.config()

startRestServer(3000);
startDataRecord(1000, 6000);
