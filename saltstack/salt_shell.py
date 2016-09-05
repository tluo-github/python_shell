#!/usr/bin/env python
# coding=utf-8
# ----------------------------------------------------------
# Name:         获取被控机运行情况脚本
# Purpose:      获取所有被控机（CPU使用率、内存使用情况、磁盘使用情况、网络流量）
# Version:      1.0
# Author:       Bruce
# EMAIL:        530308461@qq.com
# Created:      2016-08-22
# Copyright:    (c) Bruce 2016
# Python:       2.6.6
# ----------------------------------------------------------
import salt.client
import sys


# 该类获得被控机器情况
class hostinfo(object):
    def __init__(self):
        self.client = salt.client.LocalClient()

    def getcpuinfo(self):
        '''
        获取CPU使用率,获取2个采样点,计算其差值
        算法：cpu usage=(idle2-idle1)/(cpu2-cpu1)*100
        '''
        cpustats = self.client.cmd('*', 'hostinfo.host_cpu')
        for i in cpustats:
            cpuinfolist = cpustats[i]
            cpuone = cpuinfolist[0]['cpu']
            cputwo = cpuinfolist[1]['cpu']

            total_1 = cpuone['softirq'] + cpuone['irq'] + cpuone['system'] + cpuone['idle'] + cpuone['user'] + cpuone[
                'iowait'] + cpuone['nice']
            total_2 = cputwo['softirq'] + cputwo['irq'] + cputwo['system'] + cputwo['idle'] + cputwo['user'] + cputwo[
                'iowait'] + cputwo['nice']

            total_cpu = total_2 - total_1
            total_idle = cputwo['idle'] - cpuone['idle']

            cpu_usage = total_idle / total_cpu * 100
            print "%s cpu_usage:%s" % (i, cpu_usage)

    def getmeminfo(self):
        '''获取内存使用情况'''
        meminfo = self.client.cmd('*', 'hostinfo.host_meminfo')
        for i in meminfo:
            meminfolist = meminfo[i]
            MemTotal = (int(meminfolist['MemTotal']['value'])) / 1024
            MemFree = (int(meminfolist['MemFree']['value'])) / 1024
            Buffers = (int(meminfolist['Buffers']['value'])) / 1024
            Cached = (int(meminfolist['Cached']['value'])) / 1024

            Free = MemFree + Buffers + Cached
            Used = MemTotal - Free
            print "%s  MemTotal:%s Used:%s  Free: %s " % (i, MemTotal, Used, Free)

    def getnetworkinfo(self):
        '''获取网络的入口流量和出口流量'''
        netdevs = self.client.cmd('*', 'hostinfo.host_net')
        for i in netdevs:
            netinfolist = netdevs[i]

            network_in = 0
            network_out = 0
            for j in netinfolist:
                netinfos = netinfolist[j]
                network_in += netinfos['rx_bytes']
                network_out += netinfos['rx_packets']
                # print "%s in:%s  out:%s" % (netinfos['iface'],netinfos['rx_bytes'],netinfos['rx_packets'])

            print "host:%s in:%s out:%s" % (i, network_in, network_out)
            print "-----------------------------------------------------"

    def getdiskinfo(self):
        '''获取磁盘使用情况'''
        disk = self.client.cmd('*', 'hostinfo.host_disk');
        for i in disk:
            diskinfolist = disk[i]
            print i
            for j in diskinfolist:
                diskinfos = diskinfolist[j]
                print diskinfos


class Main(object):
    def main(self):
        '''主调函数'''
        host = hostinfo()
        host.getcpuinfo()
        host.getmeminfo()
        host.getnetworkinfo()
        host.getdiskinfo()


if __name__ == '__main__':
    main_obj = Main()
    main_obj.main()    