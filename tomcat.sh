#!/bin/bash
#----------------------------------------------------------
# Name:         tomcat管理脚本
# Purpose:      tomcat: start/stop/restart/status tomcat
# Version:      1.0
# Author:       Bruce
# EMAIL:        530308461@qq.com
# Created:      2016-08-31
# Copyright:    (c) Bruce 2016
# Liunx:        centos 6
#----------------------------------------------------------
  
#--This line of code must
. /etc/rc.d/init.d/functions

tomcat_home="/home/www/tomcat-7.0.68"

getPID() {
	PID=$(ps -ef|grep -v grep|grep $tomcat_home|cut -c10-14|sed -n 1p)
}

start() {
        getPID
        if [[ "${PID}X" != "X" ]]; then
            echo "-------------------------------tomcat is already running----------------------"
        else
            echo "-------------------------------starting tomcat--------------------------------"
	    cd $tomcat_home
	    sh bin/startup.sh
	    sleep 2
	    echo "-------------------------------tomcat startup success-------------------------"
        fi
}
  
stop() {
        getPID
        if [[ "${PID}X" == "X" ]]; then
            echo "-------------------------------tomcat is not running--------------------------"
        else
            echo "-------------------------------stoping tomcat---------------------------------"
	    cd $tomcat_home
	    sh bin/shutdown.sh
	    sleep 2
	    echo "-------------------------------tomcat stoping success-------------------------"
        fi
}
  
restart() {
        stop
	start
}
  
status() {
        getPID
        if [[ "${PID}X" == "X" ]]; then
            echo "-------------------------------tomcat is not running!-------------------------"
        else
            echo "-------------------------------tomcat is running!-----------------------------"
        fi
}
  
case $1 in
        start   )
                start
                ;;
        stop    )
                stop
                ;;
        restart )
                restart
                ;;
        status  )
                status
                ;;
        *       )
                echo $"Usage: $0 {start|stop|restart|status}"
                exit 2
                ;;
esac