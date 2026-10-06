FROM node:24-alpine

WORKDIR /app

# CRA вшивает REACT_APP_* только на этапе yarn build (не из runtime env_file).
ARG REACT_APP_API_URL=https://misaapi.baxic.ru
ARG REACT_APP_API_WSS=
ENV REACT_APP_API_URL=$REACT_APP_API_URL
ENV REACT_APP_API_WSS=$REACT_APP_API_WSS

COPY package*.json yarn.lock ./
RUN yarn --frozen-lockfile

COPY . .
RUN yarn build

RUN yarn global add serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
