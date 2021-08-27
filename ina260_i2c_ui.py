#!/usr/bin/env python3

import sys
print (sys.version)
from PIL import ImageFont, Image
from i2c_pkg.ina260_pkg	import ina260_ui
from time import sleep
import qrcode
import logging
import os
import pickle

def child ():
   fd = open('ina_chip','wb')
   chip1._logger.debug("child0: %d" % os.getpid())
   data = chip1.measure_ui()
   pickle.dump(data, fd,-1)
   fd.close()
   os._exit(0)

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='ina260_ui.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

buf_voltage_1 = {}
buf_current_1 = {}
buf_voltage_2 = {}
buf_current_2 = {}

chip0 = ina260_ui.INA260_UI(chip = 0, time = 0.01)
chip1 = ina260_ui.INA260_UI(chip = 1, time = 0.01)

while True:
   newpid = os.fork()
   if newpid == 0:
      child()
   else:
      chip0._logger.debug("parent0: %d" % os.getpid())
      ((size_current_1,unit_current_1,buf_current_1),(size_voltage_1,unit_voltage_1,buf_voltage_1)) = chip0.measure_ui()
      os.waitid(os.P_PID,newpid,os.WEXITED)
      break
fd = open('ina_chip','rb')
((size_current_2,unit_current_2,buf_current_2),(size_voltage_2,unit_voltage_2,buf_voltage_2)) = pickle.load(fd)
fd.close()
os.remove('ina_chip')

chip0._logger.info("Measure Current 0")
chip0._logger.info("Size: %s", size_current_1)
chip0._logger.info("Buff: %s", buf_current_1)
chip0._logger.info("Unit: %s", unit_current_1)

chip0._logger.info("Measure Voltage 0")
chip0._logger.info("Size: %s", size_voltage_1)
chip0._logger.info("Buff: %s", buf_voltage_1)
chip0._logger.info("Unit: %s", unit_voltage_1)

chip0._logger.info("Measure Current 1")
chip0._logger.info("Size: %s", size_current_2)
chip0._logger.info("Buff: %s", buf_current_2)
chip0._logger.info("Unit: %s", unit_current_2)

chip0._logger.info("Measure Voltage 1")
chip0._logger.info("Size: %s", size_voltage_2)
chip0._logger.info("Buff: %s", buf_voltage_2)
chip0._logger.info("Unit: %s", unit_voltage_2)

data = {'current_size_1' : size_current_1,
        'buf_current_1' : buf_current_1,
        'voltage_size_1' : size_voltage_1,
        'buf_voltage_1' :buf_voltage_1,
        'current_size_2' : size_current_2,
        'buf_current_2' : buf_current_2,
        'voltage_size_2' : size_voltage_2,
        'buf_voltage_2' :buf_voltage_2
       }
