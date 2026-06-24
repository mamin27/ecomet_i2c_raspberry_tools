#!/usr/bin/env python3

import sys,os

sys.path.append(os.getenv("HOME") + '/ecomet_i2c_raspberry_tools/ecomet_i2c_sensors')
from  ecomet_i2c_sensors.ecomet.winds01 import winds01, winds01_constant
import time

import logging
from datetime import datetime

# ====================== ORIGINAL LOGGER (summary) ======================
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

# ====================== NEW DETAILED LOGGER ======================
measurement_logger = logging.getLogger('measurement')
measurement_logger.setLevel(logging.INFO)

detail_handler = logging.FileHandler('measurement.log', mode='w')
detail_handler.setLevel(logging.INFO)

detail_formatter = logging.Formatter()
detail_handler.setFormatter(detail_formatter)
measurement_logger.addHandler(detail_handler)

# Prevent propagation to root logger if you don't want duplicate console output
measurement_logger.propagate = False


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

# ====================== SAFE ROUND ======================
def safe_round(val, decimals=2, default="N/A"):
    if val is None:
        return default
    try:
        return round(float(val), decimals)
    except (TypeError, ValueError):
        return default

sens = winds01.WINDS01()
sens._logger = logging.getLogger('ecomet.ecomet01')
sens._logger.info('Start logging ...')

value = 0x00
stime = 6
set = 0
start = None
diff = None
print("Blue LED Setting? (On[o]/Off[f]):")
dev_selector = input("> ").strip().lower()
if dev_selector in ["on","o"]:
	sens.write_register ( register = 'REG_INIT', value = [0b01100000])
elif dev_selector in ["off","f"]:
	sens.write_register ( register = 'REG_INIT', value = [0b00000000])
else:
	print("⚠️  Wrong selection!")
	sys.exit(1)
sens.write_register ( register = 'REG_CONF', value = [0b00001110])
data = sens.read_register ( register = 'REG_SERIAL_NUMBER' )
print (f"Serial Number: 0x{data[0]:08X}")
time.sleep(stime)
while True:
	while True:
		data = sens.read_register ( register = 'REG_INIT' )
		newV = data[0] | 0b10000000 
		sens.write_register ( register = 'REG_INIT', value = [newV] )
		data = sens.read_register ( register = 'REG_INIT' )
		#print (f"{data[0]:08b}")
		if (data[0] & 0b10000000) == 0:
			break  # Exit the loop
		time.sleep(0.2)
	#data = sens.read_register ( register = 'REG_CONF' )
	#time.sleep(stime)
	#data = sens.read_register ( register = 'REG_INIT' )
	#time.sleep(2)
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
	time.sleep(stime)

	# ====================== CALCULATIONS (All variables always defined) ======================
	gust00 = reg_gust00 * 0.10194
	avg00  = reg_avg00  * 0.003403

	avg30 = gust30 = None
	if reg_avg30 <= 16777200:
		avg30 = reg_avg30 * 0.0006807
		gust30 = reg_gust30 * 0.10194

	avg60 = gust60 = None
	if reg_avg60 <= 16777200:
		avg60 = reg_avg60 * 0.00034034
		gust60 = reg_gust60 * 0.10194

	avg360 = gust360 = None          # ← This line was missing in your current code
	if reg_avg360 <= 16777200:
		avg360 = reg_avg360 * 0.000056723
		gust360 = reg_gust360 * 0.10194

	# ====================== CONSOLE OUTPUT (Safe) ======================
	print(f"------------------------------------------------------")
	print(f"Count: {reg_ValidCnt} Index: {reg_EE_Index}")
	print(f"AVG00:  {safe_round(avg00)} m/s    GUST00:  {safe_round(gust00)} m/s")
	print(f"AVG30:  {safe_round(avg30)} m/s    GUST30:  {safe_round(gust30)} m/s")
	print(f"AVG60:  {safe_round(avg60)} m/s    GUST60:  {safe_round(gust60)} m/s")
	print(f"AVG360: {safe_round(avg360)} m/s   GUST360: {safe_round(gust360)} m/s")
	#print(f"REG_GUST360: {reg_gust360}")

	measurement_logger.info(
		f"{reg_ValidCnt}:{reg_EE_Index}:"
		f"{safe_round(avg00)}:{safe_round(avg30)}:{safe_round(avg60)}:{safe_round(avg360)}:"
		f"{safe_round(gust00)}:{safe_round(gust30)}:{safe_round(gust60)}:{safe_round(gust360)}"
	)
