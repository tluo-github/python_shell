#!/usr/bin/env python
# coding=utf-8
import time
def hostcmd(cmd):
    CMD_RUN = __salt__['cmd.run']
    return CMD_RUN(cmd)

def host_id():
    hostname = __salt__['grains.item']
    return hostname('id')

def host_meminfo():
    meminfo = __salt__['status.meminfo']
    return meminfo()

def host_uptime():
    uptime = __salt__['status.uptime']
    return uptime()

def host_ip():
    ip_addr = __salt__['network.ip_addrs']
    return ip_addr()

def host_cpu():
    cpulist = []
    cpu_one = __salt__['status.cpustats']()
    time.sleep(2)
    cpu_two = __salt__['status.cpustats']()
    cpulist.append(cpu_one)
    cpulist.append(cpu_two)
    return cpulist

def host_disk():
    disk_usage = __salt__['disk.usage']
    return disk_usage()

def host_net():
    net_usage = __salt__['status.netdev']
    return net_usage()

