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

def test_bit(reg, bit_number):
    mask = 1 << bit_number          # create mask
    return (reg & mask) != 0        # True if bit is set

def reset ():
	data = sens.read_register ( register = 'REG_INIT' )
	newV = data[0] | 0b00000010 
	sens.write_register ( register = 'REG_INIT', value = [newV] )

sens = winds01.WINDS01()
sens._logger = logging.getLogger('ecomet.ecomet01')
sens._logger.info('Start logging ...')

value = 0x00
stime = 1
set = 0
start = None
diff = None
data = sens.read_register ( register = 'REG_SERIAL_NUMBER' )
print (f"Serial Number: 0x{data[0]:08X}")
dev_mode = None
dev_selector = None
dev_selector_choise = None
print("Select Test? (Tachometer[t]/EEPROM[e]/Reset Chip[r] Test):")
dev_selector = input("> ").strip().lower()
if dev_selector in ["tachometer","t"]:
	dev_selector_choise = 'tach'
	print("DEV MODE? (Activate[a]/Deactive[d]/Measure[.]/Reset[x]):")
elif dev_selector in ["reset","r"]:
	print (f"Reset of Wind Speed Chip")
	reset()
	sys.exit(0)
elif dev_selector in ["eeprom","e"]:
	dev_selector_choise = 'eeprom'
	data = sens.read_register ( register = 'REG_INIT' )
	newV = data[0] | 0b00000001 
	sens.write_register ( register = 'REG_INIT', value = [newV] )
	print("DEV MODE? (Activate[a]):")
else:
	print("⚠️  Wrong selection!")
	sys.exit(1)
while True:
	try:
		dev_choice = input("> ").strip().lower()
		if dev_choice in ["acti", "a"]:
			print("✅ DEV MODE Activated")
			dev_mode = True
			sens.write_register ( register = 'REG_CONF', value = [0b10000000])
			time.sleep(stime)
			if dev_selector_choise == 'tach':
				data = sens.read_register ( register = 'REG_TACH_TIC_Cnt' )
				print (f"Counted TIC Count: {data[0]}")
			elif dev_selector_choise == 'eeprom':
				data = sens.read_register ( register = 'REG_ERROR' )
				if test_bit(data[0],1):
					print(f"⚠️ EEPROM Test with ERROR during Write")
				else:
					print(f"✅ EEPROM Test with correct!")
				break
		elif dev_choice in ["deact", "d"]:
			print("ℹ️  DEV MODE Deactivated")
			dev_mode = False
			sens.write_register ( register = 'REG_CONF', value = [0b00000000])
			break
		elif dev_choice in [".", "m"] and dev_mode == True:
			data = sens.read_register ( register = 'REG_TACH_TIC_Cnt' )
			print (f"Counted TIC Count: {data[0]}")
			time.sleep(stime)
		elif dev_choice in ["x",] and dev_mode == True:
			sens.write_register ( register = 'REG_TACH_TIC_Cnt', value = [0b00000000] )
			data = sens.read_register ( register = 'REG_TACH_TIC_Cnt' )
			print (f"Counted TIC Count: {data[0]}")
			time.sleep(stime)
		else:
			print("⚠️  Wrong selection!")
			sys.exit(1)

	except EOFError:
		# Ctrl+D (alebo Ctrl+Z na Windows) = rovnocenné s No
		print("ℹ️ (Ctrl+D) → DEV MODE Deactivated")
		dev_mode = False
		sens.write_register ( register = 'REG_CONF', value = [0b00000000])
		break
	except KeyboardInterrupt:
		print("⛔ Program Interrupted (Ctrl+C)")
		sys.exit(0)
