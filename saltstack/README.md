# saltstack

版本：1

目的:
    
    获取被监控(minion)机器的 处理器使用率、内存使用情况、磁盘使用情况、网卡流入流出 信息

实现思路:
    
    1. 自定义一个salt modules 脚本 （hostinfo.py） 该脚本返回所需数据(基本也是使用salt 自带的moduels和functions来获取)
    2. 同步hostinfo.py到各个监控机（minions）
    3. 编写python脚本(py_hostinfos.py)调用salt api接口 使用自定义的hostinfo.py 展示

实现流程:

     1. 安装saltstack 详见官网:https://repo.saltstack.com/#rhel
     2. 可以在本机同时安装 salt-master salt-minion(建议可以使用虚拟机多搞几个方便看效果)
     3. 在master和minion分别配置/etc/salt/master,/etc/salt/minion 使其在master机上 使用命令 # salt "*" test.ping 成功
     4. 在master上修改配置文件/etc/salt/master
           file_roots:
	       base:
	           - /srv/salt
     5. 创建自定义模块目录  #mkdir -p /srv/salt/_modules
       目录结构:
                [root@localhost ~]# cd /srv/
		[root@localhost srv]# tree
		.
		└── salt
		    └── _modules
			└── hostinfo.py
     6. 将 hostinfo.py 放入到 _modules 目录下
     7. 同步到各个minion #salt '*' saltutil.sync_all
     8. 运行py_hostinfos.py  (结果展示可以自己修改)运行效果如下:
-------------------------------------------------------------------------------------------------------
[root@localhost python_shell]# ./py_hostinfos.py 
---------------------------hostname-----------------------------------
{'model.jsh315.com_tomcat3': {'id': 'model.jsh315.com_tomcat3'}, 'model.jsh315.com_tomcat2': {'id': 'model.jsh315.com_tomcat2'}, 'model.jsh315.com_tomcat1': {'id': 'model.jsh315.com_tomcat1'}, 'www.jsh315.com_salt_master': {'id': 'www.jsh315.com_salt_master'}, 'model.jsh315.com_nginx': {'id': 'model.jsh315.com_nginx'}}
---------------------------cpuinfo-----------------------------------
model.jsh315.com_tomcat3 cpu_usage:0
model.jsh315.com_tomcat2 cpu_usage:0
model.jsh315.com_tomcat1 cpu_usage:0
www.jsh315.com_salt_master cpu_usage:0
model.jsh315.com_nginx cpu_usage:0
---------------------------meminfo-------------------------------------
model.jsh315.com_tomcat3  MemTotal:990 Used:664  Free: 326 
model.jsh315.com_tomcat2  MemTotal:990 Used:665  Free: 325 
model.jsh315.com_tomcat1  MemTotal:990 Used:664  Free: 326 
www.jsh315.com_salt_master  MemTotal:990 Used:650  Free: 340 
model.jsh315.com_nginx  MemTotal:990 Used:667  Free: 323 
---------------------------networkinfo-------------------------------------
model.jsh315.com_tomcat3
lo in:0  out:0
eth0 in:353010  out:353010
--------------------------------
model.jsh315.com_tomcat2
lo in:0  out:0
eth0 in:354155  out:354155
--------------------------------
model.jsh315.com_tomcat1
lo in:0  out:0
eth0 in:354304  out:354304
--------------------------------
www.jsh315.com_salt_master
docker0 in:2970213  out:2970213
veth16d3852 in:573729  out:573729
lo in:1325337  out:1325337
veth1c76a4f in:1507553  out:1507553
veth31c0835 in:574715  out:574715
vethaa69ae6 in:573508  out:573508
eth0 in:18229480  out:18229480
--------------------------------
model.jsh315.com_nginx
lo in:0  out:0
eth0 in:512196  out:512196
--------------------------------
---------------------------diskinfo-------------------------------------
model.jsh315.com_tomcat3
{'available': '507028', '1K-blocks': '507028', 'used': '0', 'capacity': '0%', 'filesystem': 'tmpfs'}
{'available': '507028', '1K-blocks': '507028', 'used': '0', 'capacity': '0%', 'filesystem': 'tmpfs'}
{'available': '9108228', '1K-blocks': '10190136', 'used': '541236', 'capacity': '6%', 'filesystem': '/dev/mapper/docker-8:17-262145-a759235479aae135337031d2cccfebb673d99e94b697180d9f4a08c7ab5f3dc5'}
{'available': '15899032', '1K-blocks': '20504628', 'used': '3540976', 'capacity': '19%', 'filesystem': '/dev/sdb1'}
{'available': '15899032', '1K-blocks': '20504628', 'used': '3540976', 'capacity': '19%', 'filesystem': '/dev/sdb1'}
{'available': '15899032', '1K-blocks': '20504628', 'used': '3540976', 'capacity': '19%', 'filesystem': '/dev/sdb1'}
{'available': '507028', '1K-blocks': '507028', 'used': '0', 'capacity': '0%', 'filesystem': 'tmpfs'}
{'available': '65524', '1K-blocks': '65536', 'used': '12', 'capacity': '1%', 'filesystem': 'shm'}
model.jsh315.com_tomcat2
{'available': '507028', '1K-blocks': '507028', 'used': '0', 'capacity': '0%', 'filesystem': 'tmpfs'}
{'available': '507028', '1K-blocks': '507028', 'used': '0', 'capacity': '0%', 'filesystem': 'tmpfs'}
{'available': '9108228', '1K-blocks': '10190136', 'used': '541236', 'capacity': '6%', 'filesystem': '/dev/mapper/docker-8:17-262145-ad58772de6214f16381c1ae179df1a8c184ec8245fd64725d93b23f4da588286'}
{'available': '15899032', '1K-blocks': '20504628', 'used': '3540976', 'capacity': '19%', 'filesystem': '/dev/sdb1'}
{'available': '15899032', '1K-blocks': '20504628', 'used': '3540976', 'capacity': '19%', 'filesystem': '/dev/sdb1'}
{'available': '15899032', '1K-blocks': '20504628', 'used': '3540976', 'capacity': '19%', 'filesystem': '/dev/sdb1'}
{'available': '507028', '1K-blocks': '507028', 'used': '0', 'capacity': '0%', 'filesystem': 'tmpfs'}
{'available': '65524', '1K-blocks': '65536', 'used': '12', 'capacity': '1%', 'filesystem': 'shm'}
model.jsh315.com_tomcat1
{'available': '507028', '1K-blocks': '507028', 'used': '0', 'capacity': '0%', 'filesystem': 'tmpfs'}
{'available': '507028', '1K-blocks': '507028', 'used': '0', 'capacity': '0%', 'filesystem': 'tmpfs'}
{'available': '9107932', '1K-blocks': '10190136', 'used': '541532', 'capacity': '6%', 'filesystem': '/dev/mapper/docker-8:17-262145-e72ae6736fa07e59271c360af287b4db35e35b8d9da523b9fc08a277ae2f6094'}
{'available': '15899032', '1K-blocks': '20504628', 'used': '3540976', 'capacity': '19%', 'filesystem': '/dev/sdb1'}
{'available': '15899032', '1K-blocks': '20504628', 'used': '3540976', 'capacity': '19%', 'filesystem': '/dev/sdb1'}
{'available': '15899032', '1K-blocks': '20504628', 'used': '3540976', 'capacity': '19%', 'filesystem': '/dev/sdb1'}
{'available': '507028', '1K-blocks': '507028', 'used': '0', 'capacity': '0%', 'filesystem': 'tmpfs'}
{'available': '65524', '1K-blocks': '65536', 'used': '12', 'capacity': '1%', 'filesystem': 'shm'}
www.jsh315.com_salt_master
{'available': '15899032', '1K-blocks': '20504628', 'used': '3540976', 'capacity': '19%', 'filesystem': '/dev/sdb1'}
{'available': '164328', '1K-blocks': '289293', 'used': '105509', 'capacity': '40%', 'filesystem': '/dev/sda1'}
{'available': '12827468', '1K-blocks': '18208184', 'used': '4432748', 'capacity': '26%', 'filesystem': '/dev/sda2'}
{'available': '506936', '1K-blocks': '507028', 'used': '92', 'capacity': '1%', 'filesystem': 'tmpfs'}
model.jsh315.com_nginx
{'available': '507028', '1K-blocks': '507028', 'used': '0', 'capacity': '0%', 'filesystem': 'tmpfs'}
{'available': '507028', '1K-blocks': '507028', 'used': '0', 'capacity': '0%', 'filesystem': 'tmpfs'}
{'available': '9060360', '1K-blocks': '10190136', 'used': '589104', 'capacity': '7%', 'filesystem': '/dev/mapper/docker-8:17-262145-1503ca49817a6058d9ebe8f96e839187f9d76f2b854005a731c17005db713899'}
{'available': '15899032', '1K-blocks': '20504628', 'used': '3540976', 'capacity': '19%', 'filesystem': '/dev/sdb1'}
{'available': '15899032', '1K-blocks': '20504628', 'used': '3540976', 'capacity': '19%', 'filesystem': '/dev/sdb1'}
{'available': '15899032', '1K-blocks': '20504628', 'used': '3540976', 'capacity': '19%', 'filesystem': '/dev/sdb1'}
{'available': '507028', '1K-blocks': '507028', 'used': '0', 'capacity': '0%', 'filesystem': 'tmpfs'}
{'available': '65524', '1K-blocks': '65536', 'used': '12', 'capacity': '1%', 'filesystem': 'shm'}

-------------------------------------------------------------------------------------------------------

python版本2.4-2.7
Centos 6.5 64
Stackstack 2015-2016