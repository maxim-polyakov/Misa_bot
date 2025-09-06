FROM node:24-alpine

COPY package*.json .
COPY client/yarn.lock .

RUN yarn --frozen-lockfile

COPY . .

EXPOSE 3000

CMD ["yarn", "start"]
