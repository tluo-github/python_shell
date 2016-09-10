#!/usr/bin/env python
# coding=utf-8
# ----------------------------------------------------------
# Name:         获取被控机运行情况脚本
# Purpose:      获取所有被控机（CPU使用率、内存使用情况、磁盘使用情况、网络流量）插入数据库
# Version:      2.0
# Author:       Bruce
# EMAIL:        530308461@qq.com
# Created:      2016-08-22
# Copyright:    (c) Bruce 2016
# Python:       2.6.6
# ----------------------------------------------------------
import salt.client
import sys
import MySQLdb
import time
# 该类获得被控机器情况
class hostdata(object):
    def __init__(self):
        self.client = salt.client.LocalClient()


    def getdhcpdata(self):
        itmes = self.client.cmd('*','hostinfo.host_getdhcpdata')
        return itmes


    def formatcpuinfo(self,cpuinfolist):
        '''
        返回格式化后CPU使用率,获取2个采样点,计算其差值
        算法1：cpu usage=(idle2-idle1)/(cpu2-cpu1)*100 这个有个BUG 当 idle2 == idle1 的时候就是0
        算法2：cpu usage=[(user_2 +sys_2+nice_2) - (user_1 + sys_1+nice_1)]/(total_2 - total_1)*100
        '''
        cpuone = cpuinfolist[0]['cpu']
        cputwo = cpuinfolist[1]['cpu']

        total_1 = cpuone['softirq'] + cpuone['irq'] + cpuone['system'] + cpuone['idle'] + cpuone['user'] + cpuone[
            'iowait'] + cpuone['nice']
        total_2 = cputwo['softirq'] + cputwo['irq'] + cputwo['system'] + cputwo['idle'] + cputwo['user'] + cputwo[
            'iowait'] + cputwo['nice']

        total_result =  float(total_2 - total_1)
        #print total_result

        total_two = cputwo['user'] + cputwo['system'] + cputwo['nice']
        total_one = cpuone['user'] + cpuone['system'] + cpuone['nice']
        result = float(total_two - total_one)
        #print result



        cpu_usage = ("%.2f " % (result / total_result))
        cpuitems = {}
        cpuitems['cpu_usage'] = cpu_usage
        return cpuitems

    def formatmeminfo(self,meminfo):
        '''返回格式化后内存使用情况'''

        MemTotal = (float(meminfo['MemTotal']['value']))
        MemFree = (float(meminfo['MemFree']['value']))
        Buffers = (float(meminfo['Buffers']['value']))
        Cached = (float(meminfo['Cached']['value']))

        Free = MemFree + Buffers + Cached
        Used = MemTotal - Free

        #mem_percent = ("%.2f " % ( Used / MemTotal ))
        mem_percent = round(float(Used) / float(MemTotal) * 100.0, 2)
        #print "  MemTotal:%s Used:%s  Free: %s " % ( MemTotal, Used, Free)
        memitems = {}
        memitems['mem_total'] = MemTotal
        memitems['mem_used'] = Used
        memitems['mem_free'] = Free
        memitems['mem_percent'] = mem_percent
        return memitems

    def formatnetworkinfo(self,netinfolist):
        '''返回格式化后网络的入口流量和出口流量'''
        network_in = 0
        network_out = 0
        for j in netinfolist:
            netinfos = netinfolist[j]
            network_in += netinfos['rx_bytes']
            network_out += netinfos['rx_packets']

        networkitems = {}
        networkitems['network_in'] = network_in
        networkitems['network_out'] = network_out
        return networkitems

    def formatdiskinfo(self,diskinfolist):
        '''返回格式化后磁盘使用情况'''
        print diskinfolist
#数据库操作
class DbHelp(object):
    def __init__(self):
        self.host = '192.168.174.130'
        self.user = 'yuancheng'
        self.passwd = 'Aa_123@#'
        self.db = 'OMServer'
        self.charset = 'utf8'
        self.conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,charset=self.charset)
        self.cursor = self.conn.cursor()


    def insert(self,name,sql):
        n = self.cursor.execute(sql)
        if n <= 0:
            print "%s insert faild" % name
        else:
            self.conn.commit()
            #print "commit"




    def close(self):
        #self.conn.commit()
        self.cursor.close()
        self.conn.close()
class Main(object):
    def main(self):
        '''主调函数'''
        host_info = hostdata()
        items = host_info.getdhcpdata()
        db_help = DbHelp()
        for i in items:
            #print i
            item = items[i]
            memitems = host_info.formatmeminfo(item['meminfo'])
            cpuitems = host_info.formatcpuinfo(item['cpulist'])
            networkitems = host_info.formatnetworkinfo(item['net_usage'])
            #print cpuitems
            name = i
            cpu_usage = cpuitems['cpu_usage']
            mem_total = memitems['mem_total']
            mem_used = memitems['mem_used']
            mem_free = memitems['mem_free']
            mem_percent = memitems['mem_percent']

            network_in = networkitems['network_in']
            network_out = networkitems['network_out']
            diskinfo= item['disk_usage']
            uptime = item['uptime']

            insertSQL = 'insert into jsh_hosts_data (`NAME`,cpu_usage, mem_total, mem_used, mem_free,mem_percent, network_in, network_out, diskinfo, uptime, createtime )' \
                        ' values("%s",%s,%s,%s,%s,%s,%s,%s,"%s","%s",now())' % (name,cpu_usage,mem_total,mem_used,mem_free,mem_percent,network_in,network_out,diskinfo,uptime)
            #updateSQL = 'UPDATE jsh_hosts set `status`=%s ,cpu_percent=%s,mem_percent=%s WHERE `name`=%s' % ('0',cpu_usage,mem_percent,)
            #print insertSQL
            #print
            db_help.insert(name, insertSQL)

        db_help.close()
if __name__ == '__main__':
    start = time.clock()
    main_obj = Main()
    main_obj.main()
    end = time.clock()
    #print("The script run time is : %.03f seconds" % (end - start))