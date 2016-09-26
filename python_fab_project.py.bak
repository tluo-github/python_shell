#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------
# Name:         生成环境代码包发布管理
# Purpose:      fabric 一键 拉取、备份、发布tomcat 非常适用于同时发布到多个tomcat服务器中
# Version:      1.0
# Author:       Bruce
# EMAIL:        530308461@qq.com
# Created:      2016-08-22
# Copyright:    (c) Bruce 2016
# Python:       2.4/2.7
#-----------------------------------------------------------------------------------------

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
import time
from ilogue.fexpect import expect, expecting, run 

env.user = 'root'
env.hosts = ['192.168.0.2']
env.password = 'Jsh315_docker'


env.project_dev_source = '/home/git/jsh_model_api' #本地git包位置
env.project_dev_tar_source = 'jsh_mode_api.war'   #发布包文件

env.deploy_project_root = '/home/www/' #项目生成环境主目录
env.deploy_release_dir = 'release' #项目发布目录，位于主目录下
env.deploy_version=time.strftime("%Y%m%d")+"v1" #版本号


@runs_once
def local_gitpull_task(): #本地更新包文件
    print yellow("Start git pull..")
    with settings(warn_only=True):
        if local('test -d %s' % env.project_dev_source).failed:
            local('git clone git@code.aliyun.com:1443807900/jsh_model_api.git %s' % env.project_dev_source )
    with lcd(env.project_dev_source ):
        local('git pull');
        
    print green("git pull package success!")
          
@task
def put_task():#上传文件
    print yellow("Start pull packega ...")
    with settings(warn_only=True):
        with cd(env.deploy_project_root+env.deploy_release_dir):
                run("mkdir -p %s" % (env.deploy_version)) #创建版本目录
    
    env.deploy_full_path=env.deploy_project_root+env.deploy_release_dir+"/"+env.deploy_version
    
    with settings(warn_only=True):
            result = put(env.project_dev_source+"/"+env.project_dev_tar_source,env.deploy_full_path)    
    
    if result.failed and not confirm("put file failed, Continue[Y/N]?"):
            abort("Aborthing file put task!")    
            
    print green("Put package success!")
    
    
@task
def display_task(): #部署
    
    print yellow("Start display packega ...")
    env.deploy_full_path=env.deploy_project_root+env.deploy_release_dir+"/"+env.deploy_version
    run('sh /home/www/tomcat-8.0.36/bin/shutdown.sh')
    run('rm -rf /home/www/tomcat-8.0.36/webapps/*')
    run('cp %s/jsh_mode_api.war /home/www/tomcat-8.0.36/webapps/ROOT.war' % env.deploy_full_path)
    run('chown www:www /home/www/tomcat-8.0.36/webapps/ROOT.war')
    run('set -m ;/home/www/tomcat-8.0.36/bin/startup.sh start')   #set -m; 不加启动不了
    print green("display success!!")
    
    
@task
def go():
    local_gitpull_task() #拉取最新包文件
    put_task()  #将包文件复制到目标机器
    display_task() #在目标机器部署
