FROM node:16
WORKDIR /usr/src/app
COPY reward/package*.json ./
RUN npm install
COPY reward/index.js ./
CMD [ "npm", "start" ]