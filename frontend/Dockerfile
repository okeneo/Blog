FROM node:21-alpine as builder

WORKDIR /frontend

COPY package.json ./
COPY package-lock.json ./

RUN npm ci

COPY . /frontend

CMD ["npm", "run", "build"]
