FROM node:15-alpine

# Create app directory
WORKDIR /usr/src/app

COPY package.json ./
COPY yarn.lock ./

RUN yarn install
COPY . . 
EXPOSE 5000

RUN npx prisma generate
CMD sh ./scripts/startup.sh
