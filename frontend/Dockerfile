FROM node:21-alpine as builder

WORKDIR /frontend

COPY package*.json ./

RUN npm install

COPY . /frontend

RUN npm run build
