service cron start
sh /apt/bin/update_mask_info.sh
python /apt/util.py
python app.py