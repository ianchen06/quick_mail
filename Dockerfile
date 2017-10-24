FROM alpine:3.6

WORKDIR /app

COPY ssl.cnf ssl.sh run.sh ./

RUN apk add --update postfix openssl rsyslog python3
RUN sh ./ssl.sh && mkdir -p /etc/ssl/postfix/ && cp ./server.pem /etc/ssl/postfix/server.pem
COPY main.cf vdomain vmap valias /etc/postfix/
RUN newaliases && postmap /etc/postfix/vdomain && postmap /etc/postfix/valias && postmap /etc/postfix/vmap && mkdir -p /var/spool/vhosts/bitform.co/ && chown 1004:1004 /var/spool/vhosts/bitform.co/
