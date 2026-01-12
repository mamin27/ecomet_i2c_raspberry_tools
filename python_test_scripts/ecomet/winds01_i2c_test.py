#!/usr/bin/env python3

import sys,os

sys.path.append(os.getenv("HOME") + '/ecomet_i2c_raspberry_tools/ecomet_i2c_sensors')
from  ecomet_i2c_sensors.ecomet.winds01 import winds01, winds01_constant
import time
#from hdc1080 import hdc1080

import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='ecomet01.log',
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

sens = winds01.WINDS01()
sens._logger = logging.getLogger('ecomet.ecomet01')
sens._logger.info('Start logging ...')

value = 0x10
stime = 1
set = 0
start = None
diff = None
while (1):
	#data = sens.read_register ( register = 'REG_SERIAL_NUMBER' )
	#time.sleep(stime)
	#data = sens.write_register ( register = 'REG_CONF', value = [0b00000010])
	#time.sleep(stime)
	#data = sens.write_register ( register = 'REG_INIT', value = [0b10000000] )
	#time.sleep(stime)
	#while True:
	#	data = sens.read_register ( register = 'REG_INIT' )
		#print(f"{data[0] & 0b1000000}")
	#	if (data[0] & 0b10000000) == 0:
	#		print("Bit has changed to 0. Operation complete.")
	#		break  # Exit the loop
	#	time.sleep(0.1)

	#data = sens.read_register ( register = 'REG_CONF' )
	#time.sleep(stime)
	#data = sens.read_register ( register = 'REG_INIT' )
	#time.sleep(stime)
	data_cnt = sens.read_register ( register = 'REG_ValidCnt' )
	time.sleep(stime)
	if int(data_cnt[0]) == 0 and set == 0:
		start = datetime.now()
		print(f"Start Counting ...")
		set = 1
	if int(data_cnt[0]) != 0 and set == 1:
		set = 2
	elif int(data_cnt[0]) == 0 and set == 2:
		if start != None:
			end = datetime.now()
			diff = end - start
			start = end
			set = 3
	data_avg = sens.read_register ( register = 'REG_AVG00' )
	time.sleep(stime)
	#data = sens.read_register ( register = 'REG_EEPROM_AVG' )
	data_gust = sens.read_register ( register = 'REG_GUST00' )
	time.sleep(stime)
	#data = sens.read_register ( register = 'REG_EEPROM_GUST' )
	gust_imp = ((data_gust[0] & 0xFF) << 8) | (data_gust[0] >> 8)
	gust = float(gust_imp * 0.10194)
	avg_imp = ((data_avg[0] & 0xFF) << 8) | (data_avg[0] >> 8)
	avg = float(avg_imp * 0.003403) 
	print (f"Count: {data_cnt[0]} AVG: {round(avg,2)} m.s, GUST: {round(gust,2)} m.s SET: {set}")
	if set >= 3:
		if set == 3:
			print(f"Time diff: {diff}")
			set = 4
		if int(data_cnt[0]) > 0:
			set = 2
	#print (f"AVG: {data_avg[0]} m.s, GUST: {data_gust[0]} m.s")
	#time.sleep(stime)
	#time.sleep(stime)
	#data = sens.read_register ( register = 'REG_AVG30' )
	#time.sleep(stime)
	#data = sens.read_register ( register = 'REG_AVG60' )
	#time.sleep(stime)
	#data = sens.read_register ( register = 'REG_AVG360' )
	#time.sleep(stime)
	#data = sens.read_register ( register = 'REG_GUST00' )
	#time.sleep(stime)
	#data = sens.read_register ( register = 'REG_GUST30' )
	#time.sleep(stime)
	#data = sens.read_register ( register = 'REG_GUST60' )
	#time.sleep(stime)
	#data = sens.read_register ( register = 'REG_GUST360' )
	#time.sleep(stime)
	#data = sens.read_register ( register = 'REG_ValidCnt' )
	#time.sleep(stime)
