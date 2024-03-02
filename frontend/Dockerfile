FROM node:21-alpine as builder

WORKDIR /frontend

COPY package.json ./
COPY package-lock.json ./

RUN npm ci

COPY . /frontend

CMD ["npm", "run", "build"]

# RUN npm run build

# FROM nginx:1.25.4-alpine

# COPY --from=builder /frontend/build /usr/share/nginx/html

# COPY ../nginx/default.conf /etc/nginx/conf.d/default.conf

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]
