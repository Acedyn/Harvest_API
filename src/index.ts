import express from 'express';
import dotenv from 'dotenv';

import { startDataRecord  } from './schedule/historyRecord';

dotenv.config()

const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello world!');
});

app.listen(port, () => {
  return console.log(`server is listening on ${port}`);
});

startDataRecord(500, 500);
