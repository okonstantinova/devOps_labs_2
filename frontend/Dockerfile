FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci && npm cache clean --force

COPY . .
RUN npm run build

FROM nginx:alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=build /app/build /usr/share/nginx/html

USER appuser

