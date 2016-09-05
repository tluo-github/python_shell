#!/usr/bin/env python
# coding=utf-8
# ----------------------------------------------------------
# Name:         自己定义moduels
# Purpose:      自己定义采集数据,一个静态一个动态
# Version:      2.0
# Author:       Bruce
# EMAIL:        530308461@qq.com
# Created:      2016-08-22
# Copyright:    (c) Bruce 2016
# Python:       2.6.6
# ----------------------------------------------------------
import time

def grainscmd(cmd):
    CMD_RUN = __salt__['grains.item']
    return CMD_RUN(cmd)


def host_grains():
    '''获得机器静态详细信息'''
    grains ={}
    osfinger = grainscmd('osfinger') #操作系统 eg:Centos_6
    osarch = grainscmd('osarch')  #操作系统位数 eg:x86_64
    kernel = grainscmd('kernel')  #操作系统类型 eg:Liunx
    kernelrelease = grainscmd('kernelrelease') #操作系统内核版本 eg: 3.10.10-1.el6.elrepo.x86_64
    num_cpus = grainscmd('num_cpus')  #CPU核数
    cpu_model = grainscmd('cpu_model') #CPU型号 eg:Intel(R)xen(R) CPU E3-1231 v3 3.4GHz
    ip4_interfaces = grainscmd('ip4_interfaces') #网络IP地址
    mem_total = grainscmd('mem_total') #物理内存 M


    grains['osfinger'] = osfinger
    grains['osarch'] = osarch
    grains['kernel'] = kernel
    grains['kernelrelease'] = kernelrelease
    grains['cpu_model'] = cpu_model
    grains['ip4_interfaces'] = ip4_interfaces
    grains['num_cpus'] = num_cpus
    grains['mem_total'] = mem_total

    return grains

def host_getdhcpdata():
    '''获得机器动态数据'''
    items = {}

    meminfo = __salt__['status.meminfo']() #获得内存使用情况
    uptime = __salt__['status.uptime']() #获得运行时间
    disk_usage = __salt__['disk.usage']() #获得磁盘使用情况
    net_usage = __salt__['status.netdev']() #获得流量数据

    cpulist = [] #获得CPU使用率
    cpu_one = __salt__['status.cpustats']()
    time.sleep(1)
    cpu_two = __salt__['status.cpustats']()
    cpulist.append(cpu_one)
    cpulist.append(cpu_two)

    items['meminfo'] = meminfo
    items['uptime'] = uptime
    items['disk_usage'] = disk_usage
    items['net_usage'] = net_usage
    items['cpulist'] = cpulist

    return items

