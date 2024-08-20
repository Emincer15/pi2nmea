#! /bin/bash
# bash file to enter correct directory and activate virtual environment on pi
cd /home/pi2nmea/software/pi2nmea
source .venvpi/bin/activate
python3 rbmq_receive.py
