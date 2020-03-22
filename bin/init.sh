service cron start
sh /apt/bin/download_mask_dataset.sh
python /apt/util.py
python app.py