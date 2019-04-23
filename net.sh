#!/bin/bash
# -*- coding: utf-8 -*-
echo 'SHANGHAI ELECTRIC'

#配置IP的网卡数
C=`ip add| grep inet | grep 'scope global'|wc -l`
if [ $C -lt 1 ];then 
   



#在使用的网卡名称
NET=`ip link | grep "state UP" | awk '{print $2}'|awk -F ':' '{print $1}'`
NET_COUNT=`ip link | grep "state UP" | awk '{print $2}'|awk -F ':' '{print $1}'|wc -l`
NET_1=`ip link | grep "state UP" | awk '{print $2}'|awk -F ':' '{print $1}'|head -1`
NET_2=`ip link | grep "state UP" | awk '{print $2}'|awk -F ':' '{print $1}'|tail -1`



#网卡配置文件名称
NETCONFIG=`ls /etc/sysconfig/network-scripts/| grep -E "ifcfg-$NET_1|ifcfg-$NET_2"| grep -v "lo"`

#网卡配置文件数目
NETCONFIG_COUNT=`ls /etc/sysconfig/network-scripts/| grep -E "ifcfg-$NET_1|ifcfg-$NET_2"|grep -v "lo"|wc -l`



NET_2UUID=`nmcli con | grep  $NET_2 |awk  '{print $(NF-2)}'|tail -1`
if [ $NET_COUNT = 2 ] && [ $NETCONFIG_COUNT = 1 ];then
  cp /etc/sysconfig/network-scripts/$NETCONFIG  /etc/sysconfig/network-scripts/ifcfg-$NET_2
  sed -i "s/^UUID.*/UUID=$NET_2UUID/" /etc/sysconfig/network-scripts/ifcfg-$NET_2
  sed -i "s/^NAME.*/UUID=$NET_2/" /etc/sysconfig/network-scripts/ifcfg-$NET_2
  sed -i "s/^DEVICE.*/DEVICE=$NET_2/" /etc/sysconfig/network-scripts/ifcfg-$NET_2
fi

read -p "host:" HOST
hostnamectl set-hostname $HOST

for i in $NET
  do
   
    MAC_DE=`cat /etc/sysconfig/network-scripts/ifcfg-$i | grep HWADDR|awk -F "=" '{print $2}'`
    MAC=`ip addr show $i| grep "link/ether" | awk  '{print $2}'`
      read -p "IP:" IP
   #   read -P "GATEWAY:" GATEWAY
      GWL=`echo $IP| awk -F "." '{print $4}'`
      GATEWAY=`echo $IP |sed  "s/$GWL/1/"`
      sed -i "s/^HWADDR.*/HWADDR=$MAC/" /etc/sysconfig/network-scripts/ifcfg-$i
      sed -i "s/^IPADDR.*/IPADDR0=$IP/" /etc/sysconfig/network-scripts/ifcfg-$i
      sed -i "s/^GATEWAY.*/GATEWAY0=$GATEWAY/" /etc/sysconfig/network-scripts/ifcfg-$i
done
fi 
