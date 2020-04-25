FROM node:13-alpine AS builder

COPY . /build
COPY yarn.lock /build
WORKDIR /build
RUN yarn install --non-interactive
ENV NODE_ENV=production
RUN yarn build

FROM nginx:1.17-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /build/dist /usr/share/nginx/html
EXPOSE 80/tcp
