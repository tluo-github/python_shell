#!/usr/bin/env python
# coding=utf-8
import salt.client
import sys

client = salt.client.LocalClient()

hostid = client.cmd('*','hostinfo.host_id')
ip = client.cmd('*','hostinfo.host_ip')
free = client.cmd('*','hostinfo.host_free')
disk = client.cmd('*','hostinfo.host_disk');
meminfo = client.cmd('*','hostinfo.host_meminfo')
cpustats = client.cmd('*','hostinfo.host_cpu')
netdevs = client.cmd('*','hostinfo.host_net')

print '---------------------------hostname-----------------------------------'
print hostid
print '---------------------------cpuinfo-----------------------------------'
for i in cpustats:
    cpuinfolist = cpustats[i]
    cpuone = cpuinfolist[0]['cpu']
    cputwo = cpuinfolist[1]['cpu']
    
    
    total_1 = cpuone['softirq'] + cpuone['irq'] + cpuone['system'] + cpuone['idle'] + cpuone['user'] + cpuone['iowait'] + cpuone['nice']
    total_2 = cputwo['softirq'] + cputwo['irq'] + cputwo['system'] + cputwo['idle'] + cputwo['user'] + cputwo['iowait'] + cputwo['nice']
    
    total_cpu = total_2 - total_1
    total_idle = cputwo['idle'] - cpuone['idle']
   
    cpu_usage = total_idle / total_cpu * 100    
    print "%s cpu_usage:%s" % (i,cpu_usage)
    
print "---------------------------meminfo-------------------------------------"

for i in meminfo:
    meminfolist = meminfo[i]
    MemTotal =(int( meminfolist['MemTotal']['value'])) / 1024
    MemFree = (int( meminfolist['MemFree']['value'])) / 1024
    Buffers =(int( meminfolist['Buffers']['value'])) / 1024
    Cached =(int( meminfolist['Cached']['value'])) / 1024
    
    Free = MemFree + Buffers + Cached
    Used = MemTotal - Free
    print "%s  MemTotal:%s Used:%s  Free: %s " % (i,MemTotal,Used,Free)    


print "---------------------------networkinfo-------------------------------------"
for i in netdevs:
    netinfolist = netdevs[i]
    print i
    for j in netinfolist:
        netinfos = netinfolist[j]
        print "%s in:%s  out:%s" % (netinfos['iface'],netinfos['rx_bytes'],netinfos['rx_packets'])

    print "--------------------------------"
print "---------------------------diskinfo-------------------------------------"
for i in disk:
    diskinfolist = disk[i]
    print i
    for j in diskinfolist:
        diskinfos = diskinfolist[j]
        print diskinfos
