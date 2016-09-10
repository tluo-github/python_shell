#!/usr/bin/env python
# coding=utf-8
# ----------------------------------------------------------
# Name:         自己定义docker moduels
# Purpose:      自己定义采集数据,一个静态一个动态
# Version:      2.0
# Author:       Bruce
# EMAIL:        530308461@qq.com
# Created:      2016-08-22
# Copyright:    (c) Bruce 2016
# Python:       2.6.6
# ----------------------------------------------------------
from docker import Client
import re
import json

def _get_client(timeout=None):
    client = Client(base_url='unix://var/run/docker.sock', version='1.19')
    return client

def _get_containers_data(container,client):
    container_collect = client.stats(container)
    old_result = json.loads(container_collect.next())
    new_result = json.loads(container_collect.next())
    container_collect.close()
    cpu_total_usage = new_result['cpu_stats']['cpu_usage']['total_usage'] - old_result['cpu_stats']['cpu_usage'][
        'total_usage']
    cpu_system_uasge = new_result['cpu_stats']['system_cpu_usage'] - old_result['cpu_stats']['system_cpu_usage']
    cpu_num = len(old_result['cpu_stats']['cpu_usage']['percpu_usage'])
    cpu_percent = round((float(cpu_total_usage) / float(cpu_system_uasge)) * cpu_num * 100.0, 2)

    mem_usage = new_result['memory_stats']['usage']
    mem_limit = new_result['memory_stats']['limit']
    mem_percent = round(float(mem_usage) / float(mem_limit) * 100.0, 2)

    network_rx_packets = new_result['network']['rx_packets']
    network_tx_packets = new_result['network']['tx_packets']

    collect_time = str(new_result['read'].split('.')[0].split('T')[0]) + ' ' + str(
        new_result['read'].split('.')[0].split('T')[1])

    msg = {'Container_name': container,  # 容器名称
           'Cpu_percent': cpu_percent,  # CPU使用率
           'Memory_usage': mem_usage,  # 已使用内存
           'Memory_limit': mem_limit,  # 总内存
           'Memory_percent': mem_percent,  # 内存使用率
           'Network_rx_packets': network_rx_packets,  # 网络流入流量
           'Network_tx_packets': network_tx_packets,  # 网络流出流量
           'Collect_time': collect_time}
    return msg

def inspect_container(container):
    '''获取容器静态数据'''
    client = _get_client()
    return client.inspect_container(container)


def stat_containers():
    '''获取容器动态数据'''
    client = _get_client()
    docker_container = client.containers(all=True)
    container_name = []
    container_run_name = []
    for i in docker_container:
        if re.match('Up', i['Status']):
            container_name.append(i['Names'])
    for b in container_name:
        for c in b:
            container_run_name.append(c[1::])

    data = {}
    for container in container_run_name:
        msg = _get_containers_data(container,client)
        data[container] = msg

    return data





