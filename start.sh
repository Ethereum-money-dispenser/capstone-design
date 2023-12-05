# !/bin/bash
# Remove existing crontab entries
crontab -r

# Add new crontab entries
(crontab -l ; echo "*/10 * * * * cd ~/capstone-design/src/crawling && /usr/bin/python3 ./craw.py >> ~/log/log.txt 2>&1") | crontab -
(crontab -l ; echo "0 * * * * cd ~/capstone-design/src/crawling && /usr/bin/python3 ./backup.py >> ~/log/log.txt 2>&1") | crontab -
(crontab -l ; echo "0 * * * * cd ~/capstone-design/src/crawling && /usr/bin/python3 ./delete_dup.py >> ~/log/log.txt 2>&1") | crontab -

# web server start
cd ./src/web
python3 ./app.py