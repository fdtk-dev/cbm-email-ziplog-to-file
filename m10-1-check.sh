#!/usr/bin/env bash
LOG_DIR=~/cbm_log/
LOG_FILE=$LOG_DIR`date +%Y%m%d`*.txt
echo
echo "正常硬碟總數："
hdd=`cat $LOG_FILE | grep -e "State                                   :" |grep -e "HSP" -e "OPT" -e "RDY"|wc -l`
echo "正常風扇總數："
fan=`cat $LOG_FILE |grep FANU# |grep Normal|wc -l`
echo "正常電源供應器總數："
psu=`cat $LOG_FILE |grep PSU#|grep Normal |wc -l`
echo "正常CPU總數："
cpu=`cat $LOG_FILE |grep CPU#|grep Normal |wc -l`
echo "正常RAM總數："
ram=`cat $LOG_FILE |grep "MEM#... Status:Normal" |wc -l`
echo "正常NET#總數："
nic=`cat $LOG_FILE |grep -e "^net[0-9]" |grep ok |wc -l`
echo "正常Oracle 資料庫總數"
dbs=`cat $LOG_FILE |grep "COUNT(" -A 3 |grep "   "|wc -l `
if [ hdd = "153" ] then echo "硬碟正常 153顆" 
