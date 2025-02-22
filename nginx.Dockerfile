FROM nginx

LABEL org.opencontainers.image.authors="topofeverest8848@gmail.com"

COPY nginx.conf /etc/nginx/nginx.conf
