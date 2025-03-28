FROM nginx:alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY nginx.conf /etc/nginx/nginx.conf

USER appuser

