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


def pad_to_21_left(bytes_list: list[int]) -> list[int]:
    """Strip leading 0x00 then pad left with 0x00 to exactly 21 bytes"""
    # Convert to bytes and strip leading zeros
    data = bytes(bytes_list).lstrip(b'\x00')
    # Pad left
    padding_needed = 21 - len(data)
    if padding_needed < 0:
        raise ValueError("Data longer than 20 bytes after stripping")
    return [0] * padding_needed + list(data)

def int_to_hex_bytes(value: int, min_length: int = None) -> list[int]:
    """
    Convert large integer to list of bytes (big-endian).
    Optionally pad with leading zeros to reach min_length.
    """
    hex_str = f"{value:x}"

    if len(hex_str) % 2 == 1:
        hex_str = "0" + hex_str

    bytes_list = [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]

    if min_length is not None and len(bytes_list) < min_length:
        bytes_list = [0] * (min_length - len(bytes_list)) + bytes_list
    
    return bytes_list

sens = winds01.WINDS01()
sens._logger = logging.getLogger('ecomet.ecomet01')
sens._logger.info('Start logging ...')

value = 0x00
stime = 6
set = 0
start = None
diff = None
data = sens.write_register ( register = 'REG_CONF', value = [0b00001110])
time.sleep(1)
while (1):
	#data = sens.read_register ( register = 'REG_SERIAL_NUMBER' )
	#time.sleep(stime)
	while True:
		data = sens.write_register ( register = 'REG_INIT', value = [0b10000000] )
		#print(f"{data}")
		if (data & 0b10000000) == 0:
			#print("Bit has changed to 0. Operation complete.")
			break  # Exit the loop
		time.sleep(0.2)

	#data = sens.read_register ( register = 'REG_CONF' )
	#time.sleep(stime)
	data = sens.read_register ( register = 'REG_INIT' )
	time.sleep(2)
	#data_cnt = sens.read_register ( register = 'REG_ValidCnt' )
	#time.sleep(stime)
	#data_eeprom = int_to_hex_bytes(sens.read_register ( register = 'REG_EEPROM_AVG' )[0])
	data_bulk = pad_to_21_left(int_to_hex_bytes(sens.read_register ( register = 'REG_BULK' )[0]))
	reg_avg00   = int.from_bytes(data_bulk[0:2],   "little")
	reg_avg30   = int.from_bytes(data_bulk[2:5],   "little")
	reg_avg60   = int.from_bytes(data_bulk[5:8],   "little")
	reg_avg360  = int.from_bytes(data_bulk[8:11],  "little")
	reg_gust00  = int.from_bytes(data_bulk[11:13], "little")
	reg_gust30  = int.from_bytes(data_bulk[13:15], "little")
	reg_gust60  = int.from_bytes(data_bulk[15:17], "little")
	reg_gust360 = int.from_bytes(data_bulk[17:19], "little")
	reg_ValidCnt =  int.from_bytes(data_bulk[19:20], "little")
	reg_EE_Index =  int.from_bytes(data_bulk[20:21], "little")
	if int(reg_ValidCnt) == 0 and set == 0:
		start = datetime.now()
		print(f"Start Counting ...")
		set = 1
	if int(reg_ValidCnt) != 0 and set == 1:
		set = 2
	elif int(reg_ValidCnt) == 0 and set == 2:
		if start != None:
			end = datetime.now()
			diff = end - start
			start = end
			set = 3
	time.sleep(stime)
	gust00 = float(reg_gust00 * 0.10194)
	gust30 = float(reg_gust30 * 0.10194)
	gust60 = float(reg_gust60 * 0.10194)
	gust360 = float(reg_gust360 * 0.10194)
	avg00 = float(reg_avg00 * 0.003403)
	if (reg_avg30 <= 16777200 ):
		avg30 = float(reg_avg30 * 0.0006807)
	else:
		avg00 = None
	if (reg_avg60 <= 16777200 ):
		avg60 = float(reg_avg60 * 0.00034034)
	else:
		avg60 = None
	if (reg_avg360 <= 16777200 ):
		avg360 = float(reg_avg360 * 0.000056723)
	else:
		avg360 = None
	print (f"------------------------------------------------------")
	print (f"Count: {reg_ValidCnt} Index: {reg_EE_Index} SET: {set}")
	print (f"AVG00: {round(avg00,2)} m.s, GUST00: {round(gust00,2)}")
	if avg30 == None:
		print (f"AVG30: N/A m.s, GUST30: {round(gust30,2)}")
	else:
		print (f"AVG30: {round(avg30,2)} m.s, GUST30: {round(gust30,2)}")
	if avg60 == None:
		print (f"AVG60: N/A m.s, GUST60: {round(gust60,2)}")
	else:
		print (f"AVG60: {round(avg60,2)} m.s, GUST60: {round(gust60,2)}")
	if avg360 == None:
		print (f"AVG360: N/A m.s, GUST360: {round(gust360,2)}")
	else:
		print (f"AVG360: {round(avg360,2)} m.s, GUST360: {round(gust360,2)}")
	if set >= 3:
		if set == 3:
			print(f"Time diff: {diff}")
			set = 4
		if int(reg_ValidCnt) > 0:
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
