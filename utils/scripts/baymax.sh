#!/bin/sh
#/etc/init.d/baymax

### BEGIN INIT INFO
# Provides: laofahai
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Baymax init script
# Description: This service will control the Baymax
### END INIT INFO

start() {
        echo "Baymax is waking up"
        cd "/home/pi/Application/baymax" && python3 baymax.py &
}

stop() {
        echo "Baymax is shutting down"
        kill $(ps -aux | grep -m 1 'python3 baymax.py' | awk '{print $2}')
}

restart() {
        stop;
        sleep 2;
        start;
}

case "$1" in
        start)
                start
                ;;
        stop)
                stop
                ;;
        restart)
                restart
                ;;
esac
exit 1
