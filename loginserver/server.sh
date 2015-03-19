#!/bin/sh

case "$1" in
  start)
        sh run.sh
        ;;
  stop)
        python stop-server.py
        ;;
  restart)
        ./stop-server.py&sh run.sh
        ;;    	
esac

exit 0
