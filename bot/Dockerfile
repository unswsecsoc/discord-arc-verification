FROM node:13-alpine

COPY . /app
WORKDIR /app
RUN yarn install --verbose
RUN yarn build
USER 1000:1000
EXPOSE 3000/tcp
CMD ["yarn", "prod"]