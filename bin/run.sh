cd ../
log_file_name=log_`date +"%Y%m%d"`
touch ./log/${log_file_name}
python ./FamilyReport/run_report.py >>./log/${log_file_name} &
