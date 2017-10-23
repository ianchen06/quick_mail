FROM alpine:3.6

WORKDIR /app

COPY ssl.cnf ssl.sh ./

RUN apk add --update postfix openssl rsyslog
RUN sh ./ssl.sh && mkdir -p /etc/ssl/postfix/ && cp ./server.pem /etc/ssl/postfix/server.pem && newaliases
COPY main.cf vdomain vmap valias /etc/postfix/
