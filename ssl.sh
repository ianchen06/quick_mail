#/bin/sh
openssl genrsa 512/1024 >server.pem
openssl req -new -key server.pem -days 365 -out request.pem
openssl genrsa 2048 > keyfile.pem
openssl req -new -x509 -nodes -sha1 -days 3650 -key keyfile.pem \
-config ssl.cnf > server.pem
cat keyfile.pem >> server.pem
