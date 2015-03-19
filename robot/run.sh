twistd --logfile=$PWD/start.log -repoll -y main.py
tail -f start.log
