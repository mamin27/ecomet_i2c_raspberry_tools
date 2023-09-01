#!/usr/bin/env python3

import sys
print (sys.version)
from  ecomet_i2c_sensors.sn_gcja5 import sn_gcja5
import logging

sens = sn_gcja5.SN_GCJA5()

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='sn-gcja5.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
sens._logger = logging.getLogger('ecomet.sn-gcja5')
sens._logger.info('Start logging ...')

ret = sens.self_test()
if ret == 0 :
    print(":TEST_PASSED:")
else :
    print(":MISSING_CHIP:")

register = sn_gcja5.conf_register_list()
print ('{}'.format(register))
