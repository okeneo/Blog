FROM node:21-alpine as builder

WORKDIR /frontend

COPY package*.json ./

RUN npm run install

COPY . /frontend

RUN npm run build
