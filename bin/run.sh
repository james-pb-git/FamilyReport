source /Users/bopang/.bash_profile
wd="/Users/bopang/Documents/ComputerScience/Practice/FamilyReport"
log_file_name=log_`date +"%Y%m%d"`
touch ${wd}/log/${log_file_name}
python ${wd}/FamilyReport/run_report.py >>${wd}/log/${log_file_name} &
