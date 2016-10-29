#!/usr/bin/env python
#coding:utf-8
'''
功能：使用python-nmap扫描端口
日期: 2016-10-28
版本: V2
'''
import nmap
import socket
import argparse
import sys
import threading

__author__ = 'Bruce'

#全局变量
ports = [21,22,23,80,443,1521,3306,3389,6379,9000]
target_host = ''
target_port = ''

#提升逼格专用函数
def usage():
    print "Usage:python scanner_nmap.py -t <HOST> -p <PORT>"
    print "Examples:"
    print  "python scanner.py -t 127.0.0.1 -p 22"
    sys.exit(0)
    
#获取用户输入
def parse_args():
    parser = argparse.ArgumentParser(description="Bruce's Net Tool")
    #必须项
    parser.add_argument("-t", "--target_host", help="the ip or domain of target", default = "0.0.0.0")
    parser.add_argument("-p", "--target_port", help="the host port", default = 0)
    # 可选项是否为全局扫描不需要赋值 存储为bool
    parser.add_argument(
        "-a",
        "--all",
        help="all ports",
        action='store_true'
    )
    return parser.parse_args()

#执行扫描
def nmapScan(target_host, target_port):
   
    target_port = str(target_port)
    nm = nmap.PortScanner()
    nm.scan(str(target_host), str(target_port))
    
    port = target_port
    name = nm[target_host]['tcp'][int(target_port)]['name']
    state = nm[target_host]['tcp'][int(target_port)]['state']
    product = nm[target_host]['tcp'][int(target_port)]['product']
    extrainfo = nm[target_host]['tcp'][int(target_port)]['extrainfo']
    reason = nm[target_host]['tcp'][int(target_port)]['reason']
    version = nm[target_host]['tcp'][int(target_port)]['version']
    conf = nm[target_host]['tcp'][int(target_port)]['conf']
    
    if state == "open":
        print "[*] "+target_host+" tcp/"+port+" state:"+state+" name:"+name+" product:"+product+" extrainfo:"+extrainfo+" reason:"+reason+" version:"+version+" conf:"+conf
    else:
        print "[-] "+target_host+" tcp/"+port+" state:"+state+" name:"+name+" product:"+product+" extrainfo:"+extrainfo+" reason:"+reason+" version:"+version+" conf:"+conf

    
def main():
    global ports
    global target_host
    global target_port
    print("Bruce's Net Tool")
    args = parse_args()    
    target_host = args.target_host
    target_port = args.target_port
    all = args.all
    if not  len(sys.argv[1:]) :
        usage()
        
    if all :
        for port in ports:
            t = threading.Thread(target=nmapScan, args=(target_host,port))
            t.start()
    elif len(target_host) and target_port > 0:
        nmapScan(target_host, target_port)
    else:
        usage()
          
if __name__ == "__main__":
    main()
  