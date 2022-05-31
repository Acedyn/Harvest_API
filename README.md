# Harvest API 👨‍🌾👩‍🌾🌾

![](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white) ![](https://img.shields.io/badge/express-40a9fe?style=for-the-badge&logo=express&logoColor=white) ![](https://img.shields.io/badge/Prisma-38a169?style=for-the-badge&logo=prisma&logoColor=white) ![](https://img.shields.io/badge/ESLint-4b32c3?style=for-the-badge&logo=eslint&logoColor=white) ![](https://img.shields.io/badge/Prettier-c188c1?style=for-the-badge&logo=prettier&logoColor=white)

<br>

## Introduction

Harvest is a realtime front-end application to display useful statistics for the Tractor render farm.

This is the backend API repository that the [front-end](https://github.com/ArtFXDev/harvest-ui) uses.

It uses [Prisma](https://www.prisma.io/) which is a [TypeScript](https://www.typescriptlang.org/) ORM for interacting with a [PostgreSQL](https://www.postgresql.org/) database. Then [Express](https://expressjs.com/) is used to build the REST API.

## Installation

The package manager used is [Yarn](https://yarnpkg.com/). Clone the repository and install the dependencies:

```bash
$ git clone https://github.com/ArtFXDev/harvest-api
$ cd harvest-api
$ yarn install # Install the dependencies
```

## Usage

### Environment variables

Before starting the API, make sure the variables defined in the [`.env`](.env) file are correct. To see which one are needed, please see the [`.env.example`](.env.example) file in the root of the repository.

They are:

- `TRACTOR_URL` - the url of the running Tractor API instance. Usually the hostname is `tractor` so it will be [http://tractor/Tractor](http://tractor/Tractor)

- `TRACTOR_LOGIN` / `TRACTOR_PASSWORD` - the user and password of the Tractor account (you need to enable account based auth in the configuration)

- `HARVEST_DB_USER` / `HARVEST_DB_PASSWORD` - the user and password of the Postgres database

### Available scripts

- 🚀 `yarn dev` -> will start a [`nodemon`](https://nodemon.io/) process to automatically reload the code on changes

  You can then access the api on [`http://localhost:3000`](http://localhost:3000).

- 👷 `yarn prod` -> launches the API in production mode without hot-reload

- 🔨 `yarn tsc` -> runs the TypeScript compiler and report errors. Add `:watch` to run an interactive process that watches file changes.

- 💅 `yarn prettify` -> prettify the code with Prettier. Add `:write` to write the modifications.

- 🚨 `yarn lint` -> shows ESLint warnings and errors. Add `:fix` to apply auto fixes.

## Libraries

Here are the main libraries and packages used:

| Library                                       | Version  |
| --------------------------------------------- | -------- |
| [Express](https://expressjs.com/)             | `4.17.2` |
| [TypeScript](https://www.typescriptlang.org/) | `4.5.5`  |
| [Prisma](https://www.prisma.io/)              | `3.8.1`  |

## Contributing

Pull requests and issues are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](./LICENSE.md) [@ArtFX](https://artfx.school/)
