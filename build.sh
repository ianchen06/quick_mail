#!/bin/bash

if [ $# -lt 1 ]
then
        echo "Usage : $0 Signalnumber PID"
        exit
fi

case "$1" in

build)  echo "Building Docker image"
    docker build -t ten_minute_mail:$(date +%s) .
    ;;
clean)  echo  "Cleaning docker images"
    docker rmi -f $(docker images --all --format "{{.ID}}")
    ;;
run)  echo  "Running container"
    docker run -it --rm -p 25:25 $2 sh -- run.sh
    ;;
9) echo  "Sending SIGKILL signal"
   kill -SIGKILL $2
   ;;
*) echo "Signal number $1 is not processed"
   ;;
esac
