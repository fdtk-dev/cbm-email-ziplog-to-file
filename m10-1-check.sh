#!/usr/bin/env bash
LOG_DIR=/home/ceds_log/cbm_log/
ZIP_DIR=/home/ceds_log/cbm_zip_dev/
LOG_FILES=$LOG_DIR`date +%Y%m%d`*.txt
LOG_ZIP_FILE=$ZIP_DIR`date +%Y%m%d`*-cbm-log.zip
unzip -o -qq $LOG_ZIP_FILE -d /home/ceds_log/cbm_log
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

row() {
    name=$1; expected=$2; actual=$3; unit=$4
    if [ "$actual" = "$expected" ]; then
        status="正常"; color="#2e7d32"; icon="&#10004;"
    else
        status="異常"; color="#c62828"; icon="&#10008;"
    fi
    printf '<tr>\n<td style="padding:10px 12px;border:1px solid #e0e0e0;text-align:left;">%s</td>\n<td style="padding:10px 12px;border:1px solid #e0e0e0;text-align:center;">%s</td>\n<td style="padding:10px 12px;border:1px solid #e0e0e0;text-align:center;">%s %s</td>\n<td style="padding:10px 12px;border:1px solid #e0e0e0;text-align:center;color:%s;font-weight:bold;">%s %s</td>\n</tr>\n' "$name" "$expected" "$actual" "$unit" "$color" "$icon" "$status"
}

cat <<'HEADER'
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>m10-1 設備健康檢查報告</title>
</head>
<body style="margin:0;padding:20px;background-color:#f4f4f4;font-family:'Microsoft JhengHei','PingFang TC',Arial,sans-serif;">
<div style="max-width:680px;margin:0 auto;background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.08);">
<div style="background:#1565c0;color:#ffffff;padding:18px 24px;font-size:18px;font-weight:bold;letter-spacing:1px;">m10-1 設備健康檢查報告</div>
<table style="width:100%;border-collapse:collapse;">
<tr style="background:#e3f2fd;">
<th style="padding:10px 12px;border:1px solid #e0e0e0;text-align:left;">檢查項目</th>
<th style="padding:10px 12px;border:1px solid #e0e0e0;text-align:center;">預期數量</th>
<th style="padding:10px 12px;border:1px solid #e0e0e0;text-align:center;">實際數量</th>
<th style="padding:10px 12px;border:1px solid #e0e0e0;text-align:center;">狀態</th>
</tr>
HEADER
row "硬碟" 153 "$hdd" 顆
row "風扇" 301 "$fan" 顆
row "電源供應器" 86 "$psu" 顆
row "CPU" 43 "$cpu" 顆
row "RAM" 176 "$ram" 條
row "NET 網路介面" 237 "$nic" 個
row "Oracle 資料庫" 16 "$dbs" 個
row "zpool 儲存池" 67 "$zpool" 個
row "nxinit 程序" 43 "$nxport" 臺
if [ "$psu" != "86" ]; then
    echo '<tr><td colspan="4" style="padding:10px 12px;border:1px solid #e0e0e0;background:#ffebee;color:#c62828;font-weight:bold;">異常電源供應器明細</td></tr>'
    echo '<tr><td colspan="4" style="padding:10px 12px;border:1px solid #e0e0e0;background:#fff8f8;font-family:monospace;font-size:12px;white-space:pre-wrap;">'
    cat $LOG_FILE |grep -E "### |PSU#|<div hostname" |grep -v Normal|grep PSU -B 2 | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g'
    echo '</td></tr>'
fi
echo '</table>'
echo '</div>'
echo '</body>'
echo '</html>'
