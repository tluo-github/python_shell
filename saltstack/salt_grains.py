#!/usr/bin/env python
# coding=utf-8
# ----------------------------------------------------------
# Name:         获取被控机静态数据脚本
# Purpose:      获取被控机静态数据(主机名(salt)、操作系统、系统内核、CPU核数、CPU型号、IP地址)
# Version:      1.0
# Author:       Bruce
# EMAIL:        530308461@qq.com
# Created:      2016-08-22
# Copyright:    (c) Bruce 2016
# Python:       2.6.6
# ----------------------------------------------------------
import salt.client

#该类获得被控机器情况
class hostinfo(object):
    def __init__(self,host):
        self.client = salt.client.LocalClient()
        self.host = host

    def getgrains(self):
        '''获得数据'''
        grains = self.client.cmd(self.host, 'hostinfo.host_grains')
        return grains[self.host]

class  Main(object):
    def main(self):
        '''主调函数'''
        name = 'www.jsh315.com_master'
        host = hostinfo(name)
        hostgrains = host.getgrains()

        os = '%s-%s' % (hostgrains['osfinger']['osfinger'],hostgrains['osarch']['osarch'])
        kernel = '%s-%s' % (hostgrains['kernel']['kernel'],hostgrains['kernelrelease']['kernelrelease'])
        num_cpus = hostgrains['num_cpus']['num_cpus']
        cpu_model = hostgrains['cpu_model']['cpu_model']
        lo = hostgrains['ip4_interfaces']['ip4_interfaces']['lo'][0]
        eth0 = hostgrains['ip4_interfaces']['ip4_interfaces']['eth0'][0]


if __name__ == '__main__':
    main_obj = Main()
    main_obj.main()
