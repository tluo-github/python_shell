#!/usr/bin/env python
# coding:utf-8
'''
功能：扫描目标指定端口
日期: 2016-10-28
版本: V1
'''
import socket
import argparse
import sys

__author__ = 'Bruce'

# 全局变量
target_host = ''
target_port = 0


# 提升逼格专用函数
def usage():
    print "Usage:python scanner.py -t <HOST> -p <PORT>"
    print "Examples:"
    print  "python scanner.py -t 127.0.0.1 -p 22"
    sys.exit(0)


# 获取用户输入
def parse_args():
    parser = argparse.ArgumentParser(description="Bruce's Net Tool")
    # 必须项
    parser.add_argument("-t", "--target_host", help="the ip or domain of target", default="0.0.0.0")
    parser.add_argument("-p", "--target_port", help="the host port", default=0)
    return parser.parse_args()


# 执行扫描
def connScan(target_host, target_port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_host, target_port))
        client.send('violent')
        results = client.recv(1024)
        print '[+] %d/tcp open ,result: %s' % (target_port, str(results))
        client.close()
    except:
        print '[-]%d/tcp closed' % target_port


def main():
    global target_host
    global target_port
    print("Bruce's Net Tool")
    args = parse_args()
    target_host = args.target_host
    target_port = int(args.target_port)
    if not len(sys.argv[1:]):
        usage()
    if len(target_host) and target_port > 0:
        connScan(target_host, target_port)


if __name__ == "__main__":
    main()