#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import datetime, time
import json

HOST = '10.100.10.200'
USER = 'Admin'
PWD = 'nandou'
API = 'http://10.100.10.200/zabbix/api_jsonrpc.php'

def get_zabbix_token():                                                         #定义获取zabbix登陆token方法
    data = {                                                                    #接口需要的参数
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": USER,
            "password": PWD
        },
        "id": 1

    }
    url = 'http://10.100.10.200/zabbix/api_jsonrpc.php'                          #接口地址
    headers = {"Content-Type": "application/json"}                              #请求头数据
    response = requests.post(url, json.dumps(data), headers=headers).content    #封装数据以及请求头使用POST方法请求数据获取返回结果
    result = json.loads(response)['result']
    return result
token = get_zabbix_token()
print token
def get_group():
    data = {
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
    "params": {
        "output": "extend",
    },
    "auth": token,
    "id": 1
    }
    url = API
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json.dumps(data), headers=headers).content
        result = json.loads(response)['result']
    except:
        result = {}
    return result

print get_group()

for i in get_group():
    print i
gp_list = []
for i in get_group():
    if any(j in i.values() for j in ("NewEnergy_Prodct", "NewEnergy_Test", u"尾气排放", u"楚道行")):
        gp_list.append({'name':i['name'],'groupid':i['groupid']})
print gp_list   #所有的主机组及对应的主机ID组成的列表

#根据主机组获取主机信息
def get_host(gid):
    data = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": ["groupid", "name"],
        "groupids": gid
    },
    "auth": token,
    "id": 1
    }
    url = API
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json.dumps(data), headers=headers).content

        result = json.loads(response)['result']
    except:
        result = {}
#print get_host(22)

keys = ["system.cpu.load[percpu,avg5]","system.cpu.load[percpu,avg15]","system.cpu.util[,idle]","vfs.fs.size[/,free]","vfs.fs.size[/,total]","vm.memory.size[available]","vm.memory.size[total]","vm.memory.size[used]"]


def get_info(hostid,keyid):
    data = (
            {
                "jsonrpc": "2.0",
                "method": "item.get",
                "params": {
                    "output": "extend",
                    "hostids":hostid,  #这个是host的id号
                    "search":{
                        "key_":keyid,

                    }
                },
                "auth": token,
                "id": 1
            })
    url = API
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json.dumps(data), headers=headers).content
        #print response
    except:
        resy = {}
    return json.loads(response)['result'][0]['lastvalue']
print get_info(10479,"system.cpu.util[,idle]")

