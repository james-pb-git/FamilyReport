#!/bin/bash
source /Users/bopang/.bash_profile
wd="/Users/bopang/Documents/ComputerScience/Practice/FamilyReport"
log_file_name=log_`date +"%Y%m%d"`
touch ${wd}/log/${log_file_name}
chmod a+w ${wd}/log/${log_file_name}
/Users/bopang/anaconda3/bin/python ${wd}/FamilyReport/run_report.py >>${wd}/log/${log_file_name}
