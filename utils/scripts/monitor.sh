#!/bin/sh

# 进程监控，防止因为 pygame 等异常情况导致程序意外退出，使用 crontab
# 也可以配合启动脚本 当作自启动脚本使用

RobotID = $(ps -aux | grep -m 1 'python3 baymax.py' | grep -v 'grep' | awk '{print $2}')
StartRobot= $(sudo service baymax restart)
MonitorLog=/tmp/RobotMonitor.log

Monitor()
{
  if [ !$RobotID ];then
    echo "[error] robot not start, starting...  [$(date +'%F %H:%M:%S')]"
    $StartRobot
  fi
}

Monitor>>$MonitorLog
