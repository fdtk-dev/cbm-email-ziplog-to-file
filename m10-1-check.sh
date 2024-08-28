#!/usr/bin/env bash
LOG_DIR=~/cbm_log/
LOG_FILES=$LOG_DIR`date +%Y%m%d`*.txt
LOG_FILE=$(echo $LOG_FILES |rev|cut -f 1-2 -d" "|rev)
hdd=`cat $LOG_FILE | grep -e "State                                   :" |grep -e "HSP" -e "OPT" -e "RDY"|wc -l`
fan=`cat $LOG_FILE |grep FANU# |grep Normal|wc -l`
psu=`cat $LOG_FILE |grep PSU#|grep Normal |wc -l`
cpu=`cat $LOG_FILE |grep CPU#|grep Normal |wc -l`
ram=`cat $LOG_FILE |grep "MEM#... Status:Normal" |wc -l`
nic=`cat $LOG_FILE |grep -e "^net[0-9]" |grep ok |wc -l`
dbs=`cat $LOG_FILE |grep "COUNT(" -A 3 |grep "   "|wc -l `
zpool=`cat $LOG_FILE |grep -E "(rpool|backup).*[1-9]* -" |grep ONLINE |wc -l`
nxport=`cat $LOG_FILE |grep ./nxinit |wc -l`
echo
if [ $hdd = "153" ]; then echo "硬碟正常 153顆" ; else echo "硬碟異常 $hdd" ; fi
if [ $fan = "301" ]; then echo "風扇正常 301顆" ; else echo "風扇異常 $fan" ; fi
if [ $psu = "86" ]; then echo "電源供應器正常 86顆" ; 
else 
	echo "電源供應器異常 $psu" ; 
	cat $LOG_FILE |grep -E "### |PSU#|<div hostname" |grep -v Normal|grep PSU -B 2
fi
if [ $cpu = "43" ]; then echo "CPU正常 43顆" ; else echo "CPU異常 $cpu" ; fi
if [ $ram = "176" ]; then echo "RAM正常 176條" ; else echo "RAM異常 $ram" ; fi
if [ $nic = "237" ]; then echo "NET#正常 237個" ; else echo "NET#異常 $nic" ; fi
if [ $dbs = "16" ]; then echo "Oracle 資料庫正常 16個" ; else echo "Oracle 資料庫異常 $dbs" ; fi
if [ $zpool = "67" ]; then echo "zpool 資料正常 67個" ; else echo "zpool 資料異常 $zpool" ; fi
if [ $nxport = "43" ]; then echo "nxport正常 43臺" ; else echo "nxport異常 $nxport" ; fi
