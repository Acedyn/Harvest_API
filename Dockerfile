FROM node:16-alpine

# Create app directory
WORKDIR /usr/src/app

COPY package.json yarn.lock ./

RUN yarn install --frozen-lockfile
COPY . . 
EXPOSE 3000

RUN npx prisma generate
CMD [  "yarn", "start:migrate:prod" ]
